# Create your views here.
from apqp.models import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def postapqpform(request):
	print("hello")
	if request.method == 'POST':
		project = SupplierProject()
		print(request.body);
		data = json.loads(request.body)
		# DWTeam
		dw = data['dwteam']
		project.dwteam = DWTeam.objects.get_or_create(
				vd = Employee.objects.get_or_create(name=dw['vd']['name'],email=dw['vd']['email'],ph=dw['vd']['ph'])[0],
				sta = Employee.objects.get_or_create(name=dw['sta']['name'],email=dw['sta']['email'],ph=dw['sta']['ph'])[0],
				engg = Employee.objects.get_or_create(name=dw['engg']['name'],email=dw['engg']['email'],ph=dw['engg']['ph'])[0],
				mfg = Employee.objects.get_or_create(name=dw['mfg']['name'],email=dw['mfg']['email'],ph=dw['mfg']['ph'])[0],
				gaugesupport = Employee.objects.get_or_create(name=dw['gaugesupport']['name'],email=dw['gaugesupport']['email'],ph=dw['gaugesupport']['ph'])[0],
				quality = Employee.objects.get_or_create(name=dw['quality']['name'],email=dw['quality']['email'],ph=dw['quality']['ph'])[0],
				metallurgist = Employee.objects.get_or_create(name=dw['metallurgist']['name'],email=dw['metallurgist']['email'],ph=dw['metallurgist']['ph'])[0],
				production = Employee.objects.get_or_create(name=dw['production']['name'],email=dw['production']['email'],ph=dw['production']['ph'])[0],
		)[0]
		# SupplierTeam
		dw = data['supteam']
		project.suppteam = SupplierTeam.objects.get_or_create(
				md = Employee.objects.get_or_create(name=dw['md']['name'],email=dw['md']['email'],ph=dw['md']['ph'])[0],
				marketing = Employee.objects.get_or_create(name=dw['marketing']['name'],email=dw['marketing']['email'],ph=dw['marketing']['ph'])[0],
				design = Employee.objects.get_or_create(name=dw['design']['name'],email=dw['design']['email'],ph=dw['design']['ph'])[0],
				projectleader = Employee.objects.get_or_create(name=dw['projectleader']['name'],email=dw['projectleader']['email'],ph=dw['projectleader']['ph'])[0],
			)[0]
		#Supplier
		sup = data['supplier']
		supplier = Supplier.objects.get_or_create(name = sup['name'], category = sup['category'])
		project.supplier = supplier[0]
		project.number = data['number']
		project.name = data['name']
		project.partname = data['partname']
		project.partnumber = data['partnumber']
		project.purpose = data['purpose']
		project.teamfeasibility = True
		project.ponumber = data['ponumber']
		project.status = "Existing"
		if supplier:
			project.status = "New"
			supplier[0].dwteam = project.dwteam
			supplier[0].suppteam = project.suppteam
			supplier[0].save()
		project.save()
	return HttpResponse("200")
