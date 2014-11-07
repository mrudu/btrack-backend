# Create your views here.
from modelapi.models import *
from django.http import HttpResponse
import csv,datetime,random
from dateutil import relativedelta
from django.core.exceptions import ObjectDoesNotExist

TODAY = datetime.datetime.now()
# View which returns a csv file of the project and respective task dates in the Database.
def backup(request, urltype = ""):
	response = HttpResponse(content_type = 'text/csv')
	response['Content-Disposition'] = 'attachment; filename="backup-'+urltype+'.csv"'
	writer = csv.writer(response)
	projects = Project.objects.all()
	if urltype == "compl":
		projects = projects.filter(status = 2)
	elif urltype == "ong":
		projects = projects.filter(status = 0)
	elif urltype == "fp":
		projects = projects.filter(winprobability__gte=75,status=0)
	elif urltype == "h1p":
		projects = projects.filter(sopDate__year=TODAY.year,status=0)
	elif urltype == "h2p":
		projects = projects.filter(sopDate__year=TODAY.year+1,status=0)
	elif urltype == "h3p":
		projects = projects.filter(sopDate__year__gte=TODAY.year+2,status=0)
	elif urltype == "npp":
		projects = projects.filter(winprobability__lte=10,status = 0)
	elif urltype == "sp":
		projects = projects.filter(status = 1)
	elif urltype == "lagging":
		projects = projects.filter(status = 0,sopDate__lte = TODAY)
	writer.writerow(['Project Title','Customer','Category','Price','Volume','Project Life','Start Of Production','Win Probability','Part Number','Status','Salesman','ENQ','NBO','QUOTE','IPO','PPAP','FPO','FRS'])
	for p in projects:
		row = [p.title, p.customer.name,p.get_product_display(),p.price,p.volume,p.life,p.sopDate.strftime("%d/%m/%Y"),p.winprobability,p.part_no,p.status,p.createdBy.username,'','','','','','','']
		tasks = Task.objects.filter(project = p).order_by('workflow__id')
		count = 11
		for t in tasks:
			if t.end_date != None:
				row[count] = t.end_date.strftime("%d/%m/%Y")
			count += 1
		writer.writerow(row)
	return response

def remarksbackup(request):
	response = HttpResponse(content_type = 'text/csv')
	response['Content-Disposition'] = 'attachment; filename="remarks.csv"'
	writer = csv.writer(response)
	writer.writerow(['Refernce No','Project title','Customer','Remark','Date'])
	remarks = Remark.objects.all()
	for r in remarks:
		row = [r.project.reference,r.project.title,r.project.customer.name,r.content,r.created_on]
		writer.writerow(row)
	return response

# View for population of project details into the database [Run this first and then run /taskcreate]. URL: /dbcreate
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
		p.winprobability = int(float(row[4])*100)
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
		elif p.status == 3:
			p.late_status = 5
		p.generated = 'S'
		p.pop = 'Bho'
		p.life=5
		p.description = "Actual Data"
		u1 = User.objects.get_or_create(username="ZGI",first_name="Zaheed",last_name="Inamdar",email="zginamdar@divgi-warner.com")
		u1 = User.objects.get_or_create(username="DMJ",first_name="Digvijay",last_name="Jadhav",email="dmjadhav@divgi-warner.com")
		u1 = User.objects.get_or_create(username="TJS",first_name="Tushar",last_name="Sawant",email="tjsawant@divgi-warner.com")
		r = random.randrange(1,4)
		p.createdBy = User.objects.get(pk=r)
		p.save()
		print p
		opc = OppProChe.objects.get_or_create(project=p)
	return HttpResponse(str(Project.objects.all().values('title'))+ '<br>'+str(Project.objects.all().count()))

# View for population of tasks into the database. [Run this after running /dbcreate] URL:/taskcreate
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
