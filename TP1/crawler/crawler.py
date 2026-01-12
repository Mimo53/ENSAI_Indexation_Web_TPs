import time
from collections import deque
from .robots import create_robot_parser, can_fetch_url
from .http import fetch_html
from .parser import parse_html
from .priority import prioritize_links


def crawl(start_url, max_pages):
    robot_parser = create_robot_parser(start_url)

    frontier = deque([start_url])
    visited = set()
    seen = set([start_url])

    results = []

    while frontier and len(visited) < max_pages:
        current_url = frontier.popleft()

        if current_url in visited:
            continue

        if not can_fetch_url(robot_parser, current_url):
            continue

        # Affichage de l'avancement du crawl
        current_count = len(visited) + 1
        print("[{}/{}] Crawling: {}".format(current_count, max_pages, current_url))

        html = fetch_html(current_url)
        if html is None:
            continue

        title, first_paragraph, links = parse_html(html, current_url)

        visited.add(current_url)

        results.append({
            "url": current_url,
            "title": title,
            "description": first_paragraph,
            "links": links
        })

        prioritized_links = prioritize_links(links)

        for link in prioritized_links:
            url = link["url"]
            if url not in seen:
                frontier.append(url)
                seen.add(url)

        time.sleep(1)  # Respect de la politesse (1 requête par seconde)

    return results
