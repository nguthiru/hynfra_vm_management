FROM nginx:alpine

# Remove default Nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx config
COPY ./nginx.conf /etc/nginx/nginx.conf

# Copy SSL certificates
COPY nginx/ssl /etc/nginx/ssl

# Create directory for Let's Encrypt challenges if needed
RUN mkdir -p /var/www/certbot

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]