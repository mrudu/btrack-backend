from django.core.management.base import BaseCommand, CommandError
from modelapi.models import User,Project,Task
import datetime
class Command(BaseCommand):
	help = 'Status Update'
	def handle(self, *args, **options):
		today = datetime.datetime.now()
		tomor = today + datetime.timedelta(days=1)
		tasks = Task.objects.filter(end_date__isnull=True).exclude(project__status = 1)
		for t in tasks:
			p = Project.objects.get(id=t.project.id)
			if t.due_date.date() <= today.date():
				p.late_status = 3
			elif t.due_date.date() <= tomor.date():
				p.late_status = 2
			elif t.due_date.date() <=(today+datetime.timedelta(days=7)).date():
				p.late_status = 1
			else:
				p.late_status = 0
			p.save()
		self.stdout.write('Status Update is Successful')
