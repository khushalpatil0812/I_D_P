def analyze_skill_gap(user_skills, required_skills):
    """
    Analyze the gap between user skills and required skills
    
    Args:
        user_skills: List of current user skills
        required_skills: List of required skills for target role
    
    Returns:
        Dictionary with gap analysis results
    """
    user_skills_lower = [skill.lower().strip() for skill in user_skills]
    required_skills_lower = [skill.lower().strip() for skill in required_skills]
    
    # Find missing skills
    missing_skills = [skill for skill in required_skills if skill.lower() not in user_skills_lower]
    
    # Find matching skills
    matching_skills = [skill for skill in required_skills if skill.lower() in user_skills_lower]
    
    # Calculate gap percentage
    total_required = len(required_skills)
    gap_count = len(missing_skills)
    gap_percentage = (gap_count / total_required * 100) if total_required > 0 else 0
    
    return {
        'missing_skills': missing_skills,
        'matching_skills': matching_skills,
        'gap_percentage': round(gap_percentage, 2),
        'total_required': total_required,
        'skills_acquired': len(matching_skills)
    }


def prioritize_skills(missing_skills, user_goal=None):
    """
    Prioritize skills based on importance and user goals
    
    Args:
        missing_skills: List of skills the user is missing
        user_goal: User's career goal (optional)
    
    Returns:
        Ordered list of prioritized skills
    """
    # For now, return as-is. Can be enhanced with ML-based prioritization
    return missing_skills[:5]  # Limit to top 5 for focused development
