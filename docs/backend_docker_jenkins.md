
# 🚀 Jenkins with Docker - Documentation

## 📑 Table of Contents

- [What Does This Docker Setup Do?](#what-does-this-docker-setup-do)
- [How to Build and Run Jenkins](#how-to-build-and-run-jenkins)
    - [Build the Jenkins Image](#build-the-jenkins-image)
    - [Run the Containers](#run-the-containers)
    - [Stop and Remove Containers](#stop-and-remove-containers)
- [About `casc.yaml` - Configuration as Code](#about-cascyaml---configuration-as-code)
    - [What is CasC?](#what-is-casc)
    - [Example: `casc.yaml`](#example-cascyaml)
    - [How It Works](#how-it-works)


## What Does This Docker Setup Do?

This Dockerfile builds a **custom Jenkins image** with:

- Jenkins LTS (Long-Term Support)
- Pre-installed Jenkins plugins (defined in `plugins.txt`)
- Pre-installed tools: Docker CLI, Python 3.11, Git, PostgreSQL client, Curl, Unzip
- Python virtual environment with `pytest` and `coverage`
- Jenkins configured using **Configuration as Code (CasC)** through `casc.yaml`, allowing the entire Jenkins setup to be automated (credentials, system messages, etc.).

It provides a fully functional CI/CD environment with Jenkins + Docker + PostgreSQL, ready to run pipelines, execute tests, and deploy applications.

---

## How to Build and Run Jenkins

### Build the Jenkins Image

Run the command below inside the `docker/` folder to build the custom Jenkins image:

```bash
docker build -t matheus/jenkins-custom:v1.0 .
```

---

### Run the Containers

Build and start the Jenkins and PostgreSQL containers using Docker Compose:

```bash
docker compose up --build
```

This will:

- Create a Jenkins container (`jenkins-container`) mapped to ports `8080` (UI) and `50000` (agents).

---

### Stop and Remove Containers

If you need to rebuild the containers from scratch (clearing volumes and caches), run:

```bash
docker compose down -v
```

The `-v` flag removes the persistent volumes (`jenkins_home`), ensuring a clean rebuild.

---

## About `casc.yaml` - Configuration as Code

### What is CasC?

CasC (**Configuration as Code**) is a Jenkins plugin that allows you to define the entire Jenkins configuration in YAML files. This includes:

- Credentials (API tokens, passwords, usernames)
- System messages
- Plugin settings
- Nodes and clouds
- Jobs (if extended with Job DSL)

With CasC, your Jenkins setup becomes reproducible, version-controlled, and fully automatable.

---

### Example: `casc.yaml`

```yaml
credentials:
  system:
    domainCredentials:
      - credentials:
          - usernamePassword:
              scope: GLOBAL
              id: "gpt404"
              description: "GitHub username + personal access token"
              username: "git_hub_username"
              password: "your_personal_access_token"
          - string:
              scope: GLOBAL
              id: "email-cred"
              description: "Email for pipeline notifications"
              secret: "emai_-to_receive_notifications@domain.com"

jenkins:
  systemMessage: "Credentials loaded from CasC"
```

### How It Works:

- This file is copied into `/var/jenkins_home/casc_configs/` in the container.
- The environment variable `CASC_JENKINS_CONFIG` points to this directory.
- Jenkins automatically loads this YAML at startup and configures itself.

---
