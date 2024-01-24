import codecs
import markdown
import os
import os.path
import json
import yaml
import urllib.request
from flask import Flask, request
from markupsafe import Markup
from urllib.parse import urljoin
from flask import Response, request, redirect, url_for, render_template, send_from_directory
from hashlib import md5
from libgravatar import Gravatar

app = Flask(__name__)

root_path = os.path.dirname(__file__)

@app.template_filter('gravatar_url')
def gravatar_url(email):
    url = Gravatar.get_image(email, size=180, rating='g')
    return url

@app.template_filter('get_git_repos')
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

@app.template_filter('render_markdown')
def render_markdown(md, header=False):
    """ Takes a markdown file and returns html """
    try:
        mdfile = codecs.open(os.path.join(root_path, md), 'r', 'utf-8')
    except IOError:
        return False
    extensions=['tables', 'fenced_code', 'footnotes']
    with mdfile:
            content = Markup(markdown.markdown(mdfile.read(), extensions=extensions))
    return content

@app.route('/')
def index():
    return redirect(url_for('about'))

@app.route('/about', methods=['GET'])
def about():
    serif = True
    if request.method == 'GET':
        print_page = request.args.get('print', False)
        resume_template = request.args.get('resume', 'generic')
        content = render_markdown('static/md/{0}.md'.format(resume_template))
        if print_page:
            return render_template('print_markdown.html', **locals())
        else:
            return render_template('markdown.html', **locals())

@app.route('/presentations')
def presentations():
    return redirect(url_for('about') + '#talks')

@app.route('/talks')
def talks():
    return redirect(url_for('about') + '#talks')

@app.route('/posters')
def posters():
    return redirect(url_for('about') + '#posters')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500