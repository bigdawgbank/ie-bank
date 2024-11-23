# build stage
FROM node:lts-alpine AS build-stage
ARG MODE
ARG API_URL
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

ENV VUE_APP_ROOT_API=${API_URL}

RUN npm run build -- --mode ${MODE}

# run stage
FROM nginx:stable-alpine AS run-stage
# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Copy build files
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
