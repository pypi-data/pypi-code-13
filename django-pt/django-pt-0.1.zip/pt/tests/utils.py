# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 09:07:53 2016

@author: bbatt
"""

import django
import os
import random
from datetime import timedelta
from datetime import datetime
from pt import models, shared


pd = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium.'
pms = shared.PROJECT_MANAGERS
clients = shared.CLIENTS
counties = [c for c in shared.COUNTIES.iteritems()]
doctypes = shared.ENVIRONMENTAL_DOCUMENTS
ecrangestart = datetime.strptime('8/1/2015', '%m/%d/%Y')
ecrangeend = datetime.strptime('11/1/2015', '%m/%d/%Y')
sdrangestart = datetime.strptime('1/1/2016', '%m/%d/%Y')
sdrangeend = datetime.strptime('2/1/2016', '%m/%d/%Y')
frangestart = datetime.strptime('3/1/2016', '%m/%d/%Y')
frangeend = datetime.strptime('3/14/2016', '%m/%d/%Y')
sduerangestart = datetime.strptime('2/1/2016', '%m/%d/%Y')
sduerangeend = datetime.strptime('3/1/2016', '%m/%d/%Y')
sapprangestart = datetime.strptime('3/1/2016', '%m/%d/%Y')
sapprangeend = datetime.strptime('4/1/2016', '%m/%d/%Y')
fduerangestart = datetime.strptime('5/1/2016', '%m/%d/%Y')
fduerangeend = datetime.strptime('7/1/2016', '%m/%d/%Y')

pn_list = ['CSSTP-0000-00(678)', 'STP00-0000-00(999)']

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def add_dummy_data(num_of_entries):
    c = 1
    for i in range(num_of_entries):        
        jobnumber='{}{}'.format('JOB', random.randint(1001, 9999))
        project = models.Project.objects.get_or_create(jobnumber=jobnumber)[0]
        project.projectmanager = pms[random.randrange(len(pms))][0]
        project.projectname = 'Sample Project {}'.format(c)
        project.projectdescription = pd
        project.client = clients[random.randrange(len(clients))][0]
        project.county = counties[random.randrange(len(counties))][0]
        project.comments = 'Project Info, meeting notes, client notes, etc.'        
        c+=1
        pibase = '{}'.format(random.randrange(9999))
        pi = pibase.zfill(7)
        piobj = models.PINumbers.objects.get_or_create(pi_number=pi)[0]
        project.pis.add(piobj)
        for pn in pn_list:
            pnobj = models.ProjectNumbers.objects.get_or_create(project_number=pn)[0]
            project.projectnumbers.add(pnobj)
        project.save()
        nepadoc = models.Nepa()
        nepadoc.project = project
        nepadoc.specialist = project.projectmanager
        nepadoc.stateplanner = "Mike Murdoch"
        nepadoc.documenttype = doctypes[random.randrange(len(doctypes))][0]
        nepadoc.earlycoordination = random_date(ecrangestart, ecrangeend)
        nepadoc.statedraft = random_date(sdrangestart, sdrangeend)
        nepadoc.statedraftdue = random_date(sduerangestart, sduerangeend)
        nepadoc.stateapproval = random_date(sapprangestart, sapprangeend)
        if not 'GEPA' in nepadoc.documenttype:
            nepadoc.fhwadraft = random_date(frangestart, frangeend)
            nepadoc.fhwadraftdue = random_date(fduerangestart, fduerangeend)
        nepadoc.save()
        
        #Air docs
        airdoc = models.Air()
        airdoc.project = project
        airdoc.documenttype = shared.AIR_DOCUMENTS[random.randrange(len(shared.AIR_DOCUMENTS))][0]
        airdoc.title = 'Sample Air Document Title'
        airdoc.specialist = shared.EMPLOYEES[random.randrange(len(shared.EMPLOYEES))][0]
        airdoc.duedate = random_date(sduerangestart, sduerangeend)
        airdoc.save()

        #Noise docs
        noisedoc = models.Noise()
        noisedoc.project = project
        noisedoc.documenttype = shared.NOISE_DOCUMENTS[random.randrange(len(shared.NOISE_DOCUMENTS))][0]
        noisedoc.title = 'Sample Noise Document Title'
        noisedoc.specialist = shared.EMPLOYEES[random.randrange(len(shared.EMPLOYEES))][0]
        noisedoc.duedate = random_date(sduerangestart, sduerangeend)
        noisedoc.save()

        #Ecology docs
        ecologydoc = models.Ecology()
        ecologydoc.project = project
        ecologydoc.documenttype = shared.ECOLOGY_DOCUMENTS[random.randrange(len(shared.ECOLOGY_DOCUMENTS))][0]
        ecologydoc.title = 'Sample Ecology Document Title'
        ecologydoc.specialist = shared.EMPLOYEES[random.randrange(len(shared.EMPLOYEES))][0]
        ecologydoc.duedate = random_date(sduerangestart, sduerangeend)
        ecologydoc.save()

        #Aquatics docs
        aquaticsdoc = models.Aquatics()
        aquaticsdoc.project = project
        aquaticsdoc.documenttype = shared.AQUATICS_DOCUMENTS[random.randrange(len(shared.AQUATICS_DOCUMENTS))][0]
        aquaticsdoc.title = 'Sample Aquatics Document Title'
        aquaticsdoc.specialist = shared.EMPLOYEES[random.randrange(len(shared.EMPLOYEES))][0]
        aquaticsdoc.duedate = random_date(sduerangestart, sduerangeend)
        aquaticsdoc.save()

        #Archaeology docs
        archaeologydoc = models.Archaeology()
        archaeologydoc.project = project
        archaeologydoc.documenttype = shared.ARCH_DOCUMENTS[random.randrange(len(shared.ARCH_DOCUMENTS))][0]
        archaeologydoc.title = 'Sample Archaeology Document Title'
        archaeologydoc.specialist = shared.EMPLOYEES[random.randrange(len(shared.EMPLOYEES))][0]
        archaeologydoc.duedate = random_date(sduerangestart, sduerangeend)
        archaeologydoc.save()

        #History docs
        historydoc = models.History()
        historydoc.project = project
        historydoc.documenttype = shared.HISTORY_DOCUMENTS[random.randrange(len(shared.HISTORY_DOCUMENTS))][0]
        historydoc.title = 'Sample History Document Title'
        historydoc.specialist = shared.EMPLOYEES[random.randrange(len(shared.EMPLOYEES))][0]
        historydoc.duedate = random_date(sduerangestart, sduerangeend)
        historydoc.save()
        
def clear_database():
    django.setup()
    models.Project.objects.all().delete()
    models.PINumbers.objects.all().delete()
    models.ProjectNumbers.objects.all().delete()
    models.Nepa.objects.all().delete()
    models.Air.objects.all().delete()
    models.Noise.objects.all().delete()
    models.Aquatics.objects.all().delete()
    models.Ecology.objects.all().delete()
    models.Archaeology.objects.all().delete()
    models.History.objects.all().delete()