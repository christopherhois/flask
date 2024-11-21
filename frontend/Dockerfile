FROM node:16-alpine AS build-stage
WORKDIR /frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the application
FROM nginx:alpine
COPY --from=build-stage /frontend/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]



#für developer mode gedacht um frontend dynamisch zu testen
#FROM node:16
#WORKDIR /app
#COPY package.json package.json
#RUN npm install
#COPY . .
#RUN npm run build
#EXPOSE 3000
#CMD ["npm", "run", "serve"]
