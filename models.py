from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resumes = db.relationship('Resume', backref='owner', lazy=True)
    job_analyses = db.relationship('JobAnalysis', backref='owner', lazy=True)
    scam_reports = db.relationship('ScamReport', backref='owner', lazy=True)
    history = db.relationship('ApplicationHistory', backref='owner', lazy=True)


class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_name = db.Column(db.String(200))
    raw_text = db.Column(db.Text)
    extracted_skills = db.Column(db.Text)       # JSON array string
    ats_score = db.Column(db.Float, default=0.0)
    target_role = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class JobAnalysis(db.Model):
    __tablename__ = 'job_analyses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=True)
    job_title = db.Column(db.String(200))
    job_description = db.Column(db.Text)
    match_score = db.Column(db.Float, default=0.0)
    matched_skills = db.Column(db.Text)         # JSON
    missing_skills = db.Column(db.Text)         # JSON
    extra_skills = db.Column(db.Text)           # JSON
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)


class CompanyTrust(db.Model):
    __tablename__ = 'company_trust'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200))
    website_url = db.Column(db.String(500))
    contact_email = db.Column(db.String(200))
    trust_score = db.Column(db.Float, default=0.0)
    risk_level = db.Column(db.String(20))
    reasons = db.Column(db.Text)                # JSON array
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)


class ScamReport(db.Model):
    __tablename__ = 'scam_reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_text = db.Column(db.Text)
    scam_score = db.Column(db.Float, default=0.0)
    red_flags = db.Column(db.Text)              # JSON
    risk_label = db.Column(db.String(20))
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)


class ReviewCache(db.Model):
    __tablename__ = 'reviews_cache'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200))
    positive_pct = db.Column(db.Float, default=0.0)
    negative_pct = db.Column(db.Float, default=0.0)
    neutral_pct = db.Column(db.Float, default=0.0)
    summary = db.Column(db.Text)
    common_complaints = db.Column(db.Text)      # JSON
    cached_at = db.Column(db.DateTime, default=datetime.utcnow)


class ApplicationHistory(db.Model):
    __tablename__ = 'application_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(200))
    job_title = db.Column(db.String(200))
    match_score = db.Column(db.Float)
    trust_score = db.Column(db.Float)
    scam_score = db.Column(db.Float)
    decision = db.Column(db.String(20))         # Applied / Skipped / Saved
    notes = db.Column(db.Text)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
