#/bin/bash
npm install --no-package-lock
#npm run dev -- --host
#exec node node_modules/.bin/vite --host
exec npm run serve -- --host 0.0.0.0 --port 3000
#exec node node_modules/.bin/vite --host 0.0.0.0 --port 3000