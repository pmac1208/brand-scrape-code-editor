import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time



# List of retailer URLs (replace with your own)
urls = [
    "https://pinnaclefirearmsandtraining.com/",
    # Add more like "https://dealer1.com", "https://jewelryshop.com", etc.
]

def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc == base_domain

def get_all_text(url, max_pages=25):
    visited = set()
    queue = [url]
    domain = urlparse(url).netloc
    collected_text = []
    image_texts = []

    while queue and len(visited) < max_pages:
        current_url = queue.pop(0)
        if current_url in visited:
            continue

        try:
            res = requests.get(current_url, timeout=10)
            soup = BeautifulSoup(res.text, "lxml")
            visited.add(current_url)

            # Extract visible page text
            collected_text.append(soup.get_text(separator=" ", strip=True))

            # 👇 NEW: Extract possible brand names from images
            for img in soup.find_all("img"):
                alt = img.get("alt", "")
                src = img.get("src", "")
                for text in [alt, src]:
                    if any(char.isalpha() for char in text):
                        cleaned = (
                            text.split("/")[-1].split(".")[0]
                            .replace("-", " ")
                            .replace("_", " ")
                            .strip()
                        )
                        if cleaned and len(cleaned) > 2:
                            image_texts.append(cleaned)

            # Crawl internal links
            for a_tag in soup.find_all("a", href=True):
                link = urljoin(current_url, a_tag["href"])
                if urlparse(link).netloc == domain and link not in visited:
                    queue.append(link)

        except Exception as e:
            print(f"Error on {current_url}: {e}")
            continue

    # Combine text and image brand guesses
    return "\n".join(collected_text + image_texts)


# Loop through all input URLs
for site in urls:
    print(f"\n🔍 Scraping: {site}")
    raw_text = get_all_text(site)
    
    # Save each site's text to a file
    filename = urlparse(site).netloc.replace('.', '_') + "_text.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(raw_text)

    print(f"✅ Finished. Saved raw text to {filename}")
    time.sleep(2)  # polite delay

def get_logo_images(url):
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.text, "lxml")
        images = []

        for img in soup.find_all("img"):
            src = img.get("src")
            alt = img.get("alt", "")
            if src and ("logo" in src.lower() or "brand" in src.lower() or "logo" in alt.lower()):
                full_url = urljoin(url, src)
                images.append(full_url)

        return images
    except Exception as e:
        print(f"Error collecting images from {url}: {e}")
        return []

if __name__ == "__main__":
    test_url = "https://pinnaclefirearmsandtraining.com/"
    logo_urls = get_logo_images(test_url)
    print("\nLogo Images Found:")
    for img in logo_urls:
        print(img)
