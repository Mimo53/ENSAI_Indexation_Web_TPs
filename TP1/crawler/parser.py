import urllib.parse
from bs4 import BeautifulSoup

def is_internal_link(base_url, link):
    return urllib.parse.urlparse(base_url).netloc == urllib.parse.urlparse(link).netloc

def parse_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title else ""

    first_paragraph = ""
    p = soup.find("p")
    if p:
        first_paragraph = p.get_text(strip=True)

    links = []
    for a in soup.find_all("a", href=True):
        absolute_url = urllib.parse.urljoin(base_url, a["href"])
        if is_internal_link(base_url, absolute_url):
            links.append({
                "url": absolute_url,
                "from": base_url
            })

    return title, first_paragraph, links
