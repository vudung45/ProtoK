import smtplib

gmail_user = 'protoktest1@gmail.com'
gmail_password = 'protoktest123'

def send_email(send_to, subject, body):
  email_text = """\
  From: %s
  To: %s
  Subject: %s

  %s
  """ % (gmail_user, send_to, subject, body)
  try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, send_to, email_text)
    server.close()
    print("sent successfully")
  except Exception as e:
    print(e)
