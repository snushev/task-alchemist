# 🧪 Task Alchemist

> Turn chaos into clarity — manage projects, track tasks, and guard your secrets.

**Task Alchemist** is a self-hosted project management web application built with Django. It combines task tracking with a built-in **encrypted secrets vault** per project, so your API keys and credentials live alongside the work that needs them.



---

## ✨ Features

- 📁 **Project Management** — Create, update, and delete projects with full ownership control.
- ✅ **Task Tracking** — Add tasks per project, toggle completion status with a click (No JS required).
- 🔐 **Secrets Vault** — Each project gets an encrypted vault; secrets are stored using **Fernet symmetric encryption** — never plaintext in the database.
- 📊 **Dashboard** — Overview of your projects, active tasks, and secrets count (Redis-cached).
- 👤 **User Accounts** — Registration, login, and session management.
- 🛡️ **Authorization** — Strict ownership checks; users can only see and modify their own data.
- 🚀 **Production Ready** — Powered by Gunicorn and WhiteNoise for efficient static file serving.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2 (Python 3.11) |
| **Database** | PostgreSQL 15 |
| **Cache** | Redis 7 |
| **Encryption** | \`cryptography\` (Fernet) |
| **Frontend** | Tailwind CSS |
| **Server** | Gunicorn + WhiteNoise |
| **Containers** | Docker & Docker Compose |

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose installed
- Git

### 1. Clone the repository

\`\`\`bash
git clone https://github.com/your-username/task-alchemist.git
cd task-alchemist
\`\`\`

### 2. Configure environment variables

Create a \`.env\` file in the root directory:

\`\`\`bash
touch .env
\`\`\`

Add the following configuration (adjust as needed):

\`\`\`env
# Django Settings
SECRET_KEY="your-django-insecure-key"
DEBUG=0
ALLOWED_HOSTS=*

# Encryption
ENCRYPTION_KEY=m8PYZzpdEZOGgl5hZAOM4GgKI8pxZBB5_OF_okc-t98=  # Generate your own!

# Database
DB_NAME=alchemist_db
DB_USER=postgres
DB_PASS=your_secure_password
DB_HOST=db

# Redis
REDIS_URL=redis://redis:6379/1
\`\`\`

> ⚠️ **Security Warning**: Never commit your \`.env\` file. It is already listed in \`.dockerignore\` and \`.gitignore\`.

### 3. Build and start the Alchemist lab

\`\`\`bash
docker compose up --build
\`\`\`

### 4. Apply migrations & create admin

\`\`\`bash
docker compose exec app python manage.py migrate
docker compose exec app python manage.py createsuperuser
\`\`\`

### 5. Open in browser
Access the application at \`http://localhost:8000\`.

---

## 📁 Project Structure

\`\`\`text
task-alchemist/
├── src/
│   ├── config/          # Django settings, URLs, WSGI/ASGI
│   ├── projects/        # Projects & Tasks logic
│   ├── vault/           # Encrypted secrets management
│   ├── users/           # Authentication & User profiles
│   ├── templates/       # HTML templates (Tailwind-styled)
│   └── theme/           # Tailwind theme configuration
├── Dockerfile           # Multi-stage-ready production build
├── docker-compose.yaml  # Orchestrates App, DB, and Redis
├── requirements.txt     # Python dependencies
└── .env                 # Environment secrets (ignored by Git)
\`\`\`

---

## 🔐 How the Vault Works

Every project automatically gets a **Vault** created via a Django signal on \`post_save\`. Secrets stored in a vault are encrypted with Fernet before hitting the database.



- **Encryption**: \`User input → Fernet.encrypt(value) → Ciphertext stored in DB\`
- **Decryption**: \`Retrieved Ciphertext → Fernet.decrypt(value) → Decrypted output\`

The encryption key is strictly pulled from the environment and is never stored in the source code.

---

## 🗺️ Roadmap & Future Alchemy

Planned upgrades for the Task Alchemist infrastructure:

- [ ] **Infrastructure as Code (IaC)**: Automated provisioning with **Terraform**.
- [ ] **Orchestration**: Transition from Compose to **Kubernetes (K8s)** with Helm charts.
- [ ] **CI/CD**: Automated testing and deployment pipelines via **GitHub Actions**.
- [ ] **Observability**: Real-time monitoring with **Prometheus** & **Grafana**.
- [ ] **Cloud Storage**: Offloading media and static assets to AWS S3.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: \`git checkout -b feature/cool-feature\`.
3. Commit your changes.
4. Push to the branch and open a Pull Request.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
