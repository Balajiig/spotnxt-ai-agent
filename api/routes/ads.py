from fastapi import APIRouter, Depends, HTTPException
import httpx
from services.meta_ads.meta_api import get_meta_ad_insights
from services.meta_ads.scoring_engine import calculate_spotnxt_score
from services.llm import generate_explanation_and_recommendation

router = APIRouter()



@router.get("/spotnxt-score/")
async def spotnxt_score(ad_account_id: str, access_token: str):
    try:
        insights = get_meta_ad_insights(ad_account_id, access_token)
        score_data = calculate_spotnxt_score(insights)
        llm_output = await generate_explanation_and_recommendation(insights, score_data)

        return {
            "score": score_data["average_score"],
            "details": score_data["details"],
            "insights": llm_output["explanation"],
            "recommendations": llm_output["recommendations"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/meta/accounts")
async def get_ad_accounts(access_token: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://graph.facebook.com/v17.0/me/adaccounts", params={
            "access_token": access_token,
            "fields": "name,account_id,status"
        })
        return resp.json()
