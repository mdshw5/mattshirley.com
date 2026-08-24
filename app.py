import markdown
import json
import urllib.request
from pathlib import Path
from urllib.error import URLError, HTTPError
from flask import Flask, redirect, render_template, request, url_for
from markupsafe import Markup, escape
from libgravatar import Gravatar

app = Flask(__name__)

root_path = Path(__file__).resolve().parent
markdown_root = root_path / 'static' / 'md'

@app.template_filter('gravatar_url')
def gravatar_url(email):
    url = Gravatar(email).get_image(size=180, rating='g')
    return url

@app.template_filter('get_git_repos')
def get_git_repos(user_name):
    try:
        url = 'https://api.github.com/users/{user}/repos?sort=updated&type=all'.format(user=user_name)
        request = urllib.request.Request(url, headers={'User-Agent': 'mattshirley.com'})
        with urllib.request.urlopen(request, timeout=5) as response:
            data = json.load(response)
        links = []
        for repo in data:
            if not repo['fork']:
                links.append('<li><a href="{url}" target="_blank" rel="noopener">{name}</a></li>'.format(
                    url=escape(repo['html_url']), name=escape(repo['name'])))
        return Markup('\n'.join(links))
    except (HTTPError, URLError, TimeoutError, ValueError):
        return('Repositories not available')

@app.template_filter('render_markdown')
def render_markdown(md, header=False):
    """ Takes a markdown file and returns html """
    markdown_path = (root_path / md).resolve()
    try:
        markdown_path.relative_to(root_path)
    except ValueError:
        return False
    if markdown_path.suffix != '.md' or not markdown_path.is_file():
        return False
    with markdown_path.open(encoding='utf-8') as markdown_file:
        return Markup(markdown.markdown(
            markdown_file.read(),
            extensions=['tables', 'fenced_code', 'footnotes']))

@app.route('/')
def index():
    return redirect(url_for('about'))

@app.route('/about', methods=['GET'])
def about():
    print_page = request.args.get('print', False)
    resume_template = request.args.get('resume', 'generic')
    resume_path = markdown_root / '{}.md'.format(resume_template)
    try:
        resume_path.resolve().relative_to(markdown_root)
    except ValueError:
        return render_template('404.html'), 404
    content = render_markdown(str(resume_path.relative_to(root_path)))
    if content is False:
        return render_template('404.html'), 404
    if print_page:
        return render_template('print_markdown.html', **locals())
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