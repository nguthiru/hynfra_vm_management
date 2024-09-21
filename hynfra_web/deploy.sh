#!/bin/bash

# This script is used to deploy the hynfra_web project
npm install
npm run build
sudo cp -r dist/* /var/www/html/
sudo systemctl restart nginx