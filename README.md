# TrustLens – AI Resume Analyzer & Job Matching Platform

## Abstract

TrustLens is an Artificial Intelligence-based Resume Analysis and Job Matching platform developed using Python and Flask. The application helps job seekers evaluate their resumes by calculating an ATS (Applicant Tracking System) score, identifying missing skills, recommending suitable career paths, matching resumes with job roles, and analyzing company trustworthiness. The system uses Natural Language Processing (NLP) and Machine Learning techniques to provide intelligent recommendations that improve employability and resume quality.

---

## Keywords

Artificial Intelligence, Machine Learning, Resume Analysis, ATS Score, Job Matching, Career Recommendation, Flask, NLP, Python

---

# 1. Introduction

In today's competitive job market, recruiters use Applicant Tracking Systems (ATS) to filter resumes before they reach human recruiters. Many candidates lose opportunities because their resumes are not optimized for ATS requirements or lack relevant skills.

TrustLens is designed to solve this problem by providing intelligent resume analysis, job matching, career recommendations, and skill gap identification through an easy-to-use web application.

---

# 2. Problem Statement

Many students and job seekers are unaware of how ATS systems evaluate resumes. Existing online tools often provide limited feedback and do not combine resume analysis, job matching, skill gap detection, and company trust evaluation into a single platform.

---

# 3. Objectives

- Analyze uploaded resumes.
- Calculate ATS compatibility score.
- Match resumes with suitable job roles.
- Recommend career paths.
- Identify missing skills.
- Analyze company trustworthiness.
- Improve employability using AI techniques.

---

# 4. Methodology

The project follows the following workflow:

1. User uploads resume in PDF format.
2. Resume text is extracted.
3. NLP preprocessing is performed.
4. Machine Learning models analyze the resume.
5. ATS Score is generated.
6. Suitable job roles are predicted.
7. Missing skills are identified.
8. Career recommendations are displayed.
9. Company trust analysis is performed.

---

# 5. Literature Review

| Existing System | Limitations | Proposed System |
|-----------------|------------|-----------------|
| Online ATS Checker | Only ATS score | Complete Resume Analysis |
| Job Portals | No resume feedback | AI-powered recommendations |
| Resume Review Websites | Manual suggestions | Automatic skill analysis |
| Company Review Platforms | Separate services | Integrated company trust analysis |

---

# 6. System Architecture

```
User
   │
   ▼
Flask Web Application
   │
   ▼
Resume Upload
   │
   ▼
PDF Text Extraction
   │
   ▼
NLP Processing
   │
   ▼
Machine Learning Models
   │
   ▼
ATS Score
Job Matching
Career Recommendation
Skill Gap Analysis
Company Trust Analysis
```

---

# 7. Features

- Resume Upload
- ATS Score Calculation
- Resume Analysis
- Job Matching
- Career Recommendation
- Skill Gap Analysis
- Company Trust Checker
- Intelligent Suggestions
- User Authentication

---

# 8. Implementation

## Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

## Backend

- Flask
- Flask-Login
- Flask-SQLAlchemy

## Machine Learning

- Scikit-learn
- NLTK
- VADER Sentiment
- NumPy
- Joblib

## Document Processing

- PDFPlumber

## Database

- SQLite
- SQLAlchemy ORM

---

# 9. Tech Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Framework | Flask |
| Frontend | HTML, CSS, JavaScript |
| Machine Learning | Scikit-learn |
| NLP | NLTK, VADER Sentiment |
| Database | SQLite |
| PDF Processing | PDFPlumber |
| Version Control | Git |
| Repository | GitHub |

---

# 10. Project Modules

- Resume Analyzer
- ATS Score Calculator
- Career Recommendation
- Job Matcher
- Skill Gap Analysis
- Company Trust Analyzer
- User Authentication

---

# 11. Project Structure

```
TrustLens/
│
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── resume_analyzer.py
├── career_recommender.py
├── job_matcher.py
├── skill_gap.py
├── company_trust.py
├── templates/
├── static/
├── database/
├── data/
├── routes/
├── modules/
└── utils/
```

---

# 12. Installation

Clone the repository

```bash
git clone https://github.com/yourusername/TrustLens.git
```

Go to project folder

```bash
cd TrustLens
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

# 13. Results

The application successfully:

- Calculates ATS Score.
- Extracts resume information.
- Matches resumes with suitable job roles.
- Identifies missing skills.
- Recommends career paths.
- Performs company trust analysis.
- Provides an interactive web interface.

---

# 14. Conclusion

TrustLens integrates Artificial Intelligence, Machine Learning, and Natural Language Processing to simplify the resume evaluation process. The platform provides meaningful insights that help users improve resume quality, identify skill gaps, and make better career decisions.

---

# 15. Future Scope

- Integration with LinkedIn.
- Live Job Portal APIs.
- AI Resume Builder.
- Interview Question Generator.
- Resume Ranking.
- Cloud Deployment.
- Mobile Application.
- Advanced Deep Learning Models.

---

# 16. References

1. Python Documentation
2. Flask Documentation
3. Scikit-learn Documentation
4. NLTK Documentation
5. PDFPlumber Documentation
6. Research Papers on Resume Analysis and ATS

---
