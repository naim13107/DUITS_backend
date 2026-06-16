# email_services.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_html_email(subject, template_name, context, to_email_list, pdf_buffer=None, pdf_filename="Document.pdf"):
    """
    Sends a beautifully rendered HTML email, with an optional PDF attachment.
    """
    # 1. Render the HTML using the context variables
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content) 
    
    # 2. Build the email package
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_email_list
    )
    
    # 3. Attach the HTML as the visual body
    email.attach_alternative(html_content, "text/html")
    
    # 4. Attach the PDF file if one was provided
    if pdf_buffer:
        # Read the raw bytes from the buffer
        pdf_content = pdf_buffer.getvalue()
        # Attach it to the email (Filename, Data, MIME-Type)
        email.attach(pdf_filename, pdf_content, 'application/pdf')
        # Close the buffer to free up server memory
        pdf_buffer.close()
    
    # 5. Send the email
    return email.send(fail_silently=False)