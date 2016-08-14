from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist

from pt.forms import ProjectForm, NepaForm, AirForm, NoiseForm, EcologyForm, AquaticsForm, ArchaeologyForm, HistoryForm
from pt.models import Project, Nepa, ProjectNumbers, PINumbers
from pt.utils import initial_form_lookup, form_lookup, blank_form_lookup

@login_required()
def home_page(request):	
	if request.method == 'GET':
		# project_list = Project.objects.all()
		project_list = Project.objects.order_by('row_auth')
	elif request.method == 'POST':		
		try:
			"""Dirty hack to handle post redirect from add_page :-/ """
			project_list = Project.objects.filter(projectmanager=request.POST['pm'])
		except:
			project_list = Project.objects.all()
	context = {'project_list' : project_list}
	template = loader.get_template('pt/home.html')
	return HttpResponse(template.render(context))

@login_required
def add_page(request):
	if request.method == 'POST':
		project_form = ProjectForm(request.POST)
		if project_form.is_valid():
			project_data = project_form.cleaned_data
			project = Project()
			project.jobnumber = project_data['jobnumber']
			project.projectname = project_data['projectname']
			project.projectmanager = project_data['projectmanager']
			project.projectdescription = project_data['projectdescription']
			project.county = project_data['county']
			project.comments = project_data['comments']
			project.save() ##Need to save project object before adding PIs and PNs
			for num in project_data['pinumber'].split(','):
				pi = PINumbers.objects.get_or_create(pi_number=num)[0]					
				project.pis.add(pi)
			for num in project_data['projectnumber'].split(','):
				pn = ProjectNumbers.objects.get_or_create(project_number=num)[0]					
				project.projectnumbers.add(pn)
			blank_request = HttpRequest()
			blank_request.method = 'GET'
			return redirect(home_page)
		else:
			## need to fix error checking			
			return render(request, 'pt/add_project.html', {'project_form' : project_form})
	else:
		return render(request, 'pt/add_project.html', {'project_form' : ProjectForm })

@login_required
def project_dash(request, projectid):
	project = get_object_or_404(Project, id=projectid)

	context = { 
				'project': project,				
			}
	return render(request, 'pt/projectdash.html', context)

@login_required
def pi_dash(request, projectid):
	project = get_object_or_404(Project, id=projectid)
	project_list = Project.objects.filter(pis__projects=project)
	context = { 
				'project_list': set(project_list),	
			}
	return render(request, 'pt/home.html', context)

@login_required
def pns_dash(request, projectid):
	project = get_object_or_404(Project, id=projectid)
	project_list = Project.objects.filter(projectnumbers__projects=project)
	context = { 
				'project_list': set(project_list),	
			}
	return render(request, 'pt/home.html', context)

@login_required
def nepa_dash(request, projectid, nepaid):
	project = get_object_or_404(Project, id=projectid)
	nepa = project.nepa_set.all().get(id=nepaid)
	context = { 
				'project' : project,
				'nepa': nepa,				
			}
	return render(request, 'pt/nepadash.html', context)

@login_required
def air_dash(request, projectid, airid):
	project = get_object_or_404(Project, id=projectid)
	air = project.air_set.all().get(id=airid)
	context = { 
				'project' : project,
				'air': air,				
			}
	return render(request, 'pt/airdash.html', context)

@login_required
def noise_dash(request, projectid, noiseid):
	project = get_object_or_404(Project, id=projectid)
	noise = project.noise_set.all().get(id=noiseid)
	context = { 
				'project' : project,
				'noise': noise,				
			}
	return render(request, 'pt/noisedash.html', context)

@login_required
def ecology_dash(request, projectid, ecologyid):
	project = get_object_or_404(Project, id=projectid)
	ecology = project.ecology_set.all().get(id=ecologyid)
	context = { 
				'project' : project,
				'ecology': ecology,				
			}
	return render(request, 'pt/ecologydash.html', context)

@login_required
def aquatics_dash(request, projectid, aquaticsid):
	project = get_object_or_404(Project, id=projectid)
	aquatics = project.aquatics_set.all().get(id=aquaticsid)
	context = { 
				'project' : project,
				'aquatics': aquatics,				
			}
	return render(request, 'pt/aquaticsdash.html', context)

@login_required
def archaeology_dash(request, projectid, archaeologyid):
	project = get_object_or_404(Project, id=projectid)
	archaeology = project.archaeology_set.all().get(id=archaeologyid)
	context = { 
				'project' : project,
				'archaeology': archaeology,				
			}
	return render(request, 'pt/archaeologydash.html', context)

@login_required
def history_dash(request, projectid, historyid):
	project = get_object_or_404(Project, id=projectid)
	history = project.history_set.all().get(id=historyid)
	context = { 
				'project' : project,
				'history': history,				
			}
	return render(request, 'pt/historydash.html', context)
	
@login_required
def project_edit(request, projectid):
	''' Should only come from project edit page, so nepa should update automagically '''
	project = get_object_or_404(Project, id=projectid)
	if request.method == 'POST':
		if request.POST.get('delete'):
			project.delete()
			blank_request = HttpRequest()
			blank_request.method = 'GET'
			return redirect(home_page)
		project_form = ProjectForm(request.POST, instance=project)
		attached_pis = [i.pi_number for i in project.pis.all()]
		attached_pns = [pn.project_number for pn in project.projectnumbers.all()]
		# return HttpResponse('<html>{}</html>'.format(attached_pns))
		if project_form.is_valid():
			clean = project_form.cleaned_data
			# if not clean['pinumber']=='':
			for num in attached_pis:
				pi = PINumbers.objects.get(pi_number=num)
				project.pis.remove(pi)
			for num in clean['pinumber'].split(','):
				pi = PINumbers.objects.get_or_create(pi_number=num)[0]					
				project.pis.add(pi)
			for num in attached_pns:
				pn = ProjectNumbers.objects.get(project_number=num)
				project.projectnumbers.remove(pn)
			for num in clean['projectnumber'].split(','):
				pn = ProjectNumbers.objects.get_or_create(project_number=num)[0]					
				project.projectnumbers.add(pn)
			##add PI and PN cleanup, check for orphans
			# return HttpResponse('<html>{}</html>'.format(pi))
			project_form.save() #save and commit job number to db			
			return redirect('pt/project_dash', projectid=project.id)
		return render(request, 'pt/add_project.html', {'project_form' : project_form})
	else:		
		project_form = ProjectForm(instance=project)
		return render(request, 'pt/add_project.html', {'project_form' : project_form})

@login_required
def nepa_edit(request, projectid, nepaid):
	project = get_object_or_404(Project, id=projectid)
	nepa = project.nepa_set.all().get(id=nepaid)
	if request.method == 'POST':
		if request.POST.get('delete'):
			nepa.delete()
			blank_request = HttpRequest()
			blank_request.method = 'GET'
			blank_request.user = request.user
			return redirect('project_dash', projectid)
		form = NepaForm(request.POST, instance=nepa)
		if form.is_valid():
			##fix nepa project change functionality
			form.save() #save and commit job number to db			
			return redirect('nepa_dash', projectid=project.id, nepaid=nepa.id)
		return render(request, 'pt/add_document.html', {'form':form})
	else:		
		form = NepaForm(instance=nepa)
		return render(request, 'pt/add_document.html', {'form':form})

@login_required
def nepa_add(request, projectid):
	project = get_object_or_404(Project, id=projectid)
	if request.method == 'POST':
		form = NepaForm(request.POST)
		if form.is_valid():
			##fix nepa project change functionality
			form.save() #save and commit job number to db			
			return redirect('project_dash', projectid=project.id)
		return render(request, 'pt/add_document.html', {'form':form})
	else:
		form = NepaForm(initial={'project':project})	
		return render(request, 'pt/add_document.html', {'form':form, 'project':project})

@login_required
def ss_add(request, projectid, ss_type, form_type):
	project = get_object_or_404(Project, id=projectid)
	if request.method == 'POST':
		form = form_lookup(request, form_type)
		if form.is_valid():
			##fix nepa project change functionality
			form.save() #save and commit job number to db			
			return redirect('project_dash', projectid=project.id)
		return render(request, 'pt/add_document.html', {'form':form})
	else:
		# form = AirForm(initial={'project':project})
		form = initial_form_lookup(ss_type, project)
		return render(request, 'pt/add_document.html', {'form':form, 'project':project})

@login_required
def ss_edit(request, projectid, ssid, ss_type, form_type):
	##clean this function up
	def ss_lookup(ssid, ss_type, parent_project):	
		try:
			air = parent_project.air_set.all().get(id=ssid)
		except ObjectDoesNotExist:
			air = ''	
		try:
			noise = parent_project.noise_set.all().get(id=ssid)
		except ObjectDoesNotExist:
			noise = ''
		try:
			ecology = parent_project.ecology_set.all().get(id=ssid)
		except ObjectDoesNotExist:
			ecology = ''
		try:
			aquatics = parent_project.aquatics_set.all().get(id=ssid)
		except ObjectDoesNotExist:
			aquatics = ''
		try:
			archaeology = parent_project.archaeology_set.all().get(id=ssid)
		except ObjectDoesNotExist:
			archaeology = ''
		try:
			history = parent_project.history_set.all().get(id=ssid)
		except ObjectDoesNotExist:
			history = ''
		ss_dict = {
		'air' : air,
		'noise' : noise,
		'ecology': ecology,
		'aquatics': aquatics,
		'archaeology': archaeology,
		'history': history,
		}
		return ss_dict[ss_type]
		
	project = get_object_or_404(Project, id=projectid)
	special_study = ss_lookup(ssid, ss_type, project)
	# air = project.air_set.all().get(id=ssid)
	if request.method == 'POST':
		if request.POST.get('delete'):
			special_study.delete()
			request.method = 'GET'
			return redirect('project_dash', projectid)
		# form = AirForm(request.POST, instance=air)
		form = form_lookup(request, form_type, special_study)
		# return form
		if form.is_valid():
			##fix air project change functionality
			form.save() ##save and commit job number to db
			return redirect('{}_dash'.format(ss_type), project.id, ssid)
		return render(request, 'pt/add_document.html', {'form':form})
	else:
		##also ugly - fix
		form = blank_form_lookup(ss_type, special_study)
		return render(request, 'pt/add_document.html', {'form':form})