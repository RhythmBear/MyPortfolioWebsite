# **Portfolio Website**

## **Overview**
This portfolio website is a showcase of my skills, projects, and experiences. Built using Flask and Bootstrap, it serves as an interactive platform for users to explore my work and connect with me.

### **Features**
- Dynamic project pages with detailed descriptions.
- Contact form with email functionality.
- Mobile-first responsive design.
- Secure authentication for admin management for updating the contents of the webiste.

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

Example `.env` file:
```plaintext
FLASK_SECRET_KEY=your-very-secret-key
DATABASE_URL=postgresql://username:password@localhost/dbname
