from datetime import datetime
from operator import itemgetter
from ical import get_ical

def get_substring(i,data,s1,s2):
    return data[i][alt_index(data[i],s1):alt_index(data[i],s2)]

def alt_index(s1,s2):
    if s2 in s1:
        return s1.index(s2)
    else:
        for i in range(1,len(s2)):
            temp = s2[0:i] + " " + s2[i:len(s2)]
            if temp in s1:
                return s1.index(temp)
    return -1

def clean(d):
    if ":" in d:
        d = d[d.index(":") + 1:len(d)]
        d = d.replace("\\n","")
        d = " ".join(filter(lambda a: a != "", d.split(" ")))
    elif "\\n" in d:
        d = d[0:d.index("\\n")]
    d = d.replace(' for more information.',"")
    d = d.replace('\\','')
    return d

def to_date(s):
    s = s[s.index(",") + 2:len(s)]
    s = s.replace(" -","")
    s = s[0:s.index("m") + 1]
    s = s.replace(" ","")
    s = datetime.strptime(s,"%b%d%Y%I:%M%p")
    return s

def read_ical():
    data = get_ical()
    data = data.split("DESCRIPTION:")
    data.pop(0)
    event_list = []
    for i in range(0, len(data)):
        data[i] = data[i].splitlines()
        data[i] = "".join(data[i])
        data[i] = data[i].rsplit()
        data[i] = " ".join(data[i])
        title = clean(get_substring(i,data,"","Mandatory"))
        mandatory = True if "Yes" in get_substring(i,data,"Mandatory","Date & Time") else False
        date_time = to_date(clean(get_substring(i,data,"Date & Time", "Event Location")))
        location = clean(get_substring(i,data,"Event Location", "Description"))
        description = clean(get_substring(i,data,"Description","Contact"))
        event = {}
        event['title'] = title
        event['location'] = location
        event['time'] = (str(date_time.hour) if date_time.hour > 9 else "0" + str(date_time.hour)) + ":" + (str(date_time.minute) if date_time.minute >  9 else "0" + str(date_time.minute))
        event['date'] = (str(date_time.month) if date_time.month > 9 else "0" + str(date_time.month) ) + "-" + (str(date_time.day) if date_time.day > 9 else "0" + str(date_time.day)) + "-" + str(date_time.year)
        event['mandatory'] = mandatory
        event['description'] = description
        event_list.append(event)
    return sorted(event_list, key=itemgetter('date'))

def get_event_dates():
    sorted_list = read_ical()
    dates = []
    for x in sorted_list:
        if not (x['date'] in dates):
            dates.append(x['date'])
    return dates

def get_events_by_date(date):
    sorted_list = read_ical()
    filtered = []
    for x in sorted_list:
        if x['date'] == date:
            filtered.append(x)
    return filtered
