from urllib.parse import urljoin
from flask import Markup, request
import codecs
import markdown
import os
import json
import yaml
import urllib.request

root_path = os.path.dirname(__file__)

def get_git_repos(user_name):
    try:
        data = json.load(urllib.request.urlopen('https://api.github.com/users/{user}/repos?sort=updated&type=all'.format(user=user_name)))
        links = list()
        for repo in data:
            if not repo['fork']:
                links.append(u'<li><a href="{url}" target="_blank">{name}</a></li>'.format(url=repo['html_url'], name=repo['name']))
        return Markup('\n'.join(links))
    except:
        return('Repositories not available')

def render_markdown(md, header=False):
    """ Takes a markdown file and returns html """
    try:
        mdfile = codecs.open(md, 'r', 'utf-8')
    except IOError:
        return False
    extensions=['tables', 'fenced_code', 'footnotes']
    with mdfile:
            content = Markup(markdown.markdown(mdfile.read(), extensions=extensions))
    return content

def make_external(url):
    return urljoin(request.url_root, url)
