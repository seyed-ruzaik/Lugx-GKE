# Use a base web server image
FROM nginx:alpine

# Copy the HTML files into the web server directory
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80
