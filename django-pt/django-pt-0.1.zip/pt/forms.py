from django.forms import ModelForm, Textarea, DateInput, Form, TextInput, CharField, ChoiceField
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from pt.models import Project, PINumbers, ProjectNumbers, Nepa, Air, Noise, Ecology, Aquatics, Archaeology, History
import shared


class ProjectForm(ModelForm):
    initial_fields = ('pinumber', 'projectnumber')
    pinumber = forms.CharField(required=False, label='PI Number(s)')
    projectnumber = forms.CharField(required=False, label='Project Number(s)')
    def __init__(self, *args, **kwargs):
      super(ProjectForm, self).__init__(*args, **kwargs)
      try:
        inst_projects = self.instance.projectnumbers.all()
      except:
        inst_projects = []
      try:
        inst_pis = self.instance.pis.all()
      except:
        inst_pis = []
      ##Create initial form values from database values
      csv_project_numbers = [i.project_number for i in inst_projects]
      csv_pi_numbers = [i.pi_number for i in inst_pis]
      self.fields['pinumber'].initial = ','.join(csv_pi_numbers)
      self.fields['projectnumber'].initial = ','.join(csv_project_numbers)
      
    class Meta:
      model = Project
      fields = ['jobnumber', 'projectname', 'client',
                  'projectmanager', 'projectdescription',
                  'county', 'comments', 'env_cert_row', 'env_cert_let',
                  'row_auth', 'let_cert', 'pfpr', 'ffpr']
      widgets = {
                  'jobnumber': Textarea(attrs={'cols': 20, 'rows': 1}),
                  'projectname': Textarea(attrs={'cols': 40, 'rows': 1}),
				          'client': Textarea(attrs={'cols': 40, 'rows': 1}),
                  'projectdescription': Textarea(attrs={'cols': 50, 'rows': 3}),
                  'comments': Textarea(attrs={'cols': 50, 'rows': 3}),
                  'env_cert_row': DateInput(attrs={'class':'datepicker'}),
                  'env_cert_let': DateInput(attrs={'class':'datepicker'}),
                  'row_auth': DateInput(attrs={'class':'datepicker'}),
                  'let_cert': DateInput(attrs={'class':'datepicker'}),
                  'pfpr': DateInput(attrs={'class':'datepicker'}),
                  'ffpr': DateInput(attrs={'class':'datepicker'}),
                 }
      help_texts = {
                  'jobnumber': 'Assigned billing number for project',
                  'projectname': 'Project title (i.e., Short Desc from TPRO)',
                  'client': 'Prime consultant or client',
                  'projectmanager': 'EP project manager',
                  'projectdescription': 'Brief project description',                  
                  'county': 'Primary county',
                  'comments': 'Project-specific comments or helpful notes',
                  'env_cert_row': '',
                  'env_cert_let': '',
                  'row_auth': '',
                  'let_cert': '',
                  'pfpr': '',
                  'ffpr': '',
              }
                 
      labels = {
            'jobnumber': _('Job Number'),
      			'projectname': _('Project Name'),
      			'projectmanager': _('Project Manager'),
      			'projectdescription': _('Project Description'),
            'env_cert_row': _('Environmental Certification ROW'),
            'env_cert_let': _('Environmental Certification LET'),
            'row_auth': _('ROW Authorization'),
            'let_cert': _('LET Certification'),
            'pfpr': _('Preliminary FPR'),
            'ffpr': _('Final FPR'),
        }

class NepaForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super(NepaForm, self).__init__(*args, **kwargs)
    self.name = 'Environmental Document'
    # self.fields['specialist'].choices = NEPA_PLANNERS
  class Meta:          
    model = Nepa
    fields = ['project', 'specialist', 
                  'stateplanner', 'documenttype',                  
                  'statedraftdue', 'fhwadraftdue',
				          'earlycoordination', 'statedraft',
                  'stateapproval', 'fhwadraft',
                  'fhwaapproval', 'comments']
    widgets = {
        'earlycoordination': DateInput(attrs={'class':'datepicker'}),
				'statedraft': DateInput(attrs={'class':'datepicker'}),
				'statedraftdue': DateInput(attrs={'class':'datepicker'}),
				'fhwadraftdue': DateInput(attrs={'class':'datepicker'}),
				'stateapproval': DateInput(attrs={'class':'datepicker'}),
				'fhwadraft': DateInput(attrs={'class':'datepicker'}),
				'fhwaapproval': DateInput(attrs={'class':'datepicker'}),
        'comments': Textarea(attrs={'cols': 50, 'rows': 3}),
        }
    labels = {
			'stateplanner':_('State Planner'),
      'earlycoordination': _('Early Coordination On'),
      'documenttype': _('Document Type'),
			'statedraft': _('State Draft Submitted On'),
			'statedraftdue': _('State Draft Due'),
			'fhwadraftdue': _('FHWA Draft Due'),
			'stateapproval': _('State Approval'),
			'fhwadraft': _('FHWA Draft Submitted On'),
			'fhwaapproval': _('FHWA Approval'),
        }

class AirForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super(AirForm, self).__init__(*args, **kwargs)
    self.name = 'Air Document'
    self.fields['documenttype'] = ChoiceField(choices=shared.AIR_DOCUMENTS)
  class Meta:
    model = Air
    fields = ['project', 'documenttype', 'title', 'specialist', 'gdot_specialist', 'draftsubmittal', 
              'draftapproval', 'duedate', 'comments']
    widgets = {
        'draftsubmittal': DateInput(attrs={'class':'datepicker'}),
        'draftapproval': DateInput(attrs={'class':'datepicker'}),
        'duedate': DateInput(attrs={'class':'datepicker'}),
        'comments': Textarea(attrs={'cols': 50, 'rows': 3}),
        }

    labels = {
      'draftsubmittal':_('Draft Submittal'),
      'draftapproval': _('Draft Approval'),
      'duedate': _('Due Date'),
      'gdot_specialist': _('GDOT Specialist'),
      }

class NoiseForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super(NoiseForm, self).__init__(*args, **kwargs)
    self.name = 'Noise Document'
    self.fields['documenttype'] = ChoiceField(choices=shared.NOISE_DOCUMENTS)
  class Meta:
    model = Noise
    fields = ['project', 'documenttype', 'title', 'specialist', 'gdot_specialist', 'draftsubmittal', 
              'draftapproval', 'duedate', 'comments']
    widgets = {
        'draftsubmittal': DateInput(attrs={'class':'datepicker'}),
        'draftapproval': DateInput(attrs={'class':'datepicker'}),
        'duedate': DateInput(attrs={'class':'datepicker'}),
        'comments': Textarea(attrs={'cols': 50, 'rows': 3}),
        }

    labels = {
      'draftsubmittal':_('Draft Submittal'),
      'draftapproval': _('Draft Approval'),
      'duedate': _('Due Date'),
      'gdot_specialist': _('GDOT Specialist'),
      }

class EcologyForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super(EcologyForm, self).__init__(*args, **kwargs)
    self.name = 'Ecology Document'
    self.fields['documenttype'] = ChoiceField(choices=shared.ECOLOGY_DOCUMENTS)
  class Meta:
    model = Ecology
    fields = ['project', 'documenttype', 'title', 'specialist', 'gdot_specialist', 'draftsubmittal', 
              'draftapproval', 'duedate', 'comments']
    widgets = {
        'draftsubmittal': DateInput(attrs={'class':'datepicker'}),
        'draftapproval': DateInput(attrs={'class':'datepicker'}),
        'duedate': DateInput(attrs={'class':'datepicker'}),
        'comments': Textarea(attrs={'cols': 50, 'rows': 3}),
        }

    labels = {
      'draftsubmittal':_('Draft Submittal'),
      'draftapproval': _('Draft Approval'),
      'duedate': _('Due Date'),
      'gdot_specialist': _('GDOT Specialist'),
      }

class AquaticsForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super(AquaticsForm, self).__init__(*args, **kwargs)
    self.name = 'Aquatics Document'
    self.fields['documenttype'] = ChoiceField(choices=shared.AQUATICS_DOCUMENTS)
  class Meta:
    model = Aquatics
    fields = ['project', 'documenttype', 'title', 'specialist', 'gdot_specialist', 'draftsubmittal', 
              'draftapproval', 'duedate', 'comments']
    widgets = {
        'draftsubmittal': DateInput(attrs={'class':'datepicker'}),
        'draftapproval': DateInput(attrs={'class':'datepicker'}),
        'duedate': DateInput(attrs={'class':'datepicker'}),
        'comments': Textarea(attrs={'cols': 50, 'rows': 3}),
        }

    labels = {
      'draftsubmittal':_('Draft Submittal'),
      'draftapproval': _('Draft Approval'),
      'duedate': _('Due Date'),
      'gdot_specialist': _('GDOT Specialist'),
      }

class ArchaeologyForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super(ArchaeologyForm, self).__init__(*args, **kwargs)
    self.name = 'Archaeology Document'
    self.fields['documenttype'] = ChoiceField(choices=shared.ARCH_DOCUMENTS)
  class Meta:
    model = Archaeology
    fields = ['project', 'documenttype', 'title', 'specialist', 'gdot_specialist', 'draftsubmittal', 
              'draftapproval', 'duedate', 'comments']
    widgets = {
        'draftsubmittal': DateInput(attrs={'class':'datepicker'}),
        'draftapproval': DateInput(attrs={'class':'datepicker'}),
        'duedate': DateInput(attrs={'class':'datepicker'}),
        'comments': Textarea(attrs={'cols': 50, 'rows': 3}),
        }

    labels = {
      'draftsubmittal':_('Draft Submittal'),
      'draftapproval': _('Draft Approval'),
      'duedate': _('Due Date'),
      'gdot_specialist': _('GDOT Specialist'),
      }

class HistoryForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super(HistoryForm, self).__init__(*args, **kwargs)
    self.name = 'History Document'
    self.fields['documenttype'] = ChoiceField(choices=shared.HISTORY_DOCUMENTS)
  class Meta:
    model = History
    fields = ['project', 'documenttype', 'title', 'specialist', 'gdot_specialist', 'draftsubmittal', 
              'draftapproval', 'duedate', 'comments']
    widgets = {
        'draftsubmittal': DateInput(attrs={'class':'datepicker'}),
        'draftapproval': DateInput(attrs={'class':'datepicker'}),
        'duedate': DateInput(attrs={'class':'datepicker'}),
        'comments': Textarea(attrs={'cols': 50, 'rows': 3}),
        }

    labels = {
      'draftsubmittal':_('Draft Submittal'),
      'draftapproval': _('Draft Approval'),
      'duedate': _('Due Date'),
      'gdot_specialist': _('GDOT Specialist'),
      }