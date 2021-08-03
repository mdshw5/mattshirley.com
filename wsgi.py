from microblog.app import app
from microblog.views import *
from microblog.models import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


