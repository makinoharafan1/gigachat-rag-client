FROM node:alpine AS development

WORKDIR /app

COPY yarn.lock package.json ./
RUN yarn install --frozen-lockfile

COPY . .

EXPOSE 8070

CMD ["yarn", "dev", "--host", "0.0.0.0"]
