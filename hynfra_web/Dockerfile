# Build stage
FROM node:20-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Output stage: Serve with nginx

FROM alpine:latest
WORKDIR /app
COPY --from=build-stage /app/dist /app/dist
CMD ["cp", "-r", "/app/dist", "/output"]