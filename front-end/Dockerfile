FROM node:22.13.1

WORKDIR /app

COPY front-end/package.json ./
# RUN npm install vite --save-dev
RUN npm install --no-package-lock

EXPOSE 5173

# Default command to start Vite in development mode
CMD ["npm", "run", "dev", "--", "--host"]
# CMD ["sleep", "infinity"]
