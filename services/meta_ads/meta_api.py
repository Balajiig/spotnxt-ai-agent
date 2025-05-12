import requests

def get_meta_ad_insights(ad_account_id: str, access_token: str):
    url = f"https://graph.facebook.com/v18.0/act_{ad_account_id}/insights"
    params = {
        "fields": "ad_name,ctr,cpc,spend,impressions,clicks,conversions",
        "access_token": access_token
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("data", [])
