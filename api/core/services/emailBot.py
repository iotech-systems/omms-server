
import ssl
import smtplib
import config.email as conf
from email.message import EmailMessage


class emailBot(object):

   def __init__(self, toAdr: str, frmAdr: str, subject: str, body: str):
      self.toAdr = toAdr
      self.frmAdr = frmAdr
      self.subject = subject
      self.body = body
      self.server = None

   def send(self) -> bool:
      try:
         context = ssl.create_default_context()
         self.server = smtplib.SMTP(conf.emailConfig.smtpHostOrIP, conf.emailConfig.smtpPort)
         self.server.ehlo()
         self.server.starttls(context=context)
         self.server.login(conf.emailConfig.smtpUser, conf.emailConfig.smtpPwd)
         # send here
         self.__send__()
         return True
      except Exception as e:
         print(f"\n\tSend Email Error: {e}")
         return False
      finally:
         self.server.quit()

   def __send__(self):
      em: EmailMessage = EmailMessage()
      em.add_header("Content-Type", "application/json")
      em.add_header("Subject", self.subject)
      em.add_header("From", self.frmAdr)
      em.add_header("To", self.toAdr)
      em.set_content(self.body)
      self.server.send_message(em)
