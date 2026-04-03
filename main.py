import cloudscraper
import pandas as pd
import time

BASE_URL = "https://api.startupindia.gov.in/sih/api/noauth/search/profiles"
PROFILE_URL = "https://api.startupindia.gov.in/sih/api/common/replica/user/profile/{}"

scraper = cloudscraper.create_scraper()

payload = {
    "query": "",
    "roles": ["Startup"],
    "page": 0,
    "sort": {"orders": [{"field": "registeredOn", "direction": "DESC"}]},
    "dpiitRecogniseUser": True,
    "internationalUser": False
}

def fetch_profiles(page=0, size=9):
    payload["page"] = page
    res = scraper.post(BASE_URL, params={"size": size}, json=payload)
    try:
        return res.json()
    except:
        return None

def get_all_ids(max_pages=5):
    ids = []
    for page in range(max_pages):
        data = fetch_profiles(page)
        if not data or not data.get("content"):
            break
        ids.extend([x["id"] for x in data["content"]])
        time.sleep(1)
    return ids

def fetch_profile_details(ids):
    profiles = []
    for sid in ids:
        res = scraper.get(PROFILE_URL.format(sid))
        if res.status_code == 200:
            try:
                profiles.append(res.json())
            except:
                pass
        time.sleep(0.5)
    return profiles

def clean_profiles(all_profiles):
    cleaned = []

    for p in all_profiles:
        user = p.get("user", {})
        startup = user.get("startup", {})

        website = startup.get("website")

        if not website or website.lower() in ["na", "n/a", "none", "", "only mobile app"]:
            continue

        industry = None
        if startup.get("focusArea") and startup["focusArea"].get("industry"):
            industry = startup["focusArea"]["industry"].get("industryName")

        cleaned.append({
            "name": user.get("name"),
            "idea": startup.get("ideaBrief"),
            "website": website,
            "industry": industry
        })

    return pd.DataFrame(cleaned)