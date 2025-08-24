# My study blog.


### 1. Requirement
alembic==1.16.4
bleach==6.2.0
blinker==1.9.0
click==8.2.1
colorama==0.4.6
dnspython==2.7.0
email_validator==2.2.0
Flask==3.1.1
Flask-Login==0.6.3
Flask-Migrate==4.1.0
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.2
greenlet==3.2.4
gunicorn==23.0.0
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
Mako==1.3.10
Markdown==3.8.2
MarkupSafe==3.0.2
packaging==25.0
setuptools==78.1.1
SQLAlchemy==2.0.43
typing_extensions==4.14.1
waitress==3.0.2
webencodings==0.5.1
Werkzeug==3.1.3
wheel==0.45.1
WTForms==3.2.1

### 2. Deployment
```shell
waitress-serve --port=5000 --call "app:create_app"  # Windows
gunicorn -w 4 --bind unix:/home/loveplay1983/projects/xuan-blogging/otherData/sock-file/serve.sock --access-logfile - --error-logfile - "app:create_app()" # Linux

```
### 3. Gunicorn service
```shell
[Unit]
Description=Gunicorn instance for Flask Blog
After=network.target

[Service]
User=loveplay1983
Group=loveplay1983
WorkingDirectory=/home/loveplay1983/projects/xuan-blogging
Environment="PATH=/home/loveplay1983/projects/xuan-blogging/venv/bin"
ExecStart=/home/loveplay1983/projects/xuan-blogging/venv/bin/gunicorn -w 4 --bind unix:/home/loveplay1983/projects/xuan-blogging/otherData/sock-file/serve.sock --access-logfile - --error-logfile - "app:create_app()"
[Install]
WantedBy=multi-user.target

```

### 4. Nginx configuration
```shell
server {
    listen 443 ssl; # managed by Certbot
    server_name loveplay1983.us.kg www.loveplay1983.us.kg;

    ssl_certificate /etc/letsencrypt/live/loveplay1983.us.kg/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/loveplay1983.us.kg/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    # Proxy Gunicorn app
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/loveplay1983/projects/xuan-blogging/otherData/sock-file/serve.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /home/loveplay1983/projects/xuan-blogging/app/static/;
        access_log off;
        expires 30d;
    }

    # upload folder
    location /static/uploads/ {
        alias /home/loveplay1983/projects/xuan-blogging/app/static/uploads/;
        autoindex on;
        autoindex_exact_size off;   # show human-readable sizes
        autoindex_localtime on;     # show file modification time
    }
}

server {
    listen 80;
    server_name loveplay1983.us.kg www.loveplay1983.us.kg;
    return 301 https://$host$request_uri;
}

```

### 5. [博客演示](https://www.loveplay1983.us.kg/index)

 
