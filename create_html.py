import os

from dotenv import load_dotenv

from functions import formatting
from functions import get_events
from functions import get_weather
from utils.html_blocks import event
from utils.html_blocks import header
from utils.html_blocks import header_extend
from utils.html_blocks import header_today
from utils.html_blocks import section_day
from utils.html_blocks import weather

load_dotenv()


def generate_html(events):
    with open("index.html", "w") as f:
        f.write(header(os.environ["font_wesome_kit_id"]))
        f.write("\n")
        f.write(header_extend())
        f.write("\n")
        f.write(header_today())
        f.write("\n")

        f.write("""<div id="contact">""")
        f.write("\n")
        ### comment out this block if you don't want to add weather
        weathers = get_weather()
        for i in weathers:
            f.write(weather(i))
            f.write("\n")

        f.write("""</div>""")
        f.write("\n")
        ###

        f.write("""</header>""")
        f.write("\n")

        for date in events:
            print("processing {}".format(date))

            f.write(section_day(date.strftime("%A")))
            f.write("\n")

            f.write("""<div class="section-content">""")
            f.write("\n")

            day_events = events[date]
            for i in day_events:
                f.write(event(i["start"], i["end"], i["summary"], i["next_event_in"]))
                f.write("\n")

            f.write("""</div></section>""")
            f.write("\n")

        f.write("""</body>""")


def main():
    events = get_events()
    events = formatting(events)
    generate_html(events)


main()
