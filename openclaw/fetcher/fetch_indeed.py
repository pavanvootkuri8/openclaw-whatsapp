import os
import time
import yaml
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin

BASE_URL = "https://www.indeed.com/jobs"

QUERY = os.getenv("INDEED_QUERY", "Site Reliability Engineer")
LOCATION = os.getenv("INDEED_LOCATION", "Remote")
LIMIT = int(os.getenv("INDEED_LIMIT", "20"))
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/app/data/jobs.yaml")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def fetch_jobs():
    params = {
        "q": QUERY,
        "l": LOCATION,
    }

    url = f"{BASE_URL}?{urlencode(params)}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []

    # Indeed markup changes over time, so keep selectors flexible
    cards = soup.select("div.job_seen_beacon, div.slider_container div[data-jk], a.tapItem")
    seen_urls = set()

    for card in cards:
        title = None
        company = None
        location = None
        job_url = None

        link = card.select_one("a.jcs-JobTitle, h2.jobTitle a, a.tapItem")
        if link:
            title = link.get_text(" ", strip=True)
            href = link.get("href")
            if href:
                job_url = urljoin("https://www.indeed.com", href)

        company_el = card.select_one("[data-testid='company-name'], span.companyName")
        if company_el:
            company = company_el.get_text(" ", strip=True)

        location_el = card.select_one("[data-testid='text-location'], div.companyLocation")
        if location_el:
            location = location_el.get_text(" ", strip=True)

        if job_url and job_url not in seen_urls:
            seen_urls.add(job_url)
            jobs.append({
                "title": title or "N/A",
                "company": company or "N/A",
                "location": location or "N/A",
                "url": job_url,
            })

        if len(jobs) >= LIMIT:
            break

    return jobs

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    jobs = fetch_jobs()
    with open(OUTPUT_PATH, "w") as f:
        yaml.safe_dump(jobs, f, sort_keys=False, allow_unicode=True)
    print(f"Wrote {len(jobs)} jobs to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
