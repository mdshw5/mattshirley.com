import os
import json
import yaml
import datetime
import monitor
import models
from flask import Response, request, redirect, url_for, render_template, send_from_directory
from flask.ext.gravatar import Gravatar
from werkzeug.contrib.atom import AtomFeed
from app import app


# configuration
root_path = os.path.dirname(__file__)

gravatar = Gravatar(app,
                    size=640,
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
    with open(os.path.join(root_path, 'postlisting'), 'r') as i:
        articles = json.load(i)
        articles = sorted(articles.items(), reverse=True)
        articles = articles[:10]
    for article in articles:
        feed.add(article[1], unicode(models.render_markdown(root_path + 'blog/posts/{0}.{1}'.format(article[1], 'md'),
                                                     header=True)),
                 content_type='html',
                 author='Matt Shirley',
                 url=models.make_external('http://mattshirley.com/'+article[1]),
                 updated=datetime.datetime.strptime(article[0].replace('-','') + '000000', "%Y%m%d%H%M%S"),
                 published=datetime.datetime.strptime(article[0].replace('-','') + '000000', "%Y%m%d%H%M%S"))
    return feed.get_response()

@app.route('/scical.ics')
def return_scical():
    cal = models.scrape_scical()
    return Response(cal, mimetype='text/calendar')

@app.context_processor
def query_git_repos():
    return dict(get_git_repos=models.get_git_repos)

@app.context_processor
def utility_processor():
    return(dict(root_path=root_path, render_markdown=models.render_markdown, recent_blurb=models.most_recent_blurb))

@app.route('/<postname>')
def display_post(postname):
    content = models.render_markdown('{root}/posts/{postname}.md'.format(root=root_path, postname=postname))
    if content is not False:
        return render_template('markdown.html', **locals())
    elif content is False:
        return render_template('500.html'), 500

@app.route('/update')
def update_entries():
    from subprocess import call
    retcode = call(['git', '-C', '/'.join([root_path, '..']), 'submodule', 'foreach', 'git', 'pull', 'origin', 'master'])
    if int(retcode) <= 0:
        return redirect(url_for('about'))
    else:
        return render_template('500.html'), 500

@app.route('/')
def index():
    return redirect(url_for('about'))

@app.route('/posts')
def posts():
    with open(os.path.join(root_path, 'posts/posts.yaml'), 'r') as listing:
        entries = yaml.load(listing)
        dates = sorted(entries.keys(), reverse=True)
        return render_template('show_entries.html', dates=dates, entries=entries)

@app.route('/about', methods=['GET'])
def about():
    serif = True
    if request.method == 'GET':
        print_page = request.args.get('print', False)
        resume_template = request.args.get('resume', 'generic')
        content = models.render_markdown('{0}/static/md/{1}.md'.format(root_path, resume_template))
        if print_page:
            return render_template('print_markdown.html', **locals())
        else:
            content += models.render_markdown('{0}/static/md/{1}.md'.format(root_path, 'talks'))
            return render_template('markdown.html', **locals())

@app.route('/about-me')
def aboutme_legacy():
    return redirect(url_for('about'))

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
    dirpath = os.path.join(root_path, '..', 'uploads', year, month)
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
