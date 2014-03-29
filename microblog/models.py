from urlparse import urljoin
from flask import Markup, request
import codecs
import markdown
import re
import os
import json
import urllib2
import subprocess as sub
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from app import cache

ROOT = os.path.dirname(__file__)

@cache.cached(timeout=600)
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
        try:
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
        except IndexError:
            pass
    return cal.to_ical()

def refresh_postlisting():
    try:
        entries = os.listdir(ROOT + '/posts')
        dates = map(post_date, [os.path.join(ROOT, 'blog/posts', entry) for entry in entries])
        entries = map(os.path.splitext, entries)
        entries, ext = zip(*entries)
        with open(os.path.join(ROOT, 'postlisting'), 'w') as o:
            json.dump(dict(zip(dates, entries)), o, sort_keys=True)
        return True
    except Exception, e:
        return e

@cache.cached(timeout=300)
def get_git_repos(user_name):
    try:
        data = json.load(urllib2.urlopen('https://api.github.com/users/{user}/repos?sort=updated'.format(user=user_name)))
        links = list()
        for repo in data:
            links.append(u'<li><a href="{url}" target="_blank">{name}</a></li>'.format(url=repo['html_url'], name=repo['name']))
        return Markup('\n'.join(links))
    except:
        return('Repositories not available')

def post_date(post):
    """ Extract the post date from a post md file """
    with codecs.open(post, 'r', 'utf-8') as mdfile:
        for line in mdfile.readlines():
            if re.match('post_date:', line):
                date = line.split(' ')[1]
                return date

def most_recent_blurb():
    with open(os.path.join(ROOT, 'postlisting'), 'r') as i:
        entries = json.load(i)
        entries = sorted(entries.items(), reverse=True)
        most_recent_post = entries[0][1]
        post_markdown = open(ROOT + '/blog/posts/{0}.{1}'.format(most_recent_post, 'md')).readlines()
        blank = False
        while len(post_markdown.pop(0)) > 1:
            continue
        return (post_markdown[0].strip('#'),
                '{0}...'.format(''.join(post_markdown[1:])[:200]),
                most_recent_post)


def render_markdown(md, header=False):
    """ Takes a markdown file and returns html """
    try:
        mdfile = codecs.open(md, 'r', 'utf-8')
    except IOError:
        return False

    with mdfile:
        if header == True:
            header = []
            content = []
            start = False
            for line in mdfile.readlines():
                if start == True:
                    content.append(line)
                elif line != '\n':
                    header.append(line)
                elif line == '\n':
                    start = True
            header = dict(map(lambda x: str(x).split(': ')[0:2], header))
            content = Markup(markdown.markdown(''.join(content)))
        elif header == False:
            content = Markup(markdown.markdown(mdfile.read()))
    return content

def make_external(url):
    return urljoin(request.url_root, url)
