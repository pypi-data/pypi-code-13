
DEPARTMENTS = (			
			('Dept 1', 'Dept 1'),
			('Dept 2', 'Dept 2'),
			('Dept 3', 'Dept 3'),
			('Dept 4', 'Dept 4'),
			('Dept 5', 'Dept 5'),
			
	)

EMPLOYEES = (
			('Employee 1', 'Employee 1'),
			('Employee 2', 'Employee 2'),
			('Employee 3', 'Employee 3'),
			('Employee 4', 'Employee 4'),
			('Employee 5', 'Employee 5'),
		)

PROJECT_MANAGERS = (
			('Manager 1', 'Manager 1'),
			('Manager 2', 'Manager 2'),
			('Manager 3', 'Manager 3'),
			('Manager 4', 'Manager 4'),
			('Manager 5', 'Manager 5'),			
		)

NEPA_PLANNERS = (
			('Planner 1', 'Planner 1'),
			('Planner 2', 'Planner 2'),
			('Planner 3', 'Planner 3'),
			('Planner 4', 'Planner 4'),
			('Planner 5', 'Planner 5'),
		)

CLIENTS = (
			('Client 1', 'Client 1'),
			('Client 2', 'Client 2'),
			('Client 3', 'Client 3'),
			('Client 4', 'Client 4'),
			('Client 5', 'Client 5'),
		)

ENVIRONMENTAL_DOCUMENTS = (
			('DocType 1', 'DocType 1'),
			('DocType 2', 'DocType 2'),
			('DocType 3', 'DocType 3'),
			('DocType 4', 'DocType 4'),
			('DocType 5', 'DocType 5'),
		)

AIR_DOCUMENTS = (
				('PM25 Exemption', 'PM25 Exemption'),
				('PM25 LOD', 'PM25 LOD'),
				('GEPA Memorandum', 'GEPA Memorandum'),
				('Air Assessment', 'Air Assessment'),
				('Air Memorandum', 'Air Memorandum'),
			)

NOISE_DOCUMENTS = (
				('Assessment', 'Assessment'),
				('Addendum', 'Addendum'),
				('TypeIII', 'Type III'),
				('Memorandum', 'Memorandum'),
			)

ECOLOGY_DOCUMENTS = (
				('Assessment', 'Assessment'),
				('Addendum', 'Addendum'),
				('AOE', 'AOE'),
			)

AQUATICS_DOCUMENTS = (
				('Assessment', 'Assessment'),
				('Addendum', 'Addendum'),
			)

ARCH_DOCUMENTS = (
				('Short Form', 'Short Form'),
				('Phase I', 'Phase I'),
				('Phase II', 'Phase II'),
				('Phase III', 'Phase III'),
			)


HISTORY_DOCUMENTS = (
				('HRSR', 'HRSR'),
				('Memorandum', 'Memorandum'),
				('AOE', 'AOE'),
			)

COUNTIES = {'Appling':5, 'Atkinson':4, 'Bacon':5, 'Baker':4, 'Baldwin':2,
'Banks':1, 'Barrow':1, 'Bartow':6, 'Ben Hill':4, 'Berrien':4, 'Bibb':3,
'Bleckley':2, 'Brantley':5, 'Brooks':4, 'Bryan':5,
'Bulloch':5, 'Burke':2, 'Butts':3, 'Calhoun':4,
'Camden':5, 'Candler':5, 'Carroll':6, 'Catoosa':6,
'Charlton':5,'Chatham':5, 'Chattahoochee':3, 'Chattooga':6,
'Cherokee':6, 'Clarke':1, 'Clay':4, 'Clayton':7,
'Clinch':4, 'Cobb':7, 'Coffee':4, 'Colquitt':4,
'Columbia':2, 'Cook':4, 'Coweta':3, 'Crawford':3,
'Crisp':4, 'Dade':6, 'Dawson':1, 'Decatur':4,
'DeKalb':7, 'Dodge':2, 'Dooly':3, 'Dougherty':4,
'Douglas':7, 'Early':4, 'Echols':4, 'Effingham':5,
'Elbert':1, 'Emanuel':2, 'Evans':5, 'Fannin':6,
'Fayette':3, 'Floyd':6, 'Forsyth':1, 'Franklin':1,
'Fulton':7, 'Gilmer':6, 'Glascock':2, 'Glynn':5,
'Gordon':6, 'Grady':4, 'Greene':2,'Gwinnett':1,
'Habersham':1, 'Hall':1, 'Hancock':2, 'Haralson':6,
'Harris':3, 'Hart':1, 'Heard':3, 'Henry':3,
'Houston':3, 'Irwin':4, 'Jackson':1, 'Jasper':2,
'Jeff Davis':5, 'Jefferson':2, 'Jenkins':2, 'Johnson':2,
'Jones':3, 'Lamar':3, 'Lanier':4, 'Laurens':2,
'Lee':4, 'Liberty':5, 'Lincoln':2, 'Long':5,
'Lowndes':4, 'Lumpkin':1, 'McDuffie':2, 'McIntosh':5,
'Macon':3, 'Madison':1, 'Marion':3, 'Meriwether':3,
'Miller':4, 'Mitchell':4, 'Monroe':3, 'Montgomery':5,
'Morgan':2, 'Murray':6, 'Muscogee':3, 'Newton':2,
'Oconee':1, 'Oglethorpe':2, 'Paulding':6, 'Peach':3,
'Pickens':6, 'Pierce':5, 'Pike':3, 'Polk':6,
'Pulaski':3, 'Putnam':2, 'Quitman':4, 'Rabun':1,
'Randolph':4, 'Richmond':2, 'Rockdale':7, 'Schley':3,
'Screven':2, 'Seminole':4, 'Spalding':3, 'Stephens':1,
'Stewart':3, 'Sumter':3, 'Talbot':3, 'Taliaferro':2,
'Tattnall':5, 'Taylor':3, 'Telfair':5, 'Terrell':4,
'Thomas':4, 'Tift':4, 'Toombs':5, 'Towns':1,
'Treutlen':2, 'Troup':3,'Turner':4, 'Twiggs':3,
'Union':1, 'Upson':3, 'Walker':6, 'Walton':1,
'Ware':5, 'Warren':2, 'Washington':2, 'Wayne':5,
'Webster':3, 'Wheeler':5, 'White':1, 'Whitfield':6,
'Wilcox':4, 'Wilkes':2, 'Wilkinson':2, 'Worth':4,
}

COUNTY_NAMES = [(c, c) for c in sorted(COUNTIES.iterkeys())]