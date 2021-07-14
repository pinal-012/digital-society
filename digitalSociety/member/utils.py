from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def sendOtpMail(subject,template,to,context):
    template_str = 'chairman/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'pinalaaaa@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendPasswordMail(subject,template,to,context):
    template_str = 'chairman/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'pinalaaaa@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def sendPaymentMail(subject,template,to,context):
    template_str = 'member/'+ template+'.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    from_email = 'pinalaaaa@gmail.com'
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)