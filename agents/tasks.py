from agents.prompts import classify_prompt, generate_ad_prompt, optimize_ad_prompt
from services.meta_ads import create_ad, fetch_ad_data, analyze_ads
from services.llm import ask_llm
from services.meta_ads.ads import fetch_ad_insights
from services.meta_ads.auth import get_user_ad_account  # Assume this gets token + account ID

async def handle_task(message: str, user_id: str) -> str:
    task = await classify_prompt(message)

    if task == "create":
        prompt = generate_ad_prompt(message)
        content = await ask_llm(prompt)
        ad_preview = await create_ad(user_id, content)
        return f"Here's your ad preview:\n{ad_preview}"

    elif task == "analyze":
        ad_account = await get_user_ad_account(user_id)
        if not ad_account:
            return "You haven't connected your Meta Ads account yet. Please connect it to proceed."

        try:
            data = fetch_ad_insights(
                access_token=ad_account.access_token,
                ad_account_id=ad_account.meta_ad_account_id
            )
            summary = await analyze_ads(data)
            return f"Ad performance:\n{summary}"
        except Exception as e:
            return f"Failed to fetch ad insights: {str(e)}"

    elif task == "optimize":
        prompt = optimize_ad_prompt(message)
        suggestions = await ask_llm(prompt)
        return f"Optimization Suggestions:\n{suggestions}"

    else:
        return "Sorry, I didn’t understand that. Try asking me to create, analyze, or optimize an ad."
