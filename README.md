# t0pic

## Website

[pic.t0.vc](https://pic.t0.vc)

## Description

Command line image host.

This allows you to upload images from your command line or browser. A URL to the image is returned.

Images are resized to a max dimension of 1920 px. Don't use this for anything serious.

## Usage

`<command> | curl -F 'pic=@/dev/stdin' https://pic.t0.vc`

You can also upload from the web at [pic.t0.vc](https://pic.t0.vc).

## Example

```text
$ cat kitten.jpg | curl -F 'pic=@/dev/stdin' https://pic.t0.vc
  https://pic.t0.vc/YXKV.jpg
$ firefox https://pic.t0.vc/YXKV.jpg
```

### Bash Alias

Add this to your .bashrc, then `source ~/.bashrc`:

```text
alias pic="curl -F 'pic=@/dev/stdin' https://pic.t0.vc"
```

Now you can pipe directly into pic!

```text
$ cat kitten.jpg | pic
  https://pic.t0.vc/YXKV.jpg
$ firefox https://pic.t0.vc/YXKV.jpg
```

## Self-hosting

Install dependencies:
```text
$ sudo apt install python3 python3-pip python-virtualenv python3-virtualenv
```

Clone repo, create a venv, activate it, and install:
```text
$ git clone https://github.com/tannercollin/t0pic.git
$ cd t0pic
$ virtualenv -p python3 env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

You can now run it directly:
```text
(env) $ python t0pic.py
```

It's recommended to run t0pic as its own Linux user, kept alive with [supervisor](https://pypi.org/project/supervisor/):
```text
[program:t0pic]
user=t0pic
directory=/home/t0pic/t0pic
command=/home/t0pic/t0pic/env/bin/python -u t0pic.py
autostart=true
autorestart=true
stderr_logfile=/var/log/t0pic.log
stderr_logfile_maxbytes=1MB
stdout_logfile=/var/log/t0pic.log
stdout_logfile_maxbytes=1MB
```

To expose t0pic to http / https, you should configure nginx to reverse proxy:
```text
server {
    listen 80;

    root /var/www/html;
    index index.html index.htm;

    server_name pic.t0.vc;

    client_max_body_size 16M;

    location = / {
        proxy_pass http://127.0.0.1:5003/;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        root /home/t0pic/t0pic/data;
    }
}
```

Then run `sudo certbot --nginx` and follow the prompts.

## See Also

Pastebin: [txt.t0.vc](https://txt.t0.vc) - [Source Code](https://github.com/tannercollin/t0txt)

Short URL: [url.t0.vc](https://url.t0.vc) - [Source Code](https://github.com/tannercollin/t0url)

## License
This program is free and open-source software licensed under the MIT License. Please see the `LICENSE` file for details.

That means you have the right to study, change, and distribute the software and source code to anyone and for any purpose. You deserve these rights. Please take advantage of them because I like pull requests and would love to see this code put to use.

## Acknowledgements

This project was inspired by how much imgur sucks!

Thanks to all the devs behind Flask, Pillow and Python.
