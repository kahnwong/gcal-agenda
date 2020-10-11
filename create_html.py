from list_events import main as get_events
from datetime import datetime
from dateutil.parser import parse
from html_blocks import *
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_events_list():
    events = get_events()

    return events


def get_wather():
    url = 'https://api.darksky.net/forecast/{}/{},{}?units=auto&exclude=minutely,daily,alerts,currently,flags'\
            .format(os.environ['weather_api_key'],
                    os.environ['latitude'], 
                    os.environ['longitude'])

    r = requests.get(url).json()

    ### processing
    weathers_raw = []
    weathers_raw.append(r['hourly']['data'][0])  # current
    weathers_raw.append(r['hourly']['data'][2])  # in two hours

    # "darksky: fontawesome"
    icon_dict = {
        'clear-day': 'sun',
        'clear-night': 'moon',
        'rain': 'cloud-rain',
        'snow': 'snowflake',
        'wind': 'wind',
        'cloudy': 'cloud',
        'partly-cloudy-day': 'cloud-sun',
        'partly-cloudy-night': 'cloud-moon',
    }

    weathers = [{
        'title': 'Overview',
        'icon': icon_dict[r['hourly']['icon']],
        'summary': r['hourly']['summary'],
        'temperature': None
    }]
    for i in weathers_raw:
        d = {}
        d['title'] = datetime.fromtimestamp(i['time']).strftime('%-I%p') # time
        d['icon'] = icon_dict[i['icon']]
        d['summary'] = i['summary']
        d['temperature'] = i['apparentTemperature'] 

        weathers.append(d)


    return weathers
    

def formatting(events):
    ###
    for i in events:
        i['day_name'] = parse(i['start']).strftime('%A')
        i['start'] = parse(i['start']).strftime('%H:%M')
        i['end'] = parse(i['end']).strftime('%H:%M')

    ###
    events_partition = {}
    for i in events:
        day_name = i.pop('day_name')

        # create day_name key
        if not events_partition.get(day_name):
            events_partition[day_name] = []

        events_partition[day_name].append(i)
    ###

    return events_partition


def generate_html(events):
    with open('agenda.html', 'w') as f:
        f.write(header(os.environ['font_wesome_kit_id']))
        f.write('\n')
        f.write(header_extend())
        f.write('\n')
        f.write(header_today())
        f.write('\n')

        ### comment out this block if you don't want to add weather
        weathers = get_wather()
        f.write("""<div id="contact">""")
        f.write('\n')

        for i in weathers:
            f.write(weather(i))
            f.write('\n')

        f.write("""</div>""")
        f.write('\n')
        ###

        f.write("""</header>""")
        f.write('\n')

        for day_name in events:
            print('processing {}'.format(day_name))

            f.write(section_day(day_name))
            f.write('\n')

            f.write("""<div class="section-content">""")
            f.write('\n')

            day_events = events[day_name]
            for i in day_events:
                f.write(event(i['start'], i['end'], i['summary']))
                f.write('\n')

            f.write("""</div></section>""")
            f.write('\n')

        f.write("""</body>""")


def main():
    events = get_events_list()
    events = formatting(events)
    generate_html(events)

main()
