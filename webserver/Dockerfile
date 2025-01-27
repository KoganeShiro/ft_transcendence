FROM nginx:latest

COPY webserver/nginx.conf /etc/nginx/nginx.conf

COPY webserver/certs/ /etc/nginx/certs/

COPY ../front-end/ /usr/share/nginx/html

EXPOSE 443