# 💍 Matrimony — Django Matchmaking Platform

A full-featured matrimonial web application built with **Django**, enabling users to create profiles, set partner preferences, browse matches, and connect with potential life partners.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Matrimony is a modern, Django-powered web platform that simplifies the matchmaking process. Users can register, build detailed personal profiles, specify partner preferences, upload photos, and explore curated matches — all within a secure and intuitive interface.

---

## ✨ Features

- 🔐 **User Authentication** — Secure registration, login, and session management
- 👤 **Profile Management** — Create, edit, and view detailed personal profiles
- 🔍 **Partner Preferences** — Set and update partner criteria for better matches
- 💞 **Smart Matching** — Browse profiles matched based on preferences
- 📸 **Photo Upload** — Upload and update profile photos
- 🔔 **Notifications** — Stay updated with relevant activity
- 💳 **Payments** — Premium membership and payment integration
- 🔎 **Search** — Find profiles using advanced search filters
- 📊 **Dashboard** — Personalized dashboard for activity overview
- 📱 **Responsive Design** — Mobile-friendly UI

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.14, Django 3.x |
| Database | SQLite3 (development) |
| Frontend | HTML5, CSS3, JavaScript |
| Static Files | Django Static Files |
| Version Control | Git & GitHub |
| Deployment | Heroku (Procfile, runtime.txt) |
| Environment | Python Virtual Environment |

---

## 📁 Project Structure

```
matrimony/
├── matrimony_project/       # Core Django project settings
├── accounts/                # User authentication & registration
├── profiles/                # Profile creation, editing & viewing
│   ├── views.py             # Profile views
│   ├── urls.py              # Profile URL routing
│   └── models.py            # Profile data models
├── matches/                 # Matchmaking logic
├── dashboard/               # User dashboard
├── search/                  # Search functionality
├── notifications/           # Notification system
├── payments/                # Payment & subscription handling
├── media/                   # User-uploaded media files
├── static/                  # Static assets (CSS, JS, images)
├── staticfiles/             # Collected static files
├── templates/               # HTML templates
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── Procfile                 # Heroku process declarations
├── runtime.txt              # Python runtime version
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip
- Git
- Virtualenv (recommended)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Vortex1234-cpu/matrimony-website.git
cd matrimony-website/matrimony_project
```

**2. Create and activate a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Apply migrations**

```bash
python manage.py migrate
```

**5. Create a superuser**

```bash
python manage.py createsuperuser
```

**6. Run the development server**

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## ⚙️ Configuration

Create a `.env` file in the project root (or update `settings.py`) with the following:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (defaults to SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# Media & Static
MEDIA_URL=/media/
STATIC_ROOT=staticfiles/
```

> ⚠️ Never commit your `.env` file or expose your `SECRET_KEY`.

---

## 📖 Usage

### Key URL Routes

| URL | View | Description |
|---|---|---|
| `/profiles/create/` | `create_profile` | Create a new profile |
| `/profiles/edit/` | `edit_profile` | Edit existing profile |
| `/profiles/me/` | `view_my_profile` | View your own profile |
| `/profiles/preference/` | `partner_preference` | Set partner preferences |
| `/profiles/<id>/` | `public_profile_view` | View another user's profile |
| `/profiles/update-photo/` | `update_photo` | Upload/update profile photo |

### Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/` using your superuser credentials.

---

## ☁️ Deployment (Heroku)

This project is pre-configured for Heroku deployment.

```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Push to Heroku
git push heroku main

# Run migrations on Heroku
heroku run python manage.py migrate
```

Ensure `Procfile` and `runtime.txt` are present in the root directory.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ by [Karan](https://github.com/Vortex1234-cpu)

</div>
