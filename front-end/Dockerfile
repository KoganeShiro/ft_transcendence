FROM node:22.13.1

WORKDIR /app

# COPY front-end/npm_install_start_server.sh /npm_install_start_server.sh
# RUN chmod +x /npm_install_start_server.sh

# RUN npm install vite --save-dev
# RUN npm install --no-package-lock

EXPOSE 5173




# CMD ["npm", "run", "dev", "--", "--host"]
# CMD ["./npm_install_start_server.sh"] 
# for producion change this to CMD ["npm", "run", "build"] to be sure to run as daemon
CMD ["./npm_install_start_server.sh"]
# CMD ["sleep", "infinity"]
