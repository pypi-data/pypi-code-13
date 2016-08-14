from django.db import models
from django.utils import timezone
from datetime import date
import shared

# Create your models here.
## EP Project
class Project(models.Model):
	jobnumber = models.CharField(max_length=15, default='', unique=True)
	projectname = models.CharField(max_length=100, default='')
	projectmanager = models.CharField(max_length=25, default='', choices=shared.PROJECT_MANAGERS)
	projectdescription = models.CharField(max_length=1000, default='', blank=True)
	client = models.CharField(max_length=30, default='', blank=True)
	county = models.CharField(max_length=15, default='', choices=shared.COUNTY_NAMES)
	# relatedprojects = models.ManyToManyField('self', null=True)
	env_cert_row = models.DateField(null=True, blank=True)
	env_cert_let = models.DateField(null=True, blank=True)
	row_auth = models.DateField(null=True, blank=True)
	let_cert = models.DateField(null=True, blank=True)
	pfpr = models.DateField(null=True, blank=True)
	ffpr = models.DateField(null=True, blank=True)
	comments = models.CharField(max_length=2000, default='', blank=True)
	def is_complete():
		pass
	def gdot_district(self):
		if self.county:
			return '{}'.format(shared.COUNTIES[self.county])
		else:
			return 'Unassigned'
	def __str__(self):
		return self.jobnumber

class PINumbers(models.Model):
    projects = models.ManyToManyField(Project, related_name='pis')
    pi_number = models.CharField(max_length=7, null=True, unique=True)
    class Meta:
            verbose_name_plural = 'PI Numbers'
    def __str__(self):
        return self.pi_number
        
class ProjectNumbers(models.Model):
    projects = models.ManyToManyField(Project, related_name='projectnumbers')
    project_number = models.CharField(max_length=20, null=True, unique=True)    
    class Meta:
            verbose_name_plural = 'Project Numbers'
    def __str__(self):
        return self.project_number

class SpecialStudy(models.Model):
	""" Base class for special studies documents """
	project = models.ForeignKey(Project, default='')
	specialist = models.CharField(max_length=50, default='', choices=shared.EMPLOYEES)
	gdot_specialist = models.CharField(max_length=50, default='')
	title = models.CharField(max_length=50, default='')
	documenttype = models.CharField(max_length=15, default='')
	draftsubmittal = models.DateField(null=True, blank=True)
	draftapproval = models.DateField(null=True, blank=True)
	duedate = models.DateField(null=True, blank=True)
	comments = models.CharField(max_length=1000, default='', blank=True)
	class Meta:
		abstract = True
	def __str__(self):		
		return '{}'.format(self.documenttype)

class Nepa(models.Model):
	project = models.ForeignKey(Project, default='')
	specialist = models.CharField(max_length=50, default='', choices=shared.NEPA_PLANNERS)
	stateplanner = models.CharField(max_length=50, default='')
	documenttype = models.CharField(max_length=15, default='', choices=shared.ENVIRONMENTAL_DOCUMENTS)
	##Submittals
	earlycoordination = models.DateField(null=True, blank=True)
	statedraft = models.DateField(null=True, blank=True)
	stateapproval = models.DateField(null=True, blank=True)
	fhwadraft = models.DateField(null=True, blank=True)
	fhwaapproval = models.DateField(null=True, blank=True)
	##Due Dates
	statedraftdue = models.DateField(null=True, blank=True)
	fhwadraftdue = models.DateField(null=True, blank=True)
	comments = models.CharField(max_length=1000, default='', blank=True)
	def is_gepa(self):
		if 'GEPA' in self.documenttype:
			return True
		return False
	def statedraft_due_in(self):
		if self.stateapproval:
			return 'Approved'
		if self.statedraftdue:
			date_diff = self.statedraftdue - date.today()
			if not date_diff:
				return 'Due Today'
			days = '{}'.format(date_diff)
			days_stripped = days.replace(', 0:00:00', '')
			return days_stripped
		return 'No Date'
	def fhwadraft_due_in(self):
		if 'GEPA' in self.documenttype:
			return 'Not Applicable'
		if self.fhwaapproval:
			return 'Approved'
		if self.fhwadraftdue:
			date_diff = self.fhwadraftdue - date.today()
			if not date_diff:
				return 'Due Today'
			days = '{}'.format(self.fhwadraftdue - date.today())
			days_stripped = days.replace(', 0:00:00', '')
			return days_stripped
		return 'No Date'
	def __str__(self):		
		return '{}'.format(self.documenttype)

class Air(SpecialStudy):
	pass

class Noise(SpecialStudy):
	pass

class Ecology(SpecialStudy):
	pass

class Aquatics(SpecialStudy):
	pass

class Archaeology(SpecialStudy):
	pass

class History(SpecialStudy):
	pass