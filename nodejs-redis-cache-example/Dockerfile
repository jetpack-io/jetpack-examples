FROM node:alpine

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

# Get `jetpack-sdk` in $PATH
ENV PATH /app/node_modules/.bin:$PATH
ENV JETPACK_ENTRYPOINT /app/src/cron.js
ENV NODE_ENV Production

EXPOSE 8080

CMD ["npm", "start"]
