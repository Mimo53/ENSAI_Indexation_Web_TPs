def prioritize_links(links):
    priority_links = []
    normal_links = []

    for link in links:
        if "product" in link["url"].lower():
            priority_links.append(link)
        else:
            normal_links.append(link)

    return priority_links + normal_links
