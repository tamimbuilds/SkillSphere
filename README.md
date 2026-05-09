# SkillSphere 🌐

**SkillSphere** is a premium, full-stack recruitment and skill assessment platform built with Django. It bridges the gap between talented candidates and top-tier recruiters by integrating automated skill verification, job matching, and streamlined interview scheduling into a single, cohesive ecosystem.

---

## 🚀 Key Features

### For Candidates 🎓
- **Dynamic Profiles:** Build comprehensive profiles detailing education, specialized sectors (e.g., Fullstack, Mobile, DevOps), and experience.
- **Skill Assessments & Quizzes:** Prove your expertise through automated assessments. The platform features an intelligent scoring system with penalty tracking and limited attempts to prevent fraud.
- **Certificate Verification:** Upload external certificates for admin verification to bolster your profile.
- **Job Applications:** Apply for jobs with a single click and track application status (Applied, Shortlisted, Offered, Hired).
- **Interview Dashboard:** View scheduled interviews, meeting links, and HR contact details.

### For Recruiters 🏢
- **Job Posting & Management:** Create detailed job postings with specific skill requirements (Beginner, Intermediate, Expert) and mandatory flags.
- **Automated Candidate Matching:** Automatically filter and rank candidates based on their verified skills and assessment scores.
- **Interview Scheduling:** Organize multi-round interviews (HR, Technical, Final), assign interviewers, and manage schedules.
- **Job Offers:** Generate, send, and track job offers directly through the platform.
- **Shortlisting & Notes:** Keep track of top candidates with custom notes and statuses.

### Platform-Wide ✨
- **Role-Based Access Control:** Secure, isolated dashboards for Candidates and Recruiters.
- **Premium User Interface:** Modern, tech-focused design featuring glassmorphism, background animations, responsive layouts, and staggered entrance effects.
- **Real-time Notifications:** Alerts for interview schedules, job offers, and application updates.

---

## 🛠️ Technology Stack

- **Backend:** Python 3, Django 5.0+
- **Database:** PostgreSQL (Production via Railway), SQLite3 (Local Development)
- **Static File Serving:** WhiteNoise
- **WSGI Server:** Gunicorn
- **Image Processing:** Pillow (for profile photos and certificates)
- **Frontend:** HTML5, CSS3 (Vanilla CSS with premium styling, CSS Grid/Flexbox for responsiveness), JavaScript (Vanilla for interactions)

---

## 🏗️ Project Architecture

The project is structured into four main Django applications:

1. **`accounts`**: Manages the custom `User` model, Candidate/Recruiter profiles, and real-time notifications.
2. **`skills`**: Handles the core skill taxonomy, question banks, candidate assessments, skill progress (penalty/locking), and certificate verification.
3. **`jobs`**: Manages job postings, candidate applications, matching scores, hiring invitations, and job offers.
4. **`interviews`**: Facilitates scheduling, managing interviewers, shortlisting candidates, and tracking interview feedback/scores.

---

## 💻 Local Setup & Installation

Follow these steps to run SkillSphere locally on your machine.

### Prerequisites
- Python 3.10+
- Git
- PostgreSQL (optional for local, uses SQLite by default)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd DjangoProject-skillsphere
```

### 2. Set Up a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the `skillsphere` directory (where `settings.py` is located) or at the project root, using `.env.example` as a template.
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### 5. Apply Migrations
```bash
cd skillsphere
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed the Database
To populate the database with initial skills and assessment questions, run the custom management commands:
```bash
python manage.py seed_skills
python manage.py seed_assessment_questions
```

### 7. Create a Superuser
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## ☁️ Deployment (Railway)

This project is configured for seamless deployment on [Railway](https://railway.app/).

1. Connect your GitHub repository to a new Railway project.
2. Add a **PostgreSQL** database service in Railway.
3. Railway will automatically detect the `railway.toml` and `Procfile`.
4. Ensure the following environment variables are set in your Railway project:
   - `DEBUG=False`
   - `SECRET_KEY` (Generate a secure, random string)
   - `ALLOWED_HOSTS` (Your Railway domain)
   - `CSRF_TRUSTED_ORIGINS` (e.g., `https://your-app.up.railway.app`)
   - Database Variables (Automatically added by Railway Postgres, or manually add `DATABASE_URL`)
5. Deploy the application!

---

## 🤝 Contributing

We welcome contributions to SkillSphere! 
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

*Built with ❤️ for better recruitment and career growth.*
