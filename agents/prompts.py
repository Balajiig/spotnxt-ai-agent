def classify_prompt(user_input: str) -> str:
    """Naive classification for MVP. Improve later with NLP."""
    input_lower = user_input.lower()
    if "create" in input_lower or "new ad" in input_lower:
        return "create"
    elif "analyze" in input_lower or "performance" in input_lower:
        return "analyze"
    elif "optimize" in input_lower or "improve" in input_lower:
        return "optimize"
    return "unknown"

def generate_ad_prompt(user_input: str) -> str:
    return f"""
Act as a Meta Ad copywriter. Based on this request, generate ad text and basic creative idea:

Request: {user_input}
"""

def optimize_ad_prompt(user_input: str) -> str:
    return f"""
You are a Meta Ads optimization expert. Suggest improvements to this ad content:

{user_input}
"""
