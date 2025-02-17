# FROM node:22.13.1 AS builder

# WORKDIR /app

# COPY front-end/package.json front-end/package-lock.json ./
# RUN npm install

# COPY ./front-end .

# RUN npm run build

FROM nginx:1.27.4

RUN apt-get update && \  
    apt-get install -y openssl apache2-utils 

COPY webserver/create_ssl_and_start_nginx.sh /docker-entrypoint.d/01-create_ssl_and_start_nginx.sh
RUN chmod +x /docker-entrypoint.d/01-create_ssl_and_start_nginx.sh

RUN mkdir -p /usr/share/nginx/mediafiles
RUN chown -R www-data:www-data /usr/share/nginx/mediafiles
RUN chmod -R 755 /usr/share/nginx/mediafiles

COPY webserver/nginx-dev.conf /etc/nginx/nginx.conf

COPY webserver/favicon.ico /usr/share/nginx/favicon.ico

# RUN sed -i "s/HOSTNAME/$HOSTNAME/g" /etc/nginx/nginx.conf

# COPY webserver/certs/ /etc/nginx/certs/ 
#move the certs copy to run part with script

# COPY --from=builder /app/dist /usr/share/nginx/html
# COPY ../front-end/dist /usr/share/nginx/html

# ENTRYPOINT [ "./create_ssl_and_start_nginx.sh" ]

EXPOSE 443