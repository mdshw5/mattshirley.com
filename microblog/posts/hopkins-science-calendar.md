post_date: 2013-11-05
post_name: Johns-Hopkins-Medicine-science-calendar-feed

# Johns Hopkins Medicine science calendar feed

It's always bothered me that the [Hopkins Science Calendar](http://www.hopkinsmedicine.org/scical/) is just 
a static HTML table that is periodically updated. First of all, this system is totally reliant on the one 
person maintaining the events. Second, I've missed out on lots of great seminars around campus just because 
*I forgot to check the page frequently enough*. With these grumbles in mind, I set out to scrape the HTML from the 
Science Calendar site and turn it in to a more useful iCalendar feed:
    
    import urllib2
    from bs4 import BeautifulSoup
    from icalendar import Calendar, Event
    import pytz
    from datetime import datetime, timedelta
    def scrape_scical():
        data = urllib2.urlopen('http://www.hopkinsmedicine.org/scical/').read()
        soup = BeautifulSoup(data)
        cal = Calendar()
        cal.add('prodid', '-//Hopkins Science Calendar//mattshirley.com/scical//')
        cal.add('version', '2.0')
        rows = soup.find_all('tr')
        events = list()
        for col in rows:
            strongs = col.find_all('strong')
            strongs_list = list()
            for item in strongs:
                strongs_list.append(item.get_text().encode('ascii','ignore').translate(None, '\t\r'))
            breaks = col.find_all('br')
            breaks_list = list()
            for item in breaks:
                breaks_list.extend(filter(len, re.split('\n+', item.get_text().encode('ascii','ignore').translate(None, '\t\r'))))
            events.append(strongs_list + breaks_list[:4])
        for item in events:
            if len(item) == 0:
                continue
            event = Event()
            event.add('summary', item[1])
            event.add('location', item[5])
            event.add('description', ','.join(item[3:]))
            date_start = datetime.strptime(' '.join([item[0], item[2]]), '%A %b %d, %Y %I:%M %p')
            date_end = date_start + timedelta(hours=1)
            event.add('dtstart', date_start)
            event.add('dtend', date_end)
            event.add('dtstamp', date_start)
            cal.add_component(event)
        return cal.to_ical()
        
Above is the messy code I came up with that scrapes the calendar tables and converts events in to an 
iCalendar feed. You can subscribe using your favorite calendar application at [http://mattshirley.com/scical](http://mattshirley.com/scical). 

Keep in mind that this is a hack, so please don't blame me if something breaks.