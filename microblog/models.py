from wtforms import Form, TextField, validators, HiddenField
from urlparse import urljoin
from flask import Markup, request, Response
import codecs
import markdown
import re
import os
import json
import urllib2
import subprocess as sub
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
import pytz
from datetime import datetime, timedelta
from app import cache

ROOT = '/home/matt/microblog/'

class HamstringValidate(Form):
    barcode = TextField('Hamming7,4 barcode sequence:', [validators.Length(min=7, max=7, 
                                                                        message='Must be 7 characters long'),
                                                      validators.Regexp('[AGTC]*',
                                                      message='Must be DNA sequence (AGCT only)')],
                        default='CCAACCG')

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
        entries = os.listdir(ROOT + 'posts')
        dates = map(post_date, [os.path.join(ROOT, 'posts', entry) for entry in entries])
        entries = map(os.path.splitext, entries)
        entries, ext = zip(*entries)
        with open(os.path.join(ROOT, 'postlisting'), 'w') as o:
            json.dump(dict(zip(dates, entries)), o, sort_keys=True)
        return True
    except Exception, e:
        return e

def orcid_to_markdown(orcid):
    request = urllib2.Request('http://pub.orcid.org/0000-0003-0855-9274/orcid-works')
    request.add_header("Accept", "application/orcid+json")
    data = json.load(urllib2.urlopen(request))
    bibfile = os.path.join(ROOT, 'microblog/static/bib/publications.bib')
    cslfile = os.path.join(ROOT, 'microblog/static/csl/plos.csl')
    templatefile = os.path.join(ROOT, 'microblog/static/md/publications_template.md')
    mdfile = os.path.join(ROOT, 'microblog/static/md/publications.md')
    out = []
    with open(bibfile, 'w') as bib:
        for i,p in enumerate(data['orcid-profile']['orcid-activities']['orcid-works']['orcid-work']):
            i +=1
            bibline = p['work-citation']['citation']
            out.append(bibline)
            fields = bibline.split(',')
            s = fields[0].split('{')
            fields[0] = '{'.join([s[0], ' s'+str(i)])
            bib.write(','.join(fields) + '\n')
    with open(templatefile, 'w') as tmpl:
        for i,p in enumerate(data['orcid-profile']['orcid-activities']['orcid-works']['orcid-work']):
            i +=1
            tmpl.write('[@{0}]'.format('s'+str(i)))
    call = ['pandoc', '-s', '-S', '--biblio', bibfile, '--csl', cslfile, templatefile, '-t', 'markdown', '-o', mdfile]
    sub.call(call)
    with open(mdfile, 'r') as mdin:
        contents = mdin.readlines()
    with open(mdfile, 'w') as mdout:
        mdout.write(''.join(contents[1:]))
    return ''.join(contents[1:])

@cache.cached(timeout=300)
def get_git_repos(user_name):
    try:
        data = json.load(urllib2.urlopen('https://api.github.com/users/{user}/repos'.format(user=user_name)))
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

def check_ascii(form, field):
    if any(ord(c) > 127 for c in field.data):
        raise ValidationError('Sequence must consist of standard ASCII characters only')        

class MethylDecode(Form):
    string = TextField('methylation string (ASCII encoded):', [validators.Required(), check_ascii],
                        default='$$"8,"#-"Z#",#$"$8$$$7$#$6#",')
    length = TextField('sequence length (optional):', [validators.Regexp('[0-9]*', message='Length must be a numeric value')],
                       default='59')

def decodeASCII(mstring, length):
    """ Decode string encoded by encodeASCII()                                                                                                                                   
    """
    k = []
    mstring = mstring.replace('!',':')
    for i in mstring:
        j = ord(i) - 34
        if j > 99:
            raise ValueError
        j = str(j)
        k.append(j.zfill(2))
    result = ''.join(k)[0:int(length)]
    return '<p>'.join(['MT: ' + result, visualizeStrands(result)])

def visualizeStrands(mstring):
    """ Takes a methylation string and returns a representative DNA strand diagram """
    mtop = ['    ']
    top = ["5'  "]
    bot = ["3'  "]
    mbot = ['    ']
    for n in mstring:
        if n == '0':
            mtop.append(' ')
            top.append('X')
            bot.append('X')
            mbot.append(' ')
        elif n == '1':
            mtop.append('C')            
            top.append('C')
            bot.append('G')
            mbot.append(' ')
        elif n == '2':
            mtop.append(' ')
            top.append('G')
            bot.append('C')
            mbot.append('C')
        elif n == '3':
            mtop.append('c')
            top.append('G')
            bot.append('C')
            mbot.append(' ')
        elif n == '4':
            mtop.append(' ')
            top.append('C')
            bot.append('G')
            mbot.append('c')
        elif n == '5':
            mtop.append('M')            
            top.append('C')
            bot.append('G')
            mbot.append(' ')
        elif n == '6':
            mtop.append(' ')
            top.append('G')
            bot.append('C')
            mbot.append('M')
    mtop = ''.join(mtop)
    top = ''.join(top) + " 3'"
    bot = ''.join(bot) + " 5'"
    mbot = ''.join(mbot)
    return '<br>'.join([mtop, top, bot, mbot])

class MethylEncode(Form):
    string = TextField('MT (methylation string of numeric digits [0-8]):', [validators.Required(), validators.Regexp('[0-8]*',
                                                      message='Sequence must consist of numbers 0-8 only')],
                        default='0202002210000111005601001001020002220202022102010220010010')
                        
class ncbi_epi(Form):
    """ Test form for NCBI Epigenomics Galaxy data source tool """
    ids = TextField('IDs:', default='953,954,10197')     
    GALAXY_URL = HiddenField("")
    tool_id = HiddenField("")                  

def encodeASCII(mstring):
    """ Encode methylation / conversion string as ASCII.

    >>> encodeASCII('01000023450015302440')
    '#""9O"1@!J'                                                                                                                                                                  

    """
    if len(mstring) % 2 != 0: # test odd or even
        mstring = mstring + '0' # add padding if odd 
    n = 0
    l = []
    while 1:
        try:
            j = mstring[n:n+2]
            n += 2
            k = int(j) + 34
            l.append(k)
        except ValueError:
            m = ''.join(map(chr, l))
            m = m.replace(':','!')
            return m
            break
