def recommend_careers(user_skills, role_skills_db):
    """
    Compares user's skills against all database roles and yields recommendations.
    Returns: list of recommended roles sorted by match percentage.
    """
    # Normalize user input skills list
    if isinstance(user_skills, str):
        # comma-separated list
        user_skills_list = [s.strip().lower() for s in user_skills.split(',') if s.strip()]
    else:
        user_skills_list = [s.lower() for s in user_skills if s]
        
    user_skills_set = set(user_skills_list)
    recommendations = []
    
    for role_name, data in role_skills_db.items():
        required_skills = set(data.get("required", []))
        advanced_skills = set(data.get("advanced", []))
        all_skills = required_skills.union(advanced_skills)
        
        if not required_skills:
            continue
            
        matched_required = user_skills_set.intersection(required_skills)
        matched_advanced = user_skills_set.intersection(advanced_skills)
        
        # Calculate matching percentage (weighted: 80% on required, 20% on advanced)
        req_match = len(matched_required) / len(required_skills)
        adv_match = len(matched_advanced) / len(advanced_skills) if advanced_skills else 1.0
        
        match_pct = (req_match * 80.0) + (adv_match * 20.0)
        match_pct = min(max(round(match_pct, 1), 0.0), 100.0)
        
        missing_skills = list(required_skills.union(advanced_skills).difference(user_skills_set))
        
        # Timeline recommendation based on how many missing skills
        gap_count = len(missing_skills)
        if gap_count == 0:
            timeline = "Ready to Apply!"
        elif gap_count <= 2:
            timeline = "30 Days Plan"
        elif gap_count <= 5:
            timeline = "60 Days Plan"
        else:
            timeline = "90 Days Plan"
            
        recommendations.append({
            "role": role_name,
            "match_pct": match_pct,
            "matched_skills": sorted(list(matched_required.union(matched_advanced))),
            "missing_skills": sorted(missing_skills),
            "timeline": timeline,
            "roadmap": data.get("roadmap", []),
            "projects": data.get("projects", []),
            "resources": data.get("resources", {})
        })
        
    # Sort recommendations by match percentage descending
    recommendations.sort(key=lambda x: x["match_pct"], reverse=True)
    return recommendations
