# Hynfra VM Automation 🚀

[![Site](https://img.shields.io/badge/Site-Live-brightgreen)](https://102.209.68.86)
[![API Docs](https://img.shields.io/badge/API-Documentation-blue)](https://documenter.getpostman.com/view/13304226/2sAXqtb27r)

## 🔗 Project Links
[VM Dashboard](https://102.209.68.86)
[Admin Page](https://102.209.68.86/admin)
[API](https://102.209.68.86/api)
[API documentation](https://documenter.getpostman.com/view/13304226/2sAXqtb27r)

### Admin Credentials
**Username** - hynfra-admin
**Password** - hynfra254

## 🛠 Project Setup (Development)

### 🖥 VueJs Frontend

1. **Install and setup node**
   Follow the guide: [Getting Started with Node.js](https://www.pluralsight.com/resources/blog/guides/getting-started-with-nodejs)

2. **Navigate to the frontend directory**
   ```bash
   cd hynfra_web
   ```

3. **Install packages**
   ```bash
   npm install
   ```

4. **Run Project**
   ```bash
   npm run serve
   ```

### 🐍 Django Backend

**Requirements:** `Python 3.11`

1. **Create and activate your virtual environment**
   Follow the guide: [How to Set Up Virtual Environments in Python](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)

2. **Navigate to the backend directory**
   ```bash
   cd hynfra_api
   ```

3. **Install Project Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run project**
   ```bash
   python manage.py runserver
   ```

## 🛠 Development Frameworks

### Backend
- **Django** - Robust admin, automatic migrations

### Frontend
- **VueJs** - Simple syntax, amazing developer experience
- **TailwindCSS** - Utility-first CSS framework

### Database
- **PostgreSQL** - Supports JSON schemas for VM metadata (Future work)

## 🔒 Security Features

- Self-signed HTTPS certificates
- JWT access and refresh tokens (1-hour expiration)
- Role-Based Access Control
- GitHub SSO for quick sign-up

## 🚀 Deployment

### 🐳 Container Orchestration - Kubernetes

The application is deployed to a single-node Kubernetes cluster hosted on the Virtual Machine.

**Cluster Structure:**
1. Frontend Replica (Vue + NGINX)
2. Backend Replica (Django + Gunicorn)
3. Database Replica (PostgreSQL with Persistent Volume Claim)
4. NGINX Replica (Reverse proxy for traffic direction)

The NGINX Replica is exposed through a NodePort.

#### 🎨 Design Considerations

To simplify the setup:
- Self-hosted NGINX service
- Automatic traffic acceptance on ports 80/443
- Global HTTPS setup with SSL Termination

### 🔄 CI/CD Pipeline

**GitHub Actions** power the CI/CD execution pipeline.

#### Build and Push To Docker Hub

Example: Pushing the backend service to Docker Hub
```yaml
#Push Backend Service
docker build -t ${{ secrets.DOCKER_USERNAME }}/hynfra-api:latest -f ./hynfra_api/Dockerfile ./hynfra_api
docker push ${{ secrets.DOCKER_USERNAME }}/hynfra-api:latest
```

#### Kubernetes Deployment

The deployment script applies deployments in the `k8s` folder and updates the cluster:

```bash
cd ~/hynfra_vm_management/ && \
git pull && \
microk8s.kubectl apply -f k8s/ && \
microk8s.kubectl set image deployment/frontend frontend=nguthiru/hynfra-web:latest && \
microk8s.kubectl set image deployment/django django=nguthiru/hynfra-api:latest && \
microk8s.kubectl set image deployment/nginx nginx=nguthiru/hynfra-nginx:latest
microk8s.kubectl rollout restart deployment/frontend && \
microk8s.kubectl rollout restart deployment/django && \
microk8s.kubectl rollout restart deployment/nginx
```
