# recruitment/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse

from .models import RecruitmentSettings, RecruitmentApplication
from .serializers import RecruitmentSettingsSerializer, RecruitmentApplicationSerializer

from pdf_services import generate_recruitment_pdf
from email_services import send_html_email
from permissions import IsExecutive


def _build_applicant_data(application):
    """Single place to build the applicant dict so both views stay in sync."""
    return {
        "name": application.full_name,
        "email": application.email,
        "phone": getattr(application, 'phone', 'N/A'),
        "department": application.department,
        "session": getattr(application, 'session', 'N/A'),
        "hall": getattr(application, 'hall', 'N/A'),
        "student_id": getattr(application, 'student_id', 'N/A'),
        "skills": getattr(application, 'skills', 'N/A'),
        "motivation": getattr(application, 'motivation', 'N/A'),
        "payment_status": getattr(application, 'payment_status', 'PENDING'),
    }


class RecruitmentSettingsViewSet(viewsets.ModelViewSet):
    """API endpoint for managing recruitment dates and status."""
    queryset = RecruitmentSettings.objects.all()
    serializer_class = RecruitmentSettingsSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsExecutive()]


class RecruitmentApplicationViewSet(viewsets.ModelViewSet):
    """API endpoint for submitting and managing recruitment applications."""
    queryset = RecruitmentApplication.objects.all().order_by('-created_at')
    serializer_class = RecruitmentApplicationSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsExecutive()]

    def create(self, request, *base_kwargs, **kwargs):
        """
        Step 1 of 2: Save the application only.
        No PDF or email here — those fire after payment is confirmed.
        Returns the application id so the frontend can pass it to /payment/initiate/.
        """
        active_settings = RecruitmentSettings.objects.filter(is_open=True).first()
        if not active_settings:
            return Response(
                {"detail": "Recruitment is currently closed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *base_kwargs, **kwargs)

    def perform_create(self, serializer):
        # Just save — the frontend will immediately redirect to payment initiation.
        serializer.save()

    @action(detail=True, methods=['get'], permission_classes=[IsExecutive])
    def download_pdf(self, request, pk=None):
        """
        Executive manual download — always available regardless of payment status.
        GET /api/v1/recruitment-applications/{id}/download_pdf/
        """
        application = self.get_object()
        applicant_data = _build_applicant_data(application)
        pdf_buffer = generate_recruitment_pdf(applicant_data)

        return FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename=f"{application.full_name.replace(' ', '_')}_Application.pdf",
            content_type='application/pdf'
        )

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def download_invoice(self, request, pk=None):
        """
        Step 2 of 2 (applicant-facing): Download the payment invoice PDF.
        Only works after the linked transaction is COMPLETED.
        GET /api/v1/recruitment-applications/{id}/download_invoice/

        The frontend should redirect here after payment_success.
        """
        application = self.get_object()

        # Guard: must have a completed payment
        if getattr(application, 'payment_status', None) != 'COMPLETED':
            return Response(
                {"detail": "No completed payment found for this application."},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )

        completed_transaction = application.transactions.filter(status='COMPLETED').first()

        applicant_data = _build_applicant_data(application)
        # Enrich with payment info for the invoice PDF
        applicant_data['transaction_id'] = completed_transaction.tracking_id
        applicant_data['amount'] = str(completed_transaction.amount)
        applicant_data['payment_date'] = completed_transaction.updated_at.strftime('%d %B %Y, %I:%M %p')

        pdf_buffer = generate_recruitment_pdf(applicant_data)

        return FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename=f"DUITS_Invoice_{application.full_name.replace(' ', '_')}.pdf",
            content_type='application/pdf'
        )