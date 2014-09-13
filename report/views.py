# Create your views here.
from django.http import HttpResponse
from modelapi.models import Project, Task, Workflow, Customer, User, OppProChe
import json, csv, datetime
from django.core.exceptions import ObjectDoesNotExist

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

def createdb(request):
	w = Workflow.objects.get_or_create(name="RFQ/ENQ",stage=1,description="Request for Quote/Enquiry")
	w = Workflow.objects.get_or_create(name="NBO",stage=2,description="New Business Opportunity")
	w = Workflow.objects.get_or_create(name="QUOTE",stage=3,description="Quotation submitted to Customer")
	w = Workflow.objects.get_or_create(name="IPO",stage=4,description="Initial Purchase Order")
	w = Workflow.objects.get_or_create(name="PPAP",stage=5,description="Part Production Approval Process")
	w = Workflow.objects.get_or_create(name="FPO",stage=6,description="Final Purchase Order")
	w = Workflow.objects.get_or_create(name="FRS",stage=7,description="First Revenue Shipment")
	csvfile = open('projectdata.csv','rb')
	x = []
	reader = csv.reader(csvfile)
	for row in reader:
		x.append(row)
	print x
	for row in x:
		p = Project()
		customer = Customer.objects.get_or_create(name = row[0])
		p.customer = Customer.objects.get(name=row[0])
		p.title = row[1]
		p.price = row[2]
		p.volume = row[3]
		try:
			p.volume = int(p.volume)
		except:
			p.volume = 0
		try:
			p.price = int(float(p.price))
		except:
			try:
				p.price = int(p.price)
			except:
				p.price = 0
		p.winprobability = row[4]
		sopDate = row[5]
		dae = sopDate.split("/")
		p.sopDate = dae[2]+'-'+dae[0]+'-'+dae[1]
		if row[6] == "Next Gen Platforms/ Transfer Cases":
			p.product = 'NTC'
		elif "Components (Exports/ Domestic)" in row[6]:
			p.product = 'Comp'
		elif "WTC" in row[6]:
			p.product = 'WTC'
		else:
			p.product = 'Oth'
		print p.product
		print row[6]
		p.part_no = row[7]
		p.priority = 3
		p.pop = 'Bho'
		p.life=5
		p.description = "Actual Data"
		p.createdBy = User.objects.get(pk=1)
		p.save()
		print p
		opc = OppProChe.objects.get_or_create(project=p)
	return HttpResponse(str(Project.objects.all().values('title'))+ '<br>'+str(Project.objects.all().count()))

def tasksave(request):
	csvfile = open('taskdata.csv','rb')
	x = []
	reader = csv.reader(csvfile)
	for row in reader:
		x.append(row)
	for row in x:
		project = Project.objects.get(part_no=row[0])
		if row[1] == "":
			continue
		dae = row[1].split("/")
		enq = dae[2]+'-'+dae[0]+'-'+dae[1]
		enq = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=1),start_date=enq,end_date=enq,due_date=enq,description="actualdata",remarks="actualdata")
		if row[2] == "":
			continue
		dae = row[2].split("/")
		nbo = dae[2]+'-'+dae[0]+'-'+dae[1]
		nbo = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=2),start_date=nbo,end_date=nbo,due_date=nbo,description="actualdata",remarks="actualdata")
		if row[3] == "":
			continue
		dae = row[3].split("/")
		quote = dae[2]+'-'+dae[0]+'-'+dae[1]
		enq = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=3),start_date=quote,end_date=quote,due_date=quote,description="actualdata",remarks="actualdata")
		if row[4] == "":
			continue
		dae = row[4].split("/")
		ipo = dae[2]+'-'+dae[0]+'-'+dae[1]
		enq = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=4),start_date=ipo,end_date=ipo,due_date=ipo,description="actualdata",remarks="actualdata")
		if row[5] == "":
			continue
		dae = row[5].split("/")
		ppap_start = dae[2]+'-'+dae[0]+'-'+dae[1]
		if row[6] == "":
			ppap_end = datetime.datetime.now()
			enq = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=5),start_date=ppap_start,end_date=ppap_end,due_date=ppap_end,description="actualdata",remarks="actualdata")
			continue
		dae = row[6].split("/")
		ppap_end = dae[2]+'-'+dae[0]+'-'+dae[1]
		enq = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=5),start_date=ppap_start,end_date=ppap_end,due_date=ppap_end,description="actualdata",remarks="actualdata")
		if row[7] == "":
			continue
		dae = row[7].split("/")
		fpo = dae[2]+'-'+dae[0]+'-'+dae[1]
		enq = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=6),start_date=fpo,end_date=fpo,due_date=fpo,description="actualdata",remarks="actualdata")
		if row[8] == "":
			continue
		dae = row[8].split("/")
		frs = dae[2]+'-'+dae[0]+'-'+dae[1]
		enq = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=7),start_date=frs,end_date=frs,due_date=frs,description="actualdata",remarks="actualdata")
	return HttpResponse(str(x))

def statusUpdate(request):
	today = datetime.datetime.now()
	p = Project.objects.all().distinct()
	p.update(late_status=0)
	p = Project.objects.filter(tasks__end_date__isnull=True, tasks__due_date__lte=(today+datetime.timedelta(days=7))).distinct()
	p.update(late_status=1)
	p = Project.objects.filter(tasks__end_date__isnull=True, tasks__due_date__lte=today).distinct()
	p.update(late_status=2)
	p = Project.objects.filter(tasks__end_date__isnull=True, tasks__due_date__lt=(today-datetime.timedelta(days=1))).distinct()
	p.update(late_status=3)
	return HttpResponse("200")
