FROM amd64/node:alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY ./src ./src

ENV PATH /app/node_modules/.bin:$PATH
ENV JETPACK_ENTRYPOINT /app/src/cron.js

EXPOSE 8080

CMD ["npm", "start"]