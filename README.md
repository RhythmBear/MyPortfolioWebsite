# **Portfolio Website**

## **Overview**
This portfolio website is a showcase of my skills, projects, and experiences. Built using Flask and Bootstrap, it serves as an interactive platform for users to explore my work and connect with me.

### **Features**
- Dynamic project pages with detailed descriptions.
- Contact form with email functionality.
- Mobile-first responsive design.
- Secure authentication for admin management for updating the contents of the webiste.
- Deployed On Heroku through Github Actions CI/CD


---

## **Getting Started**

### **Prerequisites**
Ensure you have the following installed:
- Python 3.7+
- Git

### **Environment Variables**
Create a `.env` file in the project root or export the following environment variables:

| Variable Name      | Description                                  |
|--------------------|----------------------------------------------|
| `FLASK_SECRET_KEY` | The secret key for Flask's CSRF protection. |
| `DATABASE_URL`     | URL for the database (e.g., PostgreSQL).    |
| `FLASK_APP`        | The entry point of the Flask application.    |
| `FLASK_ENV`        | The environment in which the Flask app runs. |
| `CONFIG_TYPE`      | The configuration type for the Flask app.    |
| `MAIL_USERNAME`    | Username for the email service.              |
| `MAIL_PASSWORD`    | Password for the email service.              |
| `PROD_DATABASE_URL`| URL for the production database.             |
| `PROD_DB_USER`     | Username for the production database.        |
| `PROD_DB_HOST`     | Host for the production database.            |
| `PROD_DB_PW`       | Password for the production database.        |
| `PROD_DB_NAME`     | Name of the production database.             |
| `MY_USERNAME`      | Your personal username for the website login |
| `MY_PASSWORD`      | Your personal password for the website login |



Example `.env` file:
```plaintext
FLASK_SECRET_KEY=your-very-secret-key
DATABASE_URL=postgresql://username:password@localhost/dbname
