import datetime
from cal_setup import get_calendar_service

def main():
    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting List o 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return ['No events today.']
    
    else:
        output = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['start'].get('date'))
    #         print(start, event['summary'])

            d = {}
            d['start'] = start
            d['end'] = end
            d['summary'] = event['summary']
            output.append(d)
            
        return output


if __name__ == '__main__':
    main()
