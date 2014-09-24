# Create your views here.
from django.http import HttpResponse
from modelapi.models import Project, Task, Workflow, Customer, User, OppProChe
import json, csv, datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

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
	csvfile = open('projectdata1.csv','rb')
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
		elif "ACE" in row[6]:
			p.product = 'ACE'
		elif "Nextrac/ PTU" in row[6]:
			p.product = 'PTU'
		elif "Synchronizers" in row[6]:
			p.product = 'Synchro'
		elif "WTC" in row[6]:
			p.product = 'WTC'
		else:
			p.product = 'Oth'
		print p.product
		print row[6]
		p.part_no = row[7]
		p.status = int(row[8])
		if p.status == 1:
			p.late_status = 4
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
	delay = datetime.timedelta(days=365)
	csvfile = open('taskdata.csv','rb')
	x = []
	reader = csv.reader(csvfile)
	for row in reader:
		x.append(row)
	for row in x:
		project = Project.objects.get(title=row[0])
		if row[1] == "":
			continue
		dae = row[1].split("/")
		enq = datetime.datetime(int(dae[2]),int(dae[0]),int(dae[1]))
		enqp = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=1),start_date=(enq-datetime.timedelta(days=7)),end_date=enq,description="stage",remarks="To be verified.",due_date=enq)
		if row[2] == "":
			nbo = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=2),due_date=(enq+delay),start_date=enq,description="stage",remarks="To be verified.")
			continue
		dae = row[2].split("/")
		nbo = datetime.datetime(int(dae[2]),int(dae[0]),int(dae[1]))
		nbop = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=2),end_date=nbo,due_date=nbo,start_date=enq,description="stage",remarks="NBO Appproved.Work on Quote begun")
		if row[3] == "":
			quotep = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=3),start_date=nbo,due_date=(nbo+delay),description="stage",remarks="Final Quote yet to be submitted.")
			continue
		dae = row[3].split("/")
		quote = dae[2]+'-'+dae[0]+'-'+dae[1]
		quote = datetime.datetime(int(dae[2]),int(dae[0]),int(dae[1]))
		quotep = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=3),start_date=nbo,end_date=quote,due_date=quote,description="stage",remarks="Final Quote submitted. Waiting for Initial Purchase Order.")
		if row[4] == "":
			ipop = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=4),start_date=quote,due_date=(quote+delay),description="milestone",remarks="Initial Purchase Order not recieved.")
			continue
		dae = row[4].split("/")
		ipo = datetime.datetime(int(dae[2]),int(dae[0]),int(dae[1]))
		ipop = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=4),start_date=quote,end_date=ipo,due_date=ipo,description="milestone",remarks="Initial Purchase Order Recieved. Work on PPAP has begun.")
		if row[5] == "":
			ppapp = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=5),start_date=ipo,due_date=(ipo+delay),description="stage",remarks="PPAP not yet submitted.")
			continue
		if row[6] == "":
			ppapp = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=5),start_date=ipo,due_date=(ipo+delay),description="stage",remarks="PPAP submitted on "+row[5]+". Waiting for Approval.")
			continue
		dae = row[6].split("/")
		ppap_end = datetime.datetime(int(dae[2]),int(dae[0]),int(dae[1]))
		ppapp = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=5),start_date=ipo,end_date=ppap_end,due_date=ppap_end,description="stage",remarks="PPAP Approved. Waiting for Final Purchase Order.")
		if row[7] == "":
			fpop = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=6),start_date=ppap_end,due_date=(ppap_end+delay),description="milestone",remarks="Final Purchase Order not Recieved.")
			continue
		dae = row[7].split("/")
		fpo = datetime.datetime(int(dae[2]),int(dae[0]),int(dae[1]))
		fpop = Task.objects.create(project=project,workflow=Workflow.objects.get(pk=6),start_date=ppap_end,end_date=fpo,due_date=fpo,description="milestone",remarks="Final Purchase Order Recieved. Production has started.")
		if row[8] == "":
			frsp = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=7),start_date=fpo,due_date=(fpo_end+delay),description="milestone",remarks="First Shipment is yet to happen.")
			continue
		dae = row[8].split("/")
		frs = datetime.datetime(int(dae[2]),int(dae[0]),int(dae[1]))
		frsp = Task.objects.create(project=project,workflow =Workflow.objects.get(pk=7),start_date=fpo,end_date=frs,due_date=frs,description="milestone",remarks="FRS has happened. Project has been completed.")
		project.status = 2
		project.save()
	return HttpResponse(str(x))

def statusUpdate(request):
	today = datetime.datetime.now()
	projects = Project.objects.filter(tasks__end_date__isnull=True).exclude(late_status=4).distinct()
	for p in projects:
		t = p.tasks.get(end_date__isnull=True)
		if t.due_date <= today-datetime.timedelta(days=1):
			p.late_status = 3
		elif t.due_date <= today:
			p.late_status = 2
		elif t.due_date <=today+datetime.timedelta(days=7):
			p.late_status = 1
		else:
			p.late_status = 0
		p.save()
	p4 = Project.objects.filter(tasks__end_date__isnull=False).exclude(id__in=projects.values('id')).exclude(late_status=4)
	p4.update(late_status=0)
	return HttpResponse("200")

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
