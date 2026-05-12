import os
from dotenv import load_dotenv

# Headers
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "es-ES,es;q=0.9",
    "Referer": "https://platzi.com/",
    "Connection": "keep-alive",
}

load_dotenv()  # Load environment variables from .env file
KEEP_TMP_FILES = os.environ.get("KEEP_TMP_FILES", "N").lower()
DOWNLOAD_RESOURCES = os.environ.get("DOWNLOAD_RESOURCES", "Y").lower()
SHOW_DOWNLOAD_LOGS = os.environ.get("SHOW_DOWNLOAD_LOGS", "N").lower()
LECTURES_FORMAT_DOWNLOAD = os.environ.get("LECTURES_FORMAT_DOWNLOAD", "PDF").lower()
COURSE_NAME_DATE_FORMAT = os.environ.get("COURSE_NAME_DATE_FORMAT", "%Y")


def validate_config():
    if KEEP_TMP_FILES not in ("y", "n"):
        raise ValueError("KEEP_TMP_FILES must be 'y' or 'n'")
    if DOWNLOAD_RESOURCES not in ("y", "n"):
        raise ValueError("DOWNLOAD_RESOURCES must be 'y' or 'n'")
    if SHOW_DOWNLOAD_LOGS not in ("y", "n"):
        raise ValueError("SHOW_DOWNLOAD_LOGS must be 'y' or 'n'")
    if LECTURES_FORMAT_DOWNLOAD not in ("md", "pdf"):
        raise ValueError("LECTURES_FORMAT_DOWNLOAD must be 'md' or 'pdf'")


try:
    VIDEO_DOWNLOAD_MAX_PARALLEL = int(os.getenv("VIDEO_DOWNLOAD_MAX_PARALLEL", "1"))
    VIDEO_DOWNLOAD_BATCH_SIZE = int(os.getenv("VIDEO_DOWNLOAD_BATCH_SIZE", "30"))
    VIDEO_DOWNLOAD_COOLDOWN = int(os.getenv("VIDEO_DOWNLOAD_COOLDOWN", "10"))
    VIDEO_DOWNLOAD_START_DELAY = float(os.getenv("VIDEO_DOWNLOAD_START_DELAY", "0.5"))
    VIDEO_DOWNLOAD_LIMIT_RATE = os.getenv("VIDEO_DOWNLOAD_LIMIT_RATE", "100M")
    VIDEO_DOWNLOAD_CONCURRENT_FRAGMENTS = os.getenv(
        "VIDEO_DOWNLOAD_CONCURRENT_FRAGMENTS", "3"
    )
    VIDEO_DOWNLOAD_FRAGMENT_RETRIES = os.getenv("VIDEO_DOWNLOAD_FRAGMENT_RETRIES", "20")
    VIDEO_DOWNLOAD_RETRIES = os.getenv("VIDEO_DOWNLOAD_RETRIES", "20")
    VIDEO_DOWNLOAD_RETRY_SLEEP = os.getenv("VIDEO_DOWNLOAD_RETRY_SLEEP", "exp=1:20")
    VIDEO_DOWNLOAD_SLEEP_REQUESTS = os.getenv("VIDEO_DOWNLOAD_SLEEP_REQUESTS", "0")
except Exception as e:
    print(f"Invalid environment configuration for video download settings: {e}")
    os._exit(1)


try:
    COOKIES = {
        "s": os.environ["COOKIE"],
    }
except KeyError:
    raise RuntimeError("COOKIE environment variable is not set")

COURSE_URL = os.environ.get("COURSE_URL")
# convert COURSE_URL to a list if it contains multiple URLs separated by commas
if COURSE_URL:
    COURSE_URL = [url.strip() for url in COURSE_URL.split(",")]
else:
    raise RuntimeError("COURSE_URL environment variable is not set")

COURSE_ID = None

BASE_FOLDER = "Videos"
DYNAMIC_NAME = None
FULL_PATH = None


def set_dynamic_name(name):
    """
    Set the dynamic name and update all related path variables.

    This function sets the DYNAMIC_NAME and updates all global path variables
    (FULL_PATH, FULL_PATH_HTML, FULL_PATH_LINKS, FULL_PATH_VIDEOS) based on the
    provided name parameter.

    Args:
        name (str): The dynamic name to set, used as a subdirectory under BASE_FOLDER.

    Global Variables Modified:
        DYNAMIC_NAME (str): The dynamic name identifier.
        FULL_PATH (str): Base path constructed as {BASE_FOLDER}/{DYNAMIC_NAME}.
        FULL_PATH_LINKS (str): Path to video links directory.
        FULL_PATH_HTML (str): Path to HTML responses directory.
        FULL_PATH_VIDEOS (str): Path to videos.json file.
        FULL_PATH_RESOURCES (str): Path to resources directory.
    """
    global DYNAMIC_NAME, FULL_PATH, FULL_PATH_HTML, FULL_PATH_LINKS, FULL_PATH_VIDEOS, FULL_PATH_RESOURCES
    DYNAMIC_NAME = name
    FULL_PATH = f"{BASE_FOLDER}/{DYNAMIC_NAME}"
    FULL_PATH_LINKS = FULL_PATH + "/VideosLinks"
    FULL_PATH_HTML = FULL_PATH + "/responses"
    FULL_PATH_VIDEOS = FULL_PATH + "/videos.json"
    FULL_PATH_RESOURCES = FULL_PATH + "/resources"
