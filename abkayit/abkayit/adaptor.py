# -*- coding: utf-8 -*-

from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_email(subject_template, content_template, content_text, data, from_email, to_addresses):
	subject = render_to_string(subject_template, data).strip()
	html_content = render_to_string(content_template, data).strip()
	text_content = render_to_string(content_text, data).strip()

	#msg = EmailMultiAlternatives(subject, text_content, from_email, to_addresses)
	msg = EmailMessage(subject, html_content, from_email, to_addresses)
	msg.content_subtype = "html"
	#msg.attach_alternative(html_content, "text/html")
	try:
		msg.send()
	except:
		pass
