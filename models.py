from urllib.parse import urljoin
from flask import Markup, request
import codecs
import markdown
import os
import json
import yaml
import urllib.request
from app import cache

root_path = os.path.dirname(__file__)

@cache.cached(timeout=300)
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

def most_recent_blurb():
    with open(os.path.join(root_path, 'posts/posts.yaml'), 'r') as listing:
        entries = yaml.load(listing, Loader=yaml.SafeLoader)
        dates = sorted(entries.keys(), reverse=True)
        most_recent_post = entries[dates[0]]['url']
        post_markdown = open('{root}/posts/{postname}.md'.format(root=root_path, postname=most_recent_post)).readlines()
        return (entries[dates[0]]['title'],
                '{0}...'.format(''.join([line for line in post_markdown if line[0] != '#'])[:100]),
                most_recent_post)

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
