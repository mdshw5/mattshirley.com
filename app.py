import codecs
import markdown
import os
import json
import yaml
import urllib.request
from flask import Flask, Markup, request
from urllib.parse import urljoin
from flask import Response, request, redirect, url_for, render_template, send_from_directory
from flask_gravatar import Gravatar

app = Flask(__name__)

root_path = os.path.dirname(__file__)

gravatar = Gravatar(app,
                    size=180,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False)

@app.context_processor
def query_git_repos():
    return dict(get_git_repos=get_git_repos)

@app.route('/')
def index():
    return redirect(url_for('about'))

@app.route('/about', methods=['GET'])
def about():
    serif = True
    if request.method == 'GET':
        print_page = request.args.get('print', False)
        resume_template = request.args.get('resume', 'generic')
        content = render_markdown('{0}/static/md/{1}.md'.format(root_path, resume_template))
        if print_page:
            return render_template('print_markdown.html', **locals())
        else:
            content += render_markdown('{0}/static/md/{1}.md'.format(root_path, 'talks'))
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