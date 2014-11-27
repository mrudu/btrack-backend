from django.core.management.base import BaseCommand, CommandError
from modelapi.models import *
from django.core.mail import EmailMessage
import datetime
class Command(BaseCommand):
	help = 'Checks mail'
	def handle(self, *args, **options):
		projects = Project.objects.filter(status = 0)
		count = 0
		today = datetime.datetime.now().date()
		for p in projects:
			latest = p.remark_set.latest('created_on').created_on.date()
			delay = (today-latest).days
			if delay%15 == 0 and delay == 15:
				count += 1
				subject = "ATTENTION: "+p.title
				message = "Note: This mail is system generated. Please do not reply. The Project "+ p.title+" has not been attended to for the last "+delay+" days. Project Owner: "+p.createdBy.first_name
				email = EmailMessage(subject,message,to=[p.createdBy.email])
				email.send()
			elif delay%15 == 0 and delay>15:
				count += 1
				subject = "ATTENTION: "+p.title
				message = "Note: This mail is system generated. Please do not reply. The Project "+ p.title+" has not been attended to for the last "+str(delay)+" days. Project Owner: "+p.createdBy.first_name
				email = EmailMessage(subject,message,to=[p.createdBy.email,'amkoppikar@divgi-warner.com'])
				email.send()
		self.stdout.write('Successfully sent mail for '+str(count))
