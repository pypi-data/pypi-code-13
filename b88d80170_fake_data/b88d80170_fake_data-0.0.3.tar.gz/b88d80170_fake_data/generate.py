from .address import *
from .company import *
from .personal_data import *
from .name import first_name
from .application import *

"""
The amount of information we capture is small, but will be enlarged through iterations

Generate numP number of people, and 
numC number of companies

Each person is associated with a company, via different relationships
WORKS_AT / OWNS

Each company is associated with an address

There are 4 files generated

person.tsv
[name, gender, dob, email, mobile, phone]

company.tsv
[name, (start, end), isSixHourClosure]

address.tsv
[number, street, suburb, postcode, state, country]

person_company.tsv
[person_name, company_name, WORKS_AT / OWNS]

company_address.tsv
[company_name, address]

"""


def gen(num_person, num_company, num_application):
    # person
    person_file = open('person.tsv', 'wb+')
    person_list = list()
    for i in range(num_person):
        d = dict()
        fng = first_name()
        fn, gender = fng[0], fng[1]
        ln = last_name()
        d['id'] = i
        d['name'] = ' '.join([fn, ln]).strip()
        d['email'] = email(fn, ln)
        d['dob'] = random_date()
        d['gender'] = gender
        d['mobile'] = mobile()
        d['phone'] = landline()
        p = Person(d)
        person_list.append(p)
        person_file.write((p.tsv() + '\n').encode())
    person_file.close()

    # company
    company_file = open('company.tsv', 'wb+')
    company_list = list()
    for i in range(num_company):
        d = dict()
        d['name'] = random_company_name()
        d['openingHours'] = pickone(['6:00-23:00', '5:00-19:00', '7:00-18:00', '9:00-21:00'])
        d['isSixHourClosure'] = pickone([True, False])
        c = Company(d)
        company_list.append(c)
        company_file.write((c.tsv() + '\n').encode())
    company_file.close()

    # company name--address
    company_address_file = open('company_address.rel', 'wb+')
    address_file = open('address.tsv', 'wb+')
    for i in range(num_company):
        num = random_st_num()
        st = random_street()
        sub, postcode = random_suburb()
        sta = random_state()
        addr = Address(num, st, sub, postcode, sta)
        address_file.write((addr.tsv() + '\n').encode())
        company_address_file.write(((company_list[i]).name + '--' + addr.tsv() + '--LOCATE_AT\n').encode())
    company_address_file.close()
    address_file.close()

    # person--application ID
    application_file = open('application.tsv', 'wb+')
    application_list = list()
    for i in range(num_application):
        d = dict()
        d['applicationId'] = random_application_id()
        d['applicationType'] = "Liquor Licence"
        app = Application(d)
        application_list.append(app)
        application_file.write((app.tsv() + '\n').encode())
    application_file.close()

    person_application_file = open('person_application.rel', 'wb+')
    for z in list(zip(person_list, application_list)):
        person_application_file.write((str(z[0].id) + '--' + str(z[1].applicationId) + '--APPLY\n').encode())
    person_application_file.close()

    # company name--person--position
    company_person_file = open('person_company.rel', 'wb+')
    owner_list = person_list[0:num_company]
    staff_list = person_list[num_company:]
    # make owner
    for i in range(num_company):
        company_person_file.write((str(owner_list[i].id) + '--' + company_list[i].name + '--OWNER_OF\n').encode())
    counter = 0
    while counter < len(staff_list):
        for i in company_list:
            if counter == len(staff_list):
                break
            company_person_file.write((str(staff_list[counter].id) + '--' + i.name + '--STAFF_OF\n').encode())
            counter += 1
    company_person_file.close()
