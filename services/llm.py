import os
from typing import List, Dict
import httpx




async def generate_explanation_and_recommendation(insights: List[Dict], score_data: Dict):
    prompt = f"""
You are a performance ad analyst. A Meta Ads account has the following average performance:
- Spotnxt Score: {score_data['average_score']}
- Sample Ads Data: {insights[:3]}

Explain this score in simple terms and suggest 3 ways the user can improve their ads.
"""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://34.93.124.236:8000/generate",
                json={
                    "prompt": prompt,
                    "max_tokens": 300
                }
            )
            response.raise_for_status()
            content = response.json().get("text", "")

        return {
            "explanation": content.split("Recommendations:")[0].strip(),
            "recommendations": content.split("Recommendations:")[-1].strip() if "Recommendations:" in content else ""
        }

    except Exception as e:
        return {
            "explanation": "Error generating explanation.",
            "recommendations": str(e)
        }
