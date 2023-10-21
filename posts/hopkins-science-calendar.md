post_date: 2013-11-05
post_name: Johns-Hopkins-Medicine-science-calendar-feed

# Johns Hopkins Medicine science calendar feed

It's always bothered me that the [Hopkins Science Calendar](http://www.hopkinsmedicine.org/scical/) is just
a static HTML table that is periodically updated. First of all, this system is totally reliant on the one
person maintaining the events. Second, I've missed out on lots of great seminars around campus just because
*I forgot to check the page frequently enough*. With these grumbles in mind, I set out to scrape the HTML from the
Science Calendar site and turn it in to a more useful iCalendar feed:

<script src="https://gist.github.com/mdshw5/9767374.js"></script>

Above is the messy code I came up with that scrapes the calendar tables and converts events in to an
iCalendar feed. You can subscribe using your favorite calendar application at [http://mattshirley.com/scical.ics](http://mattshirley.com/scical).

Keep in mind that this is a hack, so please don't blame me if something breaks.
