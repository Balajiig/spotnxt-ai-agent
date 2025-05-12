def calculate_spotnxt_score(insights):
    scores = []
    for ad in insights:
        ctr = float(ad.get("ctr", 0))
        cpc = float(ad.get("cpc", 0))
        conversions = int(ad.get("conversions", 0))

        ctr_score = min(ctr * 10, 100)
        cpc_score = max(100 - cpc * 10, 0)
        conv_score = min(conversions * 5, 100)

        score = 0.2 * ctr_score + 0.15 * cpc_score + 0.25 * conv_score
        scores.append(score)

    return {
        "average_score": round(sum(scores) / len(scores), 2) if scores else 0,
        "details": scores
    }
