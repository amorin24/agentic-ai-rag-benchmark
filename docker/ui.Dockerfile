FROM node:18-alpine

WORKDIR /app

COPY ui/viewer/package*.json ./
RUN npm install

COPY ui/viewer/ ./

RUN npm run build

CMD ["npm", "start"]
