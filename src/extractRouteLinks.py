import os
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

import config
from extractCourseLinks import cleanName
from validateHtml import verify_cookie

COURSE_HREF_RE = re.compile(r'href="(/cursos/[a-zA-Z0-9\-]+/?)"')


def is_route_url(url: str) -> bool:
    return "/ruta/" in url


def getRouteCourseLinks(url: str):
    base = "https://platzi.com"
    try:
        session = requests.Session()
        for key, value in config.COOKIES.items():
            session.cookies.set(key, value, domain=".platzi.com")
        response = session.get(
            url,
            headers=config.headers,
            cookies=config.COOKIES,
            timeout=20,
        )
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        verify_cookie(soup)
    except requests.RequestException:
        print("An exception occurred while fetching the route page.")
        os._exit(1)
    except Exception as e:
        print(str(e))
        os._exit(1)

    title_tag = soup.select_one("h1")
    route_name = cleanName(title_tag.get_text(strip=True)) if title_tag else "Ruta"

    seen = set()
    course_urls = []
    for match in COURSE_HREF_RE.finditer(html):
        href = match.group(1)
        full_url = urljoin(base, href)
        if full_url not in seen:
            seen.add(full_url)
            course_urls.append(full_url)

    if not course_urls:
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/cursos/" in href:
                full_url = urljoin(base, href)
                if full_url not in seen:
                    seen.add(full_url)
                    course_urls.append(full_url)

    if not course_urls:
        print(
            "No courses were found on the route page. "
            "Platzi may have changed its page structure, or the cookie/session "
            "does not have access to this route."
        )

    print(f"Route detected: {route_name} ({len(course_urls)} courses found)")
    return route_name, course_urls
