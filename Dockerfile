FROM gcr.io/backend-243722/aleph__nodejs:latest

USER root

WORKDIR /app/
COPY package.json .
RUN npm install
RUN npm install -g gatsby-cli
COPY . .

CMD ["gatsby", "serve", "-H", "0.0.0.0"]
