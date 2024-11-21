# 1. Phase: Build
FROM node:16-alpine AS build-stage
WORKDIR /frontend

# Installiere Abhängigkeiten und baue das Projekt
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 2. Phase: Bereitstellung mit Nginx
FROM nginx:alpine
COPY default.conf /etc/nginx/conf.d/default.conf

# Kopiere den gebauten `dist`-Ordner aus der Build-Phase
COPY --from=build-stage /frontend/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
