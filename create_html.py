from list_events import main as get_events
from datetime import datetime
from dateutil.parser import parse
from html_blocks import *
import requests
import os
from dotenv import load_dotenv
load_dotenv()


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
        i['date'] = parse(i['start']).date()
        i['start'] = parse(i['start']).strftime('%H:%M')
        i['end'] = parse(i['end']).strftime('%H:%M')

    ###
    events_partition = {}
    for i in events:
        date = i['date']

        # create day_name key
        if not events_partition.get(date):
            events_partition[date] = []            

        events_partition[date].append(i)
    ###

    return events_partition


def generate_html(events):
    with open('index.html', 'w') as f:
        f.write(header(os.environ['font_wesome_kit_id']))
        f.write('\n')
        f.write(header_extend())
        f.write('\n')
        f.write(header_today())
        f.write('\n')

        f.write("""<div id="contact">""")
        f.write('\n')
        # ### comment out this block if you don't want to add weather
        # weathers = get_wather()
        # for i in weathers:
        #     f.write(weather(i))
        #     f.write('\n')

        # f.write("""</div>""")
        # f.write('\n')
        # ###

        f.write("""</header>""")
        f.write('\n')

        for date in events:
            print('processing {}'.format(date))

            f.write(section_day(date.strftime('%A')))
            f.write('\n')

            f.write("""<div class="section-content">""")
            f.write('\n')

            day_events = events[date]
            for i in day_events:
                f.write(event(i['start'], i['end'], i['summary']))
                f.write('\n')

            f.write("""</div></section>""")
            f.write('\n')

        f.write("""</body>""")


def main():
    events = get_events()
    events = formatting(events)
    generate_html(events)

main()
