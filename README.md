# 🔒 Secure Diary

A secure web application built with Python (Flask) that allows users to create private notes. This project focuses on **AppSec** and **DevSecOps** best practices.

## 🛡️ Security Features Implemented
*   **SQL Injection Protection:** Uses parameterized queries (`?`) for all database interactions.
*   **XSS Protection:** All user inputs are escaped using `html.escape()` before rendering.
*   **CSRF Protection:** Forms are protected with unique CSRF tokens.
*   **IDOR Protection:** Users can only view and delete their own notes (access control checks).
*   **Password Hashing:** Passwords are securely hashed using `werkzeug.security`.

## 🚀 Tech Stack
*   **Backend:** Python, Flask
*   **Database:** SQLite
*   **Testing:** Unittest (automated security tests)
*   **DevOps:** Docker, GitHub Actions (CI/CD pipeline)

## ⚙️ How to Run (Docker)
The easiest way to run this project is using Docker:

1. Clone the repository:
   ```bash
   git clone https://github.com/89850850001nf-arch/secure-diary.git
