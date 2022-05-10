FROM amd64/node:17-slim

WORKDIR /app

COPY app/package*.json ./

RUN npm install

COPY ./app .

ENV PATH /app/node_modules/.bin:$PATH
ENV JETPACK_ENTRYPOINT /app/app.js

EXPOSE 8080

CMD ["node", "app.js"]