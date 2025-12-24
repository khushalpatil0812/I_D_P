from ai_engine.gemini_client import gemini_client
from ai_engine.gap_analysis import analyze_skill_gap, prioritize_skills

def generate_smart_recommendations(user, target_role, required_skills):
    """
    Generate SMART IDP recommendations using Gemini API
    
    Args:
        user: User object with current skills and profile
        target_role: Target role name
        required_skills: List of required skills for target role
    
    Returns:
        List of SMART action dictionaries
    """
    # Perform gap analysis
    user_skills = user.get_skills_list()
    gap_analysis = analyze_skill_gap(user_skills, required_skills)
    
    if not gap_analysis['missing_skills']:
        return [{
            'skill_gap': 'No significant gaps found',
            'action': f'Continue developing expertise in {", ".join(user_skills[:3])} to excel in {target_role} role.',
            'timeline': '3-6 months',
            'metric': 'Complete advanced certifications or lead complex projects',
            'status': 'pending'
        }]
    
    # Prioritize skills
    priority_skills = prioritize_skills(gap_analysis['missing_skills'], user.goal)
    
    # Generate SMART recommendations using Gemini
    recommendations = []
    
    for skill in priority_skills[:3]:  # Limit to top 3 for focused development
        prompt = f"""
You are an expert HR career development advisor. Generate a SMART (Specific, Measurable, Actionable, Relevant, Time-bound) development action for the following:

Employee Profile:
- Current Skills: {', '.join(user_skills)}
- Experience: {user.experience} years
- Current Role: {user.current_role or 'Not specified'}
- Career Goal: {user.goal or 'Professional growth'}

Target Role: {target_role}
Skill Gap Identified: {skill}

Create a detailed SMART action plan in the following format:

Action: [Specific, actionable steps to acquire the skill]
Timeline: [Time-bound deadline, e.g., "3 months" or "6 weeks"]
Metric: [Measurable success criteria]

Be specific, practical, and focused on real-world application. Keep the response concise and actionable.
"""
        
        response = gemini_client.generate_content(prompt)
        
        if response:
            # Parse the response
            action_dict = parse_gemini_response(response, skill)
            recommendations.append(action_dict)
        else:
            # Fallback if API fails
            recommendations.append({
                'skill_gap': skill,
                'action': f'Complete online course or certification in {skill}. Practice through hands-on projects.',
                'timeline': '3 months',
                'metric': f'Earn certification and complete 2 practical projects using {skill}',
                'status': 'pending'
            })
    
    return recommendations


def parse_gemini_response(response_text, skill):
    """
    Parse Gemini API response into structured SMART action
    
    Args:
        response_text: Raw response from Gemini
        skill: The skill being addressed
    
    Returns:
        Dictionary with parsed SMART action
    """
    lines = response_text.strip().split('\n')
    
    action = ""
    timeline = "3 months"
    metric = ""
    
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower.startswith('action:'):
            action = line.split(':', 1)[1].strip()
        elif line_lower.startswith('timeline:'):
            timeline = line.split(':', 1)[1].strip()
        elif line_lower.startswith('metric:'):
            metric = line.split(':', 1)[1].strip()
    
    # If parsing fails, use the entire response as action
    if not action:
        action = response_text.strip()
    
    return {
        'skill_gap': skill,
        'action': action if action else response_text,
        'timeline': timeline,
        'metric': metric if metric else f'Demonstrate proficiency in {skill}',
        'status': 'pending'
    }
