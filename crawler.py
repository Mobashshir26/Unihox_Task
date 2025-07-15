import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ✅ Domains that need Selenium
JS_HEAVY_DOMAINS = [
    "indianculture.gov.in",
    "indianmanuscripts.com"
]

def crawl_site(url):
    domain = url.split("/")[2]
    if domain in JS_HEAVY_DOMAINS:
        return crawl_with_selenium(url)
    else:
        return crawl_with_requests(url)

# ✅ Basic requests + BeautifulSoup crawler for static sites
def crawl_with_requests(base_url):
    visited = set()
    to_visit = [base_url]
    file_links = []

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        try:
            print(f"🔎 Visiting: {url}")
            time.sleep(1.5)
            r = requests.get(url, timeout=15)
            visited.add(url)
            soup = BeautifulSoup(r.content, "lxml")

            for a in soup.find_all("a", href=True):
                href = a["href"]
                full_url = urljoin(url, href)

                if href.endswith((".pdf", ".epub", ".html")):
                    file_links.append(full_url)
                elif base_url in full_url:
                    to_visit.append(full_url)
        except Exception as e:
            print(f"❌ Error crawling {url}: {e}")

    return list(set(file_links))

# ✅ Selenium for JavaScript-heavy websites
def crawl_with_selenium(url):
    print(f"🌐 Using Selenium for: {url}")
    file_links = []

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.get(url)
        time.sleep(5)  # Allow JS to load

        elements = driver.find_elements("tag name", "a")
        for elem in elements:
            href = elem.get_attribute("href")
            if href and href.endswith((".pdf", ".epub", ".html")):
                file_links.append(href)

        driver.quit()
    except Exception as e:
        print(f"❌ Selenium failed on {url}: {e}")
    return list(set(file_links))
