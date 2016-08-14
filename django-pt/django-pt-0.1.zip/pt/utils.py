from pt.forms import ProjectForm, NepaForm, AirForm, NoiseForm, EcologyForm, AquaticsForm, ArchaeologyForm, HistoryForm

def initial_form_lookup(ss_type, project_from_db):
	try:
		air = AirForm(initial={'project': project_from_db})
	except:
		air = ''
	try:
		noise = NoiseForm(initial={'project' : project_from_db})
	except:
		noise = ''
	try:
		ecology = EcologyForm(initial={'project' : project_from_db})
	except:
		ecology = ''
	try:
		aquatics = AquaticsForm(initial={'project' : project_from_db})
	except:
		aquatics = ''
	try:
		archaeology = ArchaeologyForm(initial={'project' : project_from_db})
	except:
		archaeology = ''
	try:
		history = HistoryForm(initial={'project' : project_from_db})
	except:
		history = ''
	form_dict = {
		'air' : air,
		'noise' : noise,
		'ecology': ecology,
		'aquatics': aquatics,
		'archaeology': archaeology,
		'history': history,
	}
	return form_dict[ss_type]

def form_lookup(request, form_from_url, instance=None):
	form_dict = {
	'airform': AirForm(request.POST),
	'noiseform': NoiseForm(request.POST),
	'archform': ArchaeologyForm(request.POST),
	'ecoform': EcologyForm(request.POST),
	'aquaform': AquaticsForm(request.POST),
	'histform': HistoryForm(request.POST),
	}
	##with instance
	inst_dict = {
	'airform': AirForm(request.POST, instance=instance),
	'noiseform': NoiseForm(request.POST, instance=instance),
	'archform': ArchaeologyForm(request.POST, instance=instance),
	'ecoform': EcologyForm(request.POST, instance=instance),
	'aquaform': AquaticsForm(request.POST, instance=instance),
	'histform': HistoryForm(request.POST, instance=instance),
	}
	if instance:
		return inst_dict[form_from_url]
	return form_dict[form_from_url]

def blank_form_lookup(ss_type, special_study):
	try:
		air = AirForm(instance=special_study)
	except:
		air = ''
	try:
		noise = NoiseForm(instance=special_study)
	except:
		noise = ''
	try:
		ecology = EcologyForm(instance=special_study)
	except:
		ecology = ''
	try:
		aquatics = AquaticsForm(instance=special_study)
	except:
		aquatics = ''
	try:
		archaeology = ArchaeologyForm(instance=special_study)
	except:
		archaeology = ''
	try:
		history = HistoryForm(instance=special_study)
	except:
		history = ''
	form_dict = {
		'air' : air,
		'noise' : noise,
		'ecology': ecology,
		'aquatics': aquatics,
		'archaeology': archaeology,
		'history': history,
	}
	return form_dict[ss_type]