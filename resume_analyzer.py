import re

# Comprehensive list of 150+ skills across multiple domains
SKILL_KEYWORDS = {
    # Languages
    "python", "r", "sql", "java", "javascript", "c++", "c#", "c", "go", "golang", "rust", "ruby", "php", "swift", "kotlin", "typescript", "html", "css", "bash", "shell",
    # Data Science & ML
    "machine learning", "deep learning", "natural language processing", "nlp", "computer vision", "artificial intelligence", "ai", "neural networks", "supervised learning", 
    "unsupervised learning", "reinforcement learning", "statistics", "probability", "data analysis", "data science", "data engineering", "feature engineering", 
    "time series", "a/b testing", "predictive modeling", "regression", "classification", "clustering", "dimensionality reduction", "anomaly detection",
    # DS/ML Frameworks & Libraries
    "pandas", "numpy", "scikit-learn", "sklearn", "tensorflow", "pytorch", "keras", "spacy", "nltk", "opencv", "matplotlib", "seaborn", "scipy", "huggingface", "transformers",
    "bert", "gpt", "xgboost", "lightgbm", "statsmodels",
    # Big Data & Cloud
    "spark", "apache spark", "hadoop", "hive", "kafka", "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s", "terraform", "ansible",
    "jenkins", "ci/cd", "github actions", "mlflow", "airflow", "apache airflow", "databricks", "snowflake", "redshift", "bigquery",
    # Databases
    "mysql", "postgresql", "postgres", "mongodb", "sqlite", "redis", "cassandra", "oracle", "mariadb", "dynamodb", "nosql", "sql server",
    # Web Dev & Software
    "django", "flask", "fastapi", "spring", "spring boot", "node.js", "nodejs", "react", "react.js", "angular", "vue.js", "vue", "express", "jquery", "bootstrap",
    "rest api", "graphql", "microservices", "system design", "data structures", "algorithms", "oop", "object oriented programming", "git", "github", "gitlab", "bitbucket",
    # BI & Tools
    "excel", "advanced excel", "tableau", "power bi", "powerbi", "looker", "jira", "confluence", "trello", "scrum", "agile", "linux", "unix", "postman", "swagger",
    # Soft & Business Skills
    "communication", "teamwork", "leadership", "problem solving", "critical thinking", "project management", "agile management", "requirements gathering", 
    "stakeholder management", "business analysis", "technical writing", "presentation"
}

def extract_skills(text):
    """
    Extracts skill keywords from text using regex word boundary matching.
    Handles special characters like C++ and C# explicitly.
    """
    if not text:
        return []
    
    text_lower = text.lower()
    found_skills = set()
    
    for skill in SKILL_KEYWORDS:
        # Custom regex for C++ and C# since \b doesn't work perfectly with + and #
        if skill == "c++":
            pattern = r'(?:^|[^a-zA-Z0-9])c\+\+(?:$|[^a-zA-Z0-9])'
        elif skill == "c#":
            pattern = r'(?:^|[^a-zA-Z0-9])c\#(?:$|[^a-zA-Z0-9])'
        elif skill == ".net":
            pattern = r'(?:^|[^a-zA-Z0-9])\.net(?:$|[^a-zA-Z0-9])'
        else:
            # Standard word boundary matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            
        if re.search(pattern, text_lower):
            found_skills.add(skill)
            
    # Normalize synonyms
    synonyms = {
        "nodejs": "node.js",
        "react.js": "react",
        "powerbi": "power bi",
        "golang": "go",
        "postgres": "postgresql",
        "google cloud": "gcp",
        "amazon web services": "aws",
        "apache spark": "spark",
        "apache airflow": "airflow"
    }
    
    normalized_skills = set()
    for s in found_skills:
        if s in synonyms:
            normalized_skills.add(synonyms[s])
        else:
            normalized_skills.add(s)
            
    return sorted(list(normalized_skills))

def calculate_ats_score(resume_text, target_role, role_skills_db):
    """
    Calculates ATS score based on matched keywords for the target role.
    Returns: (ats_score, matched_skills, missing_skills, extra_skills)
    """
    user_skills = set(extract_skills(resume_text))
    
    # Fallback if target role not found
    role_data = role_skills_db.get(target_role, {})
    if not role_data:
        # If unknown role, match against general skills
        required_skills = {"python", "sql", "communication", "problem solving", "git"}
    else:
        required_skills = set(role_data.get("required", []))
        
    matched_skills = user_skills.intersection(required_skills)
    missing_skills = required_skills.difference(user_skills)
    extra_skills = user_skills.difference(required_skills)
    
    if not required_skills:
        ats_score = 100.0
    else:
        # Weighted score: 80% based on required skills matching, 20% extra padding for total skills
        match_ratio = len(matched_skills) / len(required_skills)
        ats_score = match_ratio * 100.0
        
    # Cap between 0 and 100
    ats_score = min(max(round(ats_score, 1), 0.0), 100.0)
    
    return {
        "ats_score": ats_score,
        "matched_skills": sorted(list(matched_skills)),
        "missing_skills": sorted(list(missing_skills)),
        "extra_skills": sorted(list(extra_skills))
    }

def get_resume_suggestions(missing_skills):
    """
    Generates actionable improvement suggestions based on missing skills.
    """
    suggestions = []
    if not missing_skills:
        suggestions.append("Outstanding profile! Your resume covers all key required skills for this role.")
        return suggestions
        
    for skill in missing_skills:
        suggestions.append(f"Add projects and details showcasing your experience with '{skill.title()}'.")
        
    # General recommendations
    suggestions.append("Quantify achievements: use numbers and percentages (e.g., 'Optimized query performance by 30%').")
    suggestions.append("Ensure your resume uses standard section headers (Education, Experience, Projects, Skills) so ATS parsers can read it properly.")
    suggestions.append("Avoid multi-column layouts or complex graphics which can confuse automated screening software.")
    
    return suggestions
