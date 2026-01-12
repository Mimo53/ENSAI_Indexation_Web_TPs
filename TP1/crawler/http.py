import urllib.request
import urllib.error

def fetch_html(url, user_agent="MyCrawler"):
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": user_agent}
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status == 200:
                return response.read()
    except urllib.error.URLError:
        return None
