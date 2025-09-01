import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import quote_plus
import time

HEADERS = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
	"Accept-Language": "en-US,en;q=0.9",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	"Connection": "keep-alive",
	"Referer": "https://www.timesjobs.com/",
}

TIMESJOBS_URL = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={k}&txtLocation={l}&sequence=1&startPage=1"

DEBUG_DIR = os.path.join("data", "debug")
os.makedirs(DEBUG_DIR, exist_ok=True)


def _save_debug_html(name: str, content: str) -> str:
	path = os.path.join(DEBUG_DIR, f"{name}.html")
	try:
		with open(path, "w", encoding="utf-8") as f:
			f.write(content)
		print(f"[TimesJobs][DEBUG] Saved HTML: {path}")
	except Exception as e:
		print(f"[TimesJobs][DEBUG] Failed to save HTML: {e}")
	return path


def _fetch_timesjobs(url: str, *, save_name: str = "timesjobs_last") -> BeautifulSoup:
	resp = requests.get(url, headers=HEADERS, timeout=20)
	resp.raise_for_status()
	soup = BeautifulSoup(resp.text, 'html.parser')
	_save_debug_html(save_name, soup.prettify())
	return soup


def _parse_timesjobs(soup: BeautifulSoup, max_results: int) -> List[Dict]:
	results: List[Dict] = []
	cards = soup.select('ul.new-joblist > li.clearfix') or soup.select('li.clearfix.job-bx')
	for li in cards:
		title_tag = li.select_one('h2 a') or li.select_one('h3 a')
		company_tag = li.select_one('h3.joblist-comp-name') or li.select_one('.company-name')
		
		job_location = ""
		job_posted_date = ""
		
		location_tru_tag = li.select_one('li.srp-zindex.location-tru')
		if location_tru_tag and 'title' in location_tru_tag.attrs:
			job_location = location_tru_tag['title']
		else:
			loc_tag = li.select_one('ul.top-jd-dtl li span')
			if loc_tag:
				job_location = loc_tag.get_text(strip=True)

		posted_tag = li.select_one('span.sim-posted')
		if posted_tag:
			job_posted_date = posted_tag.get_text(strip=True)
		
		snippet_tag = li.select_one('.list-job-dtl p') or li.select_one('.job-description')
		link = title_tag.get('href') if title_tag else None
		title = title_tag.get_text(strip=True) if title_tag else None
		company = company_tag.get_text(strip=True) if company_tag else None
		snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ''
		if title and link:
			results.append({
				"title": title,
				"company": company,
				"location": job_location, 
				"link": link,
				"snippet": snippet,
				"date": job_posted_date,
			})
			if len(results) >= max_results:
				break
	return results


def search_timesjobs_jobs(query: str, location: str = "", page: int = 1, max_results: int = 20) -> List[Dict]:
	url = TIMESJOBS_URL.format(k=quote_plus(query or ''), l=quote_plus(location or ''))
	soup = _fetch_timesjobs(url, save_name="timesjobs_last")
	results = _parse_timesjobs(soup, max_results)
	if results:
		print(f"[TimesJobs] Found {len(results)} results")
		return results
	print("[TimesJobs] No results found")
	return []
