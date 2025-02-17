#!/bin/sh
# If SSL Certif does not exist, create it

sed -i "s/HOSTNAME/$HOSTNAME/g" /etc/nginx/nginx.conf

if [ ! -f "/etc/nginx/certs/ft_transcendence.crt" ]; then

    mkdir -p /etc/nginx/certs

    # Create a self-signed certificate, if CERTIFICAT is not set, use localhost as the default
    #CERT_SUBJECT="${CERTIFICAT:-/CN=localhost}"    

    echo "Creating self-signed certificate for $CERTIFICAT"
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -out /etc/nginx/certs/ft_transcendence.crt -keyout /etc/nginx/certs/ft_transcendence.key -subj "$CERTIFICAT"
   # cat /etc/nginx/certs/ft_transcendence.crt /etc/nginx/certs/ft_transcendence.key 

else
    echo "Certificate already exists in /etc/nginx/certs/ft_transcendence.crt"
fi




# cat /etc/nginx/nginx.conf

# Start nginx in the foreground
# exec nginx -g "daemon off;"