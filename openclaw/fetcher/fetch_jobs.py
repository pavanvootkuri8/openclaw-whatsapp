import os
import yaml
import requests

OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/app/data/jobs.yaml")

GREENHOUSE_COMPANIES = [
    c.strip() for c in os.getenv("GREENHOUSE_COMPANIES", "").split(",") if c.strip()
]
LEVER_COMPANIES = [
    c.strip() for c in os.getenv("LEVER_COMPANIES", "").split(",") if c.strip()
]

KEYWORDS = [k.strip().lower() for k in os.getenv("JOB_KEYWORDS", "").split(",") if k.strip()]
EXCLUDE = [k.strip().lower() for k in os.getenv("JOB_EXCLUDE", "").split(",") if k.strip()]
LOCATIONS = [l.strip().lower() for l in os.getenv("JOB_LOCATIONS", "").split(",") if l.strip()]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def normalize_job(title, company, location, url):
    return {
        "title": title or "N/A",
        "company": company or "N/A",
        "location": location or "N/A",
        "url": url or "",
    }


def match_filters(job):
    text = f"{job['title']} {job['company']} {job['location']}".lower()

    if KEYWORDS and not any(k in text for k in KEYWORDS):
        return False

    if EXCLUDE and any(k in text for k in EXCLUDE):
        return False

    if LOCATIONS and not any(l in text for l in LOCATIONS):
        return False

    return True


def fetch_greenhouse(company):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()

    jobs = []
    for job in data.get("jobs", []):
        jobs.append(
            normalize_job(
                title=job.get("title"),
                company=company,
                location=(job.get("location") or {}).get("name", "N/A"),
                url=job.get("absolute_url"),
            )
        )
    return jobs


def fetch_lever(company):
    url = f"https://api.lever.co/v0/postings/{company}?mode=json"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()

    jobs = []
    for job in data:
        categories = job.get("categories", {}) or {}
        location = categories.get("location", "N/A")
        jobs.append(
            normalize_job(
                title=job.get("text"),
                company=company,
                location=location,
                url=job.get("hostedUrl"),
            )
        )
    return jobs


def dedup_jobs(jobs):
    seen = set()
    result = []
    for job in jobs:
        url = job.get("url")
        if url and url not in seen:
            seen.add(url)
            result.append(job)
    return result


def main():
    all_jobs = []

    for company in GREENHOUSE_COMPANIES:
        try:
            all_jobs.extend(fetch_greenhouse(company))
        except Exception as e:
            print(f"Greenhouse fetch failed for {company}: {e}")

    for company in LEVER_COMPANIES:
        try:
            all_jobs.extend(fetch_lever(company))
        except Exception as e:
            print(f"Lever fetch failed for {company}: {e}")

    all_jobs = dedup_jobs(all_jobs)
    all_jobs = [job for job in all_jobs if match_filters(job)]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        yaml.safe_dump(all_jobs, f, sort_keys=False, allow_unicode=True)

    print(f"Wrote {len(all_jobs)} jobs to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
