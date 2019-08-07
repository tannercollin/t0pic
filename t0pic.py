# t0pic - pic.t0.vc
# MIT License

import random
import string

from flask import abort, Flask, request, redirect
from pathlib import Path
from PIL import Image

PICS = Path('data')
MAX_SIZE = 1920
PORT = 5003
URL = 'https://pic.t0.vc'
POST = 'pic'

def help():
    form = (
        '<form action="{0}" method="POST" accept-charset="UTF-8" enctype="multipart/form-data">'
	'<input name="web" type="hidden" value="true">'
        '<input name="pic" type="file" accept="image/*" />'
        '<br><br><button type="submit">Submit</button></form>'.format(URL, POST)
    )
    return """
<pre>
                        pic.t0.vc
NAME
    t0pic: command line image host.

USAGE
    &lt;image output&gt; | curl -F '{0}=@/dev/stdin' {1}
    or upload from the web:

{2}

DESCRIPTION
    I got sick of imgur not working on mobile, so I built this
    Images are resized to a max dimension of {3} px
    Don't use this for anything serious

EXAMPLES
    ~$ cat kitten.jpg | curl -F '{0}=@/dev/stdin' {1}
       {1}/YXKV.jpg
    ~$ firefox {1}/YXKV.jpg

    Add this to your .bashrc:

    alias {0}="curl -F '{0}=@/dev/stdin' {1}"

    Now you can pipe directly into {0}!

SOURCE CODE
    https://txt.t0.vc/CQQE
    nginx config: https://txt.t0.vc/ZKEH

SEE ALSO
    https://txt.t0.vc
    https://url.t0.vc
</pre>""".format(POST, URL, form, MAX_SIZE)


def new_id():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

flask_app = Flask(__name__)

@flask_app.route('/', methods=['GET'])
def index():
    return '<html><body>{}</body></html>'.format(help())

@flask_app.route('/', methods=['POST'])
def new():
    try:
        nid = new_id()
        while nid in [p.stem for p in PICS.iterdir()]:
            nid = new_id()

        pic = request.files['pic']
        if not pic: raise
        pic = Image.open(pic)

        if pic.format == 'PNG':
            ext = '.png'
        elif pic.format == 'JPEG':
            ext = '.jpg'
        else:
            raise

        filename = nid + ext
        pic.thumbnail([MAX_SIZE, MAX_SIZE], Image.ANTIALIAS)
        pic.save(str(PICS.joinpath(filename)))

        print('Adding pic {}'.format(nid))

        url = '{}/{}'.format(URL, filename)
        if 'web' in request.form:
            return redirect(url)
        else:
            return url + '\n'
    except:
        abort(400)

flask_app.run(port=PORT)
