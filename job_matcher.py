from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from modules.resume_analyzer import extract_skills

def calculate_match_score(resume_text, job_description):
    """
    Computes a text similarity match score between resume and JD using TF-IDF and Cosine Similarity.
    """
    if not resume_text or not job_description:
        return 0.0
        
    try:
        corpus = [resume_text, job_description]
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # Calculate cosine similarity
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = float(sim[0][0]) * 100
        
        # Normalization adjustments (pure word overlap may be lower, let's boost it slightly or cap)
        # Often text overlap falls in the 15-50% range. Let's scale it so a good match looks like 70-80%.
        if score > 0:
            # Simple scaling curve: square root scaling to expand higher values and compress lower ones
            score = (score ** 0.5) * 10
            
        return min(max(round(score, 1), 0.0), 100.0)
    except Exception as e:
        print(f"Error computing job match score: {e}")
        return 0.0

def get_skill_compatibility(resume_text, job_description):
    """
    Extracts skills from both resume and JD, comparing them.
    """
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(job_description))
    
    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills.difference(resume_skills)
    extra = resume_skills.difference(jd_skills)
    
    return {
        "matched": sorted(list(matched)),
        "missing": sorted(list(missing)),
        "extra": sorted(list(extra)),
        "matched_count": len(matched),
        "missing_count": len(missing),
        "total_jd_skills": len(jd_skills)
    }
