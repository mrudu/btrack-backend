from django.core.management.base import BaseCommand, CommandError
from modelapi.models import *
import datetime

class Command(BaseCommand):
	help = 'Deletes Suspended Projects after six months'
	def handle(self, *args, **options):
		sixmonthsago = datetime.datetime.now()-datetime.timedelta(days=180)
		projects = Project.objects.filter(status=1,edit_date__lte=str(sixmonthsago.year)+'-'+str(sixmonthsago.month)+'-'+str(sixmonthsago.day))
		projects.delete()
		self.stdout.write('Deleted '+str(projects.count())+' suspended projects')
