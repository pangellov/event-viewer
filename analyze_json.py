"""Hug API (local and HTTP access!)"""
import hug
from operator import itemgetter
import datetime


@hug.get("/index", output=hug.output_format.file)
def index():
    return "index.html"


@hug.get("/index.js", output=hug.output_format.file)
def index():
    return "index.js"


@hug.get("/input_json.json", output=hug.output_format.file)
def index():
    return "input_json.json"


@hug.post()
@hug.local()
#  Analyze type one - use one outage more than once for flapping scenarios
def analyze_json_type_one(body):
"""
Add docstring
"""
    flapping_services = []
    currently_down = []
    recently_down = []
    items = body["items"]
    items = sorted(items, key=itemgetter('id', 'startTime'))

    for item in items:
        item['startTime'] = datetime.datetime.strptime(item['startTime'], '%Y-%m-%d %H:%M:%S')
        item['endTime'] = item['startTime'] + datetime.timedelta(minutes=item['duration'])
        if item['startTime'] >= (datetime.datetime.now() - datetime.timedelta(minutes=5)):  # Currently down (in last 5 minutes)
            currently_down.append(item)
        if item['endTime'] >= (datetime.datetime.now() - datetime.timedelta(minutes=60)) and \
                item['startTime'] < (datetime.datetime.now() - datetime.timedelta(minutes=5)):  # Recently down (in last hour and not in currently down)
            recently_down.append(item)

    for i, item in enumerate(items):
        sum_of_outages = 0
        amount_of_outages = 0
        end_time = datetime.datetime
        for check_item in items[i:]:
            if check_item['id'] == item['id']:
                if ((check_item['startTime'] - item['startTime']).total_seconds() / 60) <= 120:
                    sum_of_outages = sum_of_outages + check_item['duration']
                    amount_of_outages = amount_of_outages + 1
                    end_time = check_item['endTime']
                else:
                    break
            else:
                break
        if sum_of_outages >= 15:
            flapping_services.append({"id": item['id'],
                                      "duration": (end_time - item['startTime']).total_seconds() / 60,
                                      "startTime": item['startTime'],
                                      "endTime": end_time,
                                      "amountOfOutages": amount_of_outages,
                                      "sumOfOutages": sum_of_outages})

    return {'currently_down': currently_down, 'recently_down': recently_down, 'flapping_services': flapping_services}


@hug.post()
@hug.local()
#  Analyze type two - use one outage only in one flapping scenario. Add item['isUsed'] = 0 property.
def analyze_json_type_two(body):
    flapping_services = []
    currently_down = []
    recently_down = []
    items = body["items"]
    items = sorted(items, key=itemgetter('id', 'startTime'))

    for item in items:
        item['startTime'] = datetime.datetime.strptime(item['startTime'], '%Y-%m-%d %H:%M:%S')
        item['endTime'] = item['startTime'] + datetime.timedelta(minutes=item['duration'])
        if item['startTime'] >= (datetime.datetime.now() - datetime.timedelta(minutes=5)):
            currently_down.append(item)
        if item['endTime'] >= (datetime.datetime.now() - datetime.timedelta(minutes=60)) and \
                item['startTime'] < (datetime.datetime.now() - datetime.timedelta(minutes=5)):
            recently_down.append(item)
        item['isUsed'] = 0

    for i, item in enumerate(items):
        if item['isUsed'] != 1:
            sum_of_outages = 0
            amount_of_outages = 0
            end_time = datetime.datetime
            for check_item in items[i:]:
                if check_item['id'] == item['id']:
                    if ((check_item['startTime'] - item['startTime']).total_seconds() / 60) <= 120:
                        sum_of_outages = sum_of_outages + check_item['duration']
                        amount_of_outages = amount_of_outages + 1
                        end_time = check_item['endTime']
                        check_item['isUsed'] = 1
                    else:
                        break
                else:
                    break
            if sum_of_outages >= 15:
                flapping_services.append({"id": item['id'],
                                          "duration": (end_time - item['startTime']).total_seconds() / 60,
                                          "startTime": item['startTime'],
                                          "endTime": end_time,
                                          "amountOfOutages": amount_of_outages,
                                          "sumOfOutages": sum_of_outages})

    return {'currently_down': currently_down, 'recently_down': recently_down, 'flapping_services': flapping_services}
