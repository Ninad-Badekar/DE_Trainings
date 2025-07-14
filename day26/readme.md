#  Docker - Containerization Made Easy

##  What is Docker?

**Docker** is an open-source platform designed to help developers build, ship, and run applications efficiently using **containers**.

A **container** is a lightweight, standalone, and executable package that includes everything needed to run a piece of software—code, runtime, libraries, dependencies, and system tools.

Unlike traditional virtual machines (VMs), containers share the host system's kernel, making them faster and more resource-efficient.

---

##  Why Docker?

| Feature                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
|  Lightweight          | Containers are smaller and faster than VMs.                                |
|  Portable             | Run your app consistently on any environment—dev, test, or production.     |
|  Dependency Isolation | Ensures all dependencies are packaged with the app.                        |
|  Easy Versioning      | Docker images are version-controlled and can be rolled back.               |
|  Microservice-ready   | Great for breaking monolithic apps into microservices.                    |
|  Developer Friendly  | Easily reproducible dev environments for teams.                             |

---

##  Core Docker Components

| Component      | Description |
|----------------|-------------|
| **Docker Engine** | The runtime that builds, runs, and manages containers. |
| **Dockerfile**    | A script with instructions to build a Docker image. |
| **Docker Image**  | A read-only snapshot created from a Dockerfile. |
| **Docker Container** | A running instance of a Docker image. |
| **Docker Hub**     | A cloud registry to store and share Docker images. |

---

##  Docker vs Virtual Machines

| Feature             | Docker Containers                      | Virtual Machines                      |
|---------------------|----------------------------------------|---------------------------------------|
| Startup Time        | Seconds                                | Minutes                               |
| Performance         | Near-native                            | Overhead due to guest OS              |
| OS Requirements     | Shares host OS                         | Full guest OS per VM                  |
| Size                | MBs                                    | GBs                                   |
| Isolation           | Process-level                          | Hardware-level                        |

---

##  Dockerfile Example

```dockerfile
# Use official Python image from Docker Hub
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Run the application
CMD ["python", "app.py"]
```

#  Common Docker Commands

| Command                          | Description                         |
|----------------------------------|-------------------------------------|
| `docker build -t app-name .`     | Build an image from Dockerfile      |
| `docker run app-name`            | Run a container from the image      |
| `docker ps`                      | List running containers             |
| `docker images`                  | List all images                     |
| `docker stop <container-id>`     | Stop a running container            |
| `docker rm <container-id>`       | Remove a container                  |
| `docker rmi <image-id>`          | Remove an image                     |

---

#  Docker Compose

For multi-container applications, use `docker-compose.yml`.

## Example

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
  redis:
    image: "redis:alpine"
```
## Run With

```bash
docker-compose up --build

```