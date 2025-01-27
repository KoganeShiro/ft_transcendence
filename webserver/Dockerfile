FROM node:latest AS builder

WORKDIR /app

COPY front-end/package.json front-end/package-lock.json ./
RUN npm install

COPY ./front-end .
RUN npm run build

FROM nginx:latest

COPY webserver/nginx.conf /etc/nginx/nginx.conf

COPY webserver/certs/ /etc/nginx/certs/

COPY --from=builder /app/dist /usr/share/nginx/html
# COPY ../front-end/dist /usr/share/nginx/html

EXPOSE 443