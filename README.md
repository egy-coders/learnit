# 🧠 Django Learning Management System (LMS)

A full-featured Learning Management System (LMS) built with Django, designed for academies, training centers, and individual educators. It includes robust user roles, course and track management, quizzes, payment handling (including installment plans), certificates, and more.

---

## 🚀 Features

- 👤 **Custom User Roles**: Admin, Instructor, and Student
- 📚 **Courses & Tracks**: Organize content into structured tracks and standalone courses
- 📝 **Quizzes**: Auto-graded quizzes with scoring logic
- 💳 **Payments**: One-time payments and installment plans (with transaction history)
- 📜 **Certificates**: Auto-generated PDF certificates upon completion
- 🔐 **Authentication**: Secure login, registration, and role-based access
- 📈 **Enrollment Tracking**: Manage and track student progress
- 📬 **Notifications** _(Optional)_: Email notifications for course events

---

## 🛠️ Tech Stack

- **Backend**: Django (Custom User Model, Class-Based Views, REST APIs)
- **Database**: PostgreSQL (default can be changed to SQLite or others)
- **Payments**: Paymob
- **Frontend**: Django Templates or REST-ready for React/Vue/Next.js frontends
- **PDF Generation**: WeasyPrint / ReportLab for certificate generation

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/egy-coders/django-lms.git
   cd django-lms
   ```
