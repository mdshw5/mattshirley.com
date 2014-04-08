import os
import json
import datetime
import monitor
from flask import request, redirect, url_for, \
     render_template, send_from_directory, Response
from flask.ext.gravatar import Gravatar
from werkzeug.contrib.atom import AtomFeed
from app import app
from models import render_markdown, refresh_postlisting, \
    make_external, get_git_repos, scrape_scical, \
    most_recent_blurb

# configuration
ROOT = os.path.dirname(__file__)

gravatar = Gravatar(app,
                    size=180,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False)

@app.before_request
def remove_trailing_slash():
    if request.path != '/' and request.path.endswith('/'):
        return redirect(request.path[:-1])

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    with open(os.path.join(ROOT, 'postlisting'), 'r') as i:
        articles = json.load(i)
        articles = sorted(articles.items(), reverse=True)
        articles = articles[:10]
    for article in articles:
        feed.add(article[1], unicode(render_markdown(ROOT + 'blog/posts/{0}.{1}'.format(article[1], 'md'),
                                                     header=True)),
                 content_type='html',
                 author='Matt Shirley',
                 url=make_external('http://mattshirley.com/'+article[1]),
                 updated=datetime.datetime.strptime(article[0].replace('-','') + '000000', "%Y%m%d%H%M%S"),
                 published=datetime.datetime.strptime(article[0].replace('-','') + '000000', "%Y%m%d%H%M%S"))
    return feed.get_response()

@app.route('/scical.ics')
def return_scical():
    cal = scrape_scical()
    return Response(cal, mimetype='text/calendar')

@app.context_processor
def query_git_repos():
    return dict(get_git_repos=get_git_repos)

@app.context_processor
def utility_processor():
    return(dict(ROOT=ROOT, render_markdown=render_markdown, recent_blurb=most_recent_blurb))

@app.route('/<postname>')
def display_post(postname):
    content = render_markdown(ROOT + '/blog/posts/{0}.{1}'.format(postname, 'md'), header=True)
    if content is not False:
        return render_template('markdown.html', **locals())
    elif content is False:
        return render_template('500.html'), 500

@app.route('/update-entries')
def update_entries():
    success = refresh_postlisting()
    return str(success)

@app.route('/update-citations')
def update_citations():
    success = orcid_to_markdown('0000-0003-0855-9274')
    return str(success)

@app.route('/')
def index():
    return redirect(url_for('about'))

@app.route('/posts')
def posts():
    with open(os.path.join(ROOT, 'postlisting'), 'r') as i:
        entries = json.load(i)
        entries = sorted(entries.items(), reverse=True)
        return render_template('show_entries.html', entries=entries)

@app.route('/about', methods=['GET'])
def about():
    content = render_markdown(ROOT + '/static/md/about.md')
    serif = True
    if request.method == 'GET':
        print_page = request.args.get('print', '')
        if print_page == 'true':
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

@app.route('/uploads/<year>/<month>/<filename>')
def uploads(year, month, filename):
    dirpath = os.path.join(ROOT, 'uploads', year, month)
    print dirpath
    return send_from_directory(dirpath, filename)

@app.route('/reload')
def reload():
    """ Monitor for changes to site code and restart wsgi process if necessary """
    monitor.start(interval=1.0)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
