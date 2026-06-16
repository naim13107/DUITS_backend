# payment/views.py
import logging
import requests
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

logger = logging.getLogger(__name__)

from recruitment.models import RecruitmentApplication
from permissions import IsExecutive
from .models import Transaction
from .serializers import TransactionSerializer

FRONTEND_BASE = getattr(settings, 'FRONTEND_BASE_URL', 'https://your-react-frontend.com')


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for the Executive Panel to view the payment ledger.
    """
    queryset = Transaction.objects.all().select_related('application').order_by('-created_at')
    serializer_class = TransactionSerializer
    permission_classes = [IsExecutive]


class PaymentViewSet(viewsets.ViewSet):
    """
    Production-ready aamarPay integration for DUITS.

    ID convention
    ─────────────
    tracking_id   → our 32-char UUID, sent to aamarPay as `tran_id`.
                    aamarPay echoes it back as `mer_txnid` in every callback.
    transaction_id → aamarPay's own gateway ID (`pg_txnid`), stored only
                    after the payment is COMPLETED and verified.
    """
    AAMARPAY_BASE_URL = getattr(settings, 'AAMARPAY_BASE_URL', 'https://sandbox.aamarpay.com')
    AAMARPAY_STORE_ID = getattr(settings, 'AAMARPAY_STORE_ID', 'aamarpaytest')
    AAMARPAY_SIGNATURE_KEY = getattr(settings, 'AAMARPAY_SIGNATURE_KEY', 'dbb74894e82415a2f7ff0ec3a97e4183')

    def get_permissions(self):
        public_actions = {'list', 'initiate', 'payment_success', 'payment_fail', 'payment_cancel'}
        if self.action in public_actions:
            return [permissions.AllowAny()]
        return [IsExecutive()]

    def list(self, request):
        return Response({
            "message": "DUITS aamarPay Gateway Hub",
            "endpoints": {
                "initiate": request.build_absolute_uri('initiate/'),
                "success": request.build_absolute_uri('payment_success/'),
                "fail": request.build_absolute_uri('payment_fail/'),
                "cancel": request.build_absolute_uri('payment_cancel/'),
            }
        })

    @action(detail=False, methods=['post'])
    def initiate(self, request):
        application_id = request.data.get('application_id')
        if not application_id:
            return Response({"error": "application_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            application = RecruitmentApplication.objects.get(id=application_id)
        except RecruitmentApplication.DoesNotExist:
            return Response({"error": "Application not found."}, status=status.HTTP_404_NOT_FOUND)

        transaction = Transaction.objects.create(
            application=application,
            amount=100.00,
            status='PENDING',
        )

        payload = {
            "store_id": self.AAMARPAY_STORE_ID,
            "signature_key": self.AAMARPAY_SIGNATURE_KEY,
            "tran_id": transaction.tracking_id,   # our UUID → aamarPay echoes as mer_txnid
            "amount": "100.00",
            "currency": "BDT",
            "desc": f"Recruitment Payment: {application.full_name}",
            "cus_name": application.full_name,
            "cus_email": application.email,
            "cus_phone": getattr(application, 'phone', '01700000000'),
            "success_url": request.build_absolute_uri('/api/v1/payment/payment_success/'),
            "fail_url": request.build_absolute_uri('/api/v1/payment/payment_fail/'),
            "cancel_url": request.build_absolute_uri('/api/v1/payment/payment_cancel/'),
            "type": "json",
        }

        try:
            resp = requests.post(
                f"{self.AAMARPAY_BASE_URL}/jsonpost.php",
                json=payload,
                timeout=15,
            )
            resp.raise_for_status()
            response_data = resp.json()
        except requests.RequestException as exc:
            transaction.status = 'FAILED'
            transaction.save(update_fields=['status'])
            return Response({"error": "Gateway unreachable.", "detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        if response_data.get('result') == 'true':
            return Response({
                "payment_url": response_data.get('payment_url'),
                "tracking_id": transaction.tracking_id,   # return so frontend can reference it
            })

        transaction.status = 'FAILED'
        transaction.save(update_fields=['status'])
        return Response({"error": "Gateway error.", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'post'])
    def payment_success(self, request):
        # aamarPay POSTs to this URL — always read from request.data first
        data = request.data if request.method == 'POST' else request.query_params

        # Log everything aamarPay sent so we can inspect it
        logger.warning("[aamarPay SUCCESS callback] raw data: %s", dict(data))

        # aamarPay echoes our tran_id as "mer_txnid"
        track_id = data.get('mer_txnid') or data.get('tran_id')

        if not track_id:
            logger.error("[aamarPay] No track_id found in callback data: %s", dict(data))
            return redirect(f"{FRONTEND_BASE}/recruitment/failed")

        # ── Verification call ──────────────────────────────────────────────
        try:
            verify_resp = requests.get(
                f"{self.AAMARPAY_BASE_URL}/api/v1/trxcheck/request.php",
                params={
                    "request_id": track_id,
                    "store_id": self.AAMARPAY_STORE_ID,
                    "signature_key": self.AAMARPAY_SIGNATURE_KEY,
                    "type": "json",
                },
                timeout=15,
            )
            verify_resp.raise_for_status()
            verify_data = verify_resp.json()
        except requests.RequestException as exc:
            logger.error("[aamarPay] Verify request failed for %s: %s", track_id, exc)
            return redirect(f"{FRONTEND_BASE}/recruitment/failed")

        logger.warning("[aamarPay SUCCESS verify] track_id=%s verify_data=%s", track_id, verify_data)

        # aamarPay sandbox sometimes returns "Successful" instead of "COMPLETED"
        gateway_status = verify_data.get('status', '')
        pay_status = verify_data.get('pay_status', '')          # alternate field
        is_success = gateway_status in ('COMPLETED', 'Successful') or pay_status in ('Successful',)

        if is_success:
            transaction = Transaction.objects.filter(tracking_id=track_id).first()
            if not transaction:
                logger.error("[aamarPay] No Transaction found for tracking_id=%s", track_id)
                return redirect(f"{FRONTEND_BASE}/recruitment/failed")

            if transaction.status != 'COMPLETED':
                transaction.transaction_id = verify_data.get('pg_txnid') or None
                transaction.status = 'COMPLETED'
                transaction.save(update_fields=['transaction_id', 'status'])

                # ── Sync application payment fields ───────────────────────
                application = transaction.application
                if application:
                    application.payment_status = 'COMPLETED'
                    application.transaction_id = transaction.transaction_id or transaction.tracking_id
                    application.payment_response = str(verify_data)
                    application.save(update_fields=['payment_status', 'transaction_id', 'payment_response'])

                # ── Send invoice PDF email ─────────────────────────────────
                application = transaction.application
                if application:
                    try:
                        from recruitment.views import _build_applicant_data
                        from pdf_services import generate_recruitment_pdf
                        from email_services import send_html_email

                        applicant_data = _build_applicant_data(application)
                        applicant_data['transaction_id'] = transaction.tracking_id
                        applicant_data['amount'] = str(transaction.amount)
                        applicant_data['payment_date'] = transaction.updated_at.strftime('%d %B %Y, %I:%M %p')

                        pdf_buffer = generate_recruitment_pdf(applicant_data)

                        send_html_email(
                            subject="DUITS Recruitment — Payment Confirmed & Invoice",
                            template_name="emails/payment_confirmed.html",
                            context=applicant_data,
                            to_email_list=[application.email],
                            pdf_buffer=pdf_buffer,
                            pdf_filename=f"DUITS_Invoice_{application.full_name.replace(' ', '_')}.pdf",
                        )
                    except Exception as exc:
                        logger.error("[aamarPay] Invoice email failed for %s: %s", track_id, exc)

            # Pass application id so frontend can offer the invoice download button
            app_id = transaction.application_id or ''
            return redirect(f"{FRONTEND_BASE}/recruitment/success?trx={track_id}&app={app_id}")

        logger.error("[aamarPay] Payment NOT successful. gateway_status=%s verify_data=%s", gateway_status, verify_data)
        return redirect(f"{FRONTEND_BASE}/recruitment/failed")

    @action(detail=False, methods=['get', 'post'])
    def payment_fail(self, request):
        data = request.data if request.method == 'POST' else request.query_params
        track_id = data.get('mer_txnid') or data.get('tran_id')

        if track_id:
            Transaction.objects.filter(tracking_id=track_id, status='PENDING').update(status='FAILED')

        return redirect(f"{FRONTEND_BASE}/recruitment/failed")

    @action(detail=False, methods=['get', 'post'])
    def payment_cancel(self, request):
        data = request.data if request.method == 'POST' else request.query_params
        track_id = data.get('mer_txnid') or data.get('tran_id')

        if track_id:
            Transaction.objects.filter(tracking_id=track_id, status='PENDING').update(status='CANCELLED')

        return redirect(f"{FRONTEND_BASE}/recruitment/cancelled")