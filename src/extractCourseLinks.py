import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import config
from utils import extract_field, generate_course_md
from validateHtml import validate_html
from datetime import datetime


def download_image(img_url, filename):
    """
    Download an image from a URL and save it to a file.

    Checks if the file already exists to avoid re-downloading.
    If the file exists, the function returns without performing any action.
    Otherwise, it fetches the image from the provided URL and writes it to disk.

    Args:
        img_url (str): The URL of the image to download.
        filename (str): The file path where the image should be saved.

    Returns:
        None

    Raises:
        requests.RequestException: If the HTTP request fails.
        IOError: If the file cannot be written to disk.
    """
    # Validate if image exists in folder
    if os.path.exists(filename):
        return
    referer = None

    if "imgur.com" in img_url:
        referer = "https://imgur.com/"
    elif "platzi.com" in img_url:
        referer = "https://platzi.com/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/136.0.0.0 Safari/537.36"
        ),
    }
    if referer:
        headers["Referer"] = referer
    response = requests.get(img_url, headers=headers, timeout=20)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)

        print("🖼️  Course Image Downloaded")
    else:
        print(f"Failed to download course image. Status code: {response.status_code}")


def cleanName(name):
    """
    Remove invalid characters from a string to make it suitable for use as a filename.

    Args:
        name (str): The string to clean.

    Returns:
        str: The cleaned string with invalid filename characters removed and whitespace stripped.
    """
    # Remove invalid characters for filenames
    name = re.sub(r'[\\/*?:¿"<>|]', "", name)
    return name.strip()


def extractLinksFromPage(html, url):
    """
    Extract course links and metadata from a Platzi course page HTML.

    Parses the HTML content to extract course links, class names, and metadata.
    Creates necessary directories, downloads the course thumbnail image, and saves
    all links with their corresponding names to a file.

    Args:
        html (str): The HTML content of a Platzi course page.

    Returns:
        tuple: A tuple containing:
            - names (list): List of cleaned class/section names extracted from the page.
            - links (list): List of absolute URLs for the course content items.

    Side Effects:
        - Creates directories specified in config.FULL_PATH and config.FULL_PATH_LINKS.
        - Downloads and saves the course thumbnail image as 'course_image.jpg'.
        - Writes extracted links and names to 'links.txt' file in config.FULL_PATH_LINKS.
        - Updates the dynamic course name in config with the course title and year.
        - Prints the total number of classes extracted.
    """
    base = "https://platzi.com"

    soup = BeautifulSoup(html, "html.parser")
    links = [
        urljoin(base, a["href"])
        for a in soup.select('a[class*="ItemLink-module_ItemLink"]')
    ]
    names = [
        cleanName(a.get_text(strip=True))
        for a in soup.select('h3[class*="SyllabusSection-module_Item__Title"]')
    ]
    courseName = soup.select_one("h1").get_text(strip=True)
    raw_date = extract_field(html, "launch_date")
    dt = None
    if raw_date:
        dt = datetime.fromisoformat(raw_date)

    launch_date = dt.strftime(config.COURSE_NAME_DATE_FORMAT) if dt else None
    # launch_date = raw_date.split("T")[0] if raw_date else None
    description = soup.select_one(
        'p[class*="CourseInfo_CourseInfo__Description"]'
    ).get_text(strip=True)
    #! THE ORDER OF THE TAGS IS NOT GUARANTEED, SO THIS MAY CAUSE ISSUES IN THE FUTURE
    tags = soup.select('div[class*="CourseTags_CourseTags__Tag"]')

    level = tags[0].get_text(strip=True) if len(tags) > 0 else None
    number_of_classes = tags[1].get_text(strip=True) if len(tags) > 1 else None
    duration_content = tags[2].get_text(strip=True) if len(tags) > 2 else None
    professors_tag = soup.select_one('p[class*="CourseTeacher_CourseTeacher__Name"]')
    professors = professors_tag.get_text(strip=True) if professors_tag else None

    professors_img_tag = soup.select_one(
        'img[class*="CourseTeacher_CourseTeacher__Image"]'
    )
    professors_img = (
        professors_img_tag["src"]
        if professors_img_tag and professors_img_tag.has_attr("src")
        else None
    )

    professors_description_tag = soup.select_one(
        'p[class*="CourseTeacher_CourseTeacher__Description"]'
    )
    professors_description = (
        professors_description_tag.get_text(strip=True)
        if professors_description_tag
        else None
    )

    reviews_tag = soup.select_one(
        'span[class*="CourseMetrics_CourseMetrics__Stars__Number"]'
    )
    reviews = reviews_tag.get_text(strip=True) if reviews_tag else None

    config.COURSE_ID = extract_field(html, "courseId")
    # get year from launch_date
    if launch_date:
        # year = launch_date.split("-")[0]
        courseName += f" ({launch_date})"
    if courseName:
        config.set_dynamic_name(cleanName(courseName))
    print(f"⬇️  Starting download: {courseName}")
    os.makedirs(config.FULL_PATH, exist_ok=True)
    os.makedirs(config.FULL_PATH_LINKS, exist_ok=True)
    generate_course_md(
        courseName,
        dt.strftime("%B %d, %Y") if raw_date else None,
        description,
        level,
        number_of_classes,
        duration_content,
        professors,
        professors_img,
        professors_description,
        reviews,
        url,
        os.path.join(config.FULL_PATH, "course_info.md"),
    )
    img = soup.find("meta", property="og:image")["content"] if soup.find("meta", property="og:image") else extract_field(html, "thumbnail_url") 
    if img:
        download_image(img, os.path.join(config.FULL_PATH, "course_image.jpg"))
    # Save links in a file in the config.FULL_PATH_LINKS
    with open(
        os.path.join(config.FULL_PATH_LINKS, "links.txt"), "w", encoding="utf-8"
    ) as f:
        for link, name in zip(links, names):
            f.write(f"{name}; {link}\n")
    print(f"Total Classes: {len(links)}")
    return names, links


def getLinks(url):
    """
    Fetch course links from a Platzi course page.

    Establishes a requests session with configured cookies and headers,
    retrieves the course page content, and extracts all links from it.

    Returns:
        list: A list of links extracted from the course page.

    Raises:
        Prints an error message to console if any exception occurs during
        the HTTP request or link extraction process.

    Note:
        - Uses cookies from config.COOKIES for authentication
        - Implements a 20 second timeout for the HTTP request
        - Validates response status with raise_for_status()
    """
    try:
        session = requests.Session()
        # Cookies
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
        validate_html(html)
        return extractLinksFromPage(html, url)
    except requests.RequestException as e:
        print("An exception occurred while fetching the page.")
        os._exit(1)
    except Exception as e:
        print(str(e))
        os._exit(1)
