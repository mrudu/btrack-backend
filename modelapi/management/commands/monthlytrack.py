from django.core.management.base import BaseCommand, CommandError
from modelapi.models import *
from django.core.mail import EmailMessage
import datetime
class Command(BaseCommand):
	help = 'Keeps track of the number of projects every month'
	def handle(self, *args, **options):
		track = Track()
		today = datetime.datetime.now()
		track.active = Project.objects.filter(status=0).count()
		track.suspended = Project.objects.filter(status=1).count()
		track.completed = Project.objects.filter(status=2).count()
		track.month = today.strftime("%b")
		track.year = str(today.year)
		track.save()
		self.stdout.write('Successfully recorded Project Status for '+track.month+' '+track.year)
