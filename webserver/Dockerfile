FROM node:latest AS builder

WORKDIR /app

COPY front-end/package.json front-end/package-lock.json ./
RUN npm install

COPY ./front-end .
RUN npm run build

FROM nginx:latest

RUN apt-get update && \  
    apt-get install -y openssl   

COPY webserver/create_ssl_and_start_nginx.sh /docker-entrypoint.d/01-create_ssl_and_start_nginx.sh
RUN chmod +x /docker-entrypoint.d/01-create_ssl_and_start_nginx.sh

COPY webserver/nginx.conf /etc/nginx/nginx.conf

# COPY webserver/certs/ /etc/nginx/certs/ 
#move the certs copy to run part with script

COPY --from=builder /app/dist /usr/share/nginx/html
# COPY ../front-end/dist /usr/share/nginx/html

# ENTRYPOINT [ "./create_ssl_and_start_nginx.sh" ]

EXPOSE 443