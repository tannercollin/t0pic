# t0pic - pic.t0.vc
# MIT License

import random
import string

from flask import abort, Flask, request, redirect
from pathlib import Path
from PIL import Image

app = Flask(__name__)
PICS = Path('data')
MAX_SIZE = 1920
PORT = 5003
URL = 'https://pic.t0.vc'
POST = 'pic'
MAX_ALLOWED_SIZE = 16 * 1024 * 1024  # 16 MB

def help():
    form = (
        f'<form action="{URL}" method="POST" accept-charset="UTF-8" enctype="multipart/form-data">'
        '<input name="web" type="hidden" value="true">'
        f'<input name="{POST}" type="file" accept="image/*" />'
        '<br><br><button type="submit">Submit</button></form>'
    )
    return f"""
<pre>
                        pic.t0.vc
NAME
    t0pic: command line image host.

USAGE
    &lt;image output&gt; | curl -F '{POST}=@/dev/stdin' {URL}
    or upload from the web:

{form}

    or paste the image into this page.

DESCRIPTION
    I got sick of imgur not working on mobile, so I built this
    Images are resized to a max dimension of {MAX_SIZE} px
    Don't use this for anything serious

EXAMPLES
    ~$ cat kitten.jpg | curl -F '{POST}=@/dev/stdin' {URL}
       {URL}/YXKV.jpg
    ~$ firefox {URL}/YXKV.jpg

    Add this to your .bashrc:

    alias {POST}="curl -F '{POST}=@/dev/stdin' {URL}"

    Now you can pipe directly into {POST}!

SOURCE CODE
    https://txt.t0.vc/CQQE
    nginx config: https://txt.t0.vc/ZKEH
    https://github.com/tannercollin/t0pic

SEE ALSO
    https://txt.t0.vc
    https://url.t0.vc
</pre>"""

def paste():
    return f"""
    window.addEventListener('paste', e => {{
      const file = e.clipboardData.items[0].getAsFile();
      const url = URL.createObjectURL(file);
      const image = new Image();
      image.src = url;

      const form = new FormData();
      form.append('{POST}', file);
      fetch('/', {{
          method: 'POST',
          body: form
        }})
        .then(r => r.text())
        .then(u => window.location = u)
        .catch(e => alert(e.message));
    }});
"""

def new_id():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

@app.route('/', methods=['GET'])
def index():
    return f'<html><script>{paste()}</script><body>{help()}</body></html>'

@app.route('/', methods=['POST'])
def new():
    try:
        if 'pic' not in request.files or request.files['pic'].filename == '':
            print("No file part")
            abort(400)  # No file was uploaded

        pic = request.files['pic']

        if pic.mimetype not in ['image/png', 'image/jpeg', 'image/gif', 'application/octet-stream']:
            print(f"Unsupported image format: {pic.mimetype}")
            abort(400)  # Consider using a more specific status code or returning an error message

        if pic.seek(0, 2) > MAX_ALLOWED_SIZE:  # Move to end to get file size
            print(f"File size exceeds maximum allowed limit: {pic.tell()} bytes")
            abort(413)  # Payload Too Large
        pic.seek(0)  # Reset file pointer

        nid = new_id()
        while nid in [p.stem for p in PICS.iterdir()]:
            nid = new_id()

        pic = Image.open(pic.stream)  # Use .stream to read directly from Flask file storage

        if pic.format == 'PNG':
            ext = '.png'
        elif pic.format == 'JPEG':
            ext = '.jpg'
        elif pic.format == 'GIF':
            ext = '.gif'
        else:
            print(f"Unsupported image format: {pic.format}")
            abort(400)

        filename = nid + ext
        pic.thumbnail([MAX_SIZE, MAX_SIZE], Image.Resampling.LANCZOS)
        pic.save(PICS / filename)  # Use pathlib's / operator for path concatenation

        print(f'Adding pic {nid}{ext}')

        url = f'{URL}/{nid}{ext}'
        if 'web' in request.form:
            return redirect(url)
        else:
            return f'{url}\n'
    except Exception as e:
        print(f"Error processing image upload: {e}")
        abort(400)

if __name__ == '__main__':
    if not PICS.exists():
        PICS.mkdir(parents=True)
    app.run(port=PORT, debug=False)  # Turn off debug for production
