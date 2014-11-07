# Create your views here.
from django.http import HttpResponse
from modelapi.models import Project, Task, Workflow, Customer, User, OppProChe
import json, csv, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.core.mail import send_mail

# View for the Salesman Matrix Page. URL:/api/v1/salesmanmatrix
def usermatrix(request):
	data = {}
	u = User.objects.all()
	p = Project.objects.all()
	for x in u:
		total = p.filter(createdBy=x)
		completed = total.filter(status = 2).count()
		active = total.filter(status = 0).count()
		suspended = total.count()-(completed + active)
		tc = total.filter(product="NTC").count()
		syn = total.filter(product="Synchro").count()
		ptu = total.filter(product="PTU").count()
		comp = total.filter(product="Comp").count()
		ace = total.filter(product="ACE").count()
		wtc = total.filter(product="WTC").count()
		oth = total.filter(product="Oth").count()
		data[x.id] = {'name':x.first_name,'username':x.username,'id':x.id,'tot':total.count(),'com':completed,'sus':suspended,'act':active,'tc':tc,'syn':syn,'ptu':ptu,'comp':comp,'ace':ace,'wtc':wtc,'oth':oth}
	return HttpResponse(json.dumps(data), content_type="application/json")

# View for the Dashboard page. URL:/api/v1/dashboard
def dashboard(request):
	data = {}
	data['active'] = Project.objects.filter(status=0).count()
	data['suspended'] = Project.objects.filter(status=1).count()
	data['completed'] = Project.objects.filter(status=2).count()
	enq= Workflow.objects.get(id=1)
	nbo= Workflow.objects.get(id=2)
	quo= Workflow.objects.get(id=3)
	ipo= Workflow.objects.get(id=4)
	ppap= Workflow.objects.get(id=5)
	fpo= Workflow.objects.get(id=6)
	frs= Workflow.objects.get(id=7)
	data['enq'] = Task.objects.filter(workflow=enq).count()
	data['nbo'] = Task.objects.filter(workflow=nbo).count()
	data['quo'] = Task.objects.filter(workflow=quo).count()
	data['ipo'] = Task.objects.filter(workflow=ipo).count()
	data['ppap'] = Task.objects.filter(workflow=ppap).count()
	data['fpo'] = Task.objects.filter(workflow=fpo).count()
	data['frs'] = Task.objects.filter(workflow=frs).count()
	data['tc'] = Project.objects.filter(product="NTC").count()
	data['syn'] = Project.objects.filter(product="Synchro").count()
	data['ptu'] = Project.objects.filter(product="PTU").count()
	data['comp'] = Project.objects.filter(product="Comp").count()
	data['ace'] = Project.objects.filter(product="ACE").count()
	data['wtc'] = Project.objects.filter(product="WTC").count()
	data['oth'] = Project.objects.filter(product="Oth").count()
	return HttpResponse(json.dumps(data), content_type="application/json")

# View for updation of status of Projects. URL:/api/v1/statusupdate
def statusUpdate(request):
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
	return HttpResponse("200")

# View which returns the revenue per Product Category. URL :/api/v1/cpc
def categoryPieChart(request):
	data = {}
	tot = Project.objects.all().aggregate(Sum('tot_revenue'))['tot_revenue__sum']
	data['ntc'] = Project.objects.filter(product="NTC").aggregate(Sum('tot_revenue'))['tot_revenue__sum']*100/tot
	data['wtc'] = Project.objects.filter(product="WTC").aggregate(Sum('tot_revenue'))['tot_revenue__sum']*100/tot
	data['ace'] = Project.objects.filter(product="ACE").aggregate(Sum('tot_revenue'))['tot_revenue__sum']*100/tot
	data['ptu'] = Project.objects.filter(product="PTU").aggregate(Sum('tot_revenue'))['tot_revenue__sum']*100/tot
	data['syn'] = Project.objects.filter(product="Synchro").aggregate(Sum('tot_revenue'))['tot_revenue__sum']*100/tot
	data['com'] = Project.objects.filter(product="Comp").aggregate(Sum('tot_revenue'))['tot_revenue__sum']*100/tot
	return HttpResponse(json.dumps(data), content_type="application/json")

# Updates the number of days the project is delayed by. URL:/api/v1/progressupdate
def progressUpdate(request):
	projects = Project.objects.all()
	for p in projects:
		count = 0
		for t in p.tasks.all():
			if t.end_date:
				if t.end_date>t.due_date:
					count += (t.end_date-t.due_date).days()
			elif t.due_date<datetime.datetime.now():
				count += (datetime.datetime.now()-t.due_date).days()
		p.progress = count
		p.save()

def mailupdate(request):
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
			send_mail(subject,message,"abd@divgi-warner.com",[p.createdBy.email],fail_silently=False)
		elif delay%15 == 0 and delay>15:
			count += 1
			subject = "ATTENTION: "+p.title
			message = "Note: This mail is system generated. Please do not reply. The Project "+ p.title+" has not been attended to for the last "+str(delay)+" days. Project Owner: "+p.createdBy.first_name
			send_mail(subject,message,"abd@divgi-warner.com",[p.createdBy.email,'amkoppikar@divgi-warner.com'],fail_silently=False)
	return HttpResponse(str(count))
