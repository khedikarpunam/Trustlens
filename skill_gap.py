def analyze_skill_gap(user_skills, target_role, role_skills_db):
    """
    Analyzes the gap between a user's skills and a target role.
    Computes gap details, retrieves roadmap, projects, and learning resources.
    """
    # Normalize user input skills list
    if isinstance(user_skills, str):
        # comma-separated list
        user_skills_list = [s.strip().lower() for s in user_skills.split(',') if s.strip()]
    else:
        user_skills_list = [s.lower() for s in user_skills if s]
        
    user_skills_set = set(user_skills_list)
    
    role_data = role_skills_db.get(target_role)
    if not role_data:
        return {
            "error": f"Role '{target_role}' not found in database.",
            "required_skills": [],
            "current_matching": [],
            "missing_skills": [],
            "gap_percentage": 0.0,
            "roadmap": [],
            "projects": [],
            "resources": {}
        }
        
    required_skills = role_data.get("required", [])
    advanced_skills = role_data.get("advanced", [])
    all_role_skills = set(required_skills + advanced_skills)
    
    current_matching = user_skills_set.intersection(all_role_skills)
    missing_skills = all_role_skills.difference(user_skills_set)
    
    # Required-only matching
    req_matching = user_skills_set.intersection(set(required_skills))
    
    if not required_skills:
        gap_percentage = 0.0
    else:
        gap_percentage = (1.0 - (len(req_matching) / len(required_skills))) * 100
        
    gap_percentage = min(max(round(gap_percentage, 1), 0.0), 100.0)
    
    return {
        "target_role": target_role,
        "required_skills": required_skills,
        "advanced_skills": advanced_skills,
        "current_matching": sorted(list(current_matching)),
        "missing_skills": sorted(list(missing_skills)),
        "gap_percentage": gap_percentage,
        "roadmap": role_data.get("roadmap", []),
        "projects": role_data.get("projects", []),
        "resources": role_data.get("resources", {})
    }
