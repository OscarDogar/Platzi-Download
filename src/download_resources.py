
"""Download and save recommended links and files for Platzi course resources."""
import json
import os
import requests
import config
from get_token import TOKEN


def save_links_to_file(links, video_info):
    """Save recommended reading links to a text file."""
    if not links:
        return

    txt_file_path = os.path.join(
        config.FULL_PATH_RESOURCES,
        f"{video_info['class_number']}. Lecturas Recomendadas.txt",
    )
    # Check if the file already exists to avoid downloading it again.
    if os.path.exists(txt_file_path):
        return

    with open(
        txt_file_path,
        "w",
        encoding="utf-8",
    ) as file:
        print("Saving recommended reading links for " f"{video_info['name']}...")
        for resource in links:
            file.write(f"{resource['title']}: {resource['link']}\n")


def save_files_from_url(files, video_info, new_headers):
    """Download file resources for a lesson if they are not already saved."""
    if not files:
        return

    for resource in files:
        file_url = resource.get("archive")
        if not file_url:
            print(
                "Warning: No URL found for resource "
                f"'{resource['name']}' in {video_info['name']}. "
                "Skipping this resource."
            )
            continue

        filename = os.path.join(
            config.FULL_PATH_RESOURCES,
            f"{video_info['class_number']}. {resource['name']}",
        )
        # Check if the file already exists to avoid downloading it again.
        if os.path.exists(filename):
            continue

        file_response = requests.get(
            file_url,
            headers=new_headers,
            timeout=30,
        )
        file_response.raise_for_status()

        with open(filename, "wb") as file:
            file.write(file_response.content)

        print(f"Downloaded resource '{resource['name']}' " f"for {video_info['name']}.")


def download_resources_by_class(video_info):
    """
    Download educational resources (links and files) for a given video lecture.

    This function checks if resources already exist locally to avoid redundant
    downloads. If not present, it fetches recommended reading links and
    associated files from the Platzi API and saves them to the local resources
    directory.

    Args:
        video_info (dict): A dictionary containing video information with the
            following keys:
            - 'name' (str): The name of the video/lecture used for file naming.
            - 'materialId' (str, optional): The material ID required to fetch
              resources from the API.

    Returns:
        None

    Raises:
        requests.RequestException: Caught and printed if API request or file
            download fails.

    Side Effects:
        - Creates a text file with recommended reading links named
          "{video_info['name']}_Lecturas_Recomendadas.txt"
        - Downloads and saves resource files with names formatted as
          "{video_info['name']}_{resource['name']}"
        - Creates the FULL_PATH_RESOURCES directory if it doesn't exist
        - Prints warning messages if required data is missing or download
          errors occur
        - Prints success messages when resources are downloaded

    Requires:
        - TOKEN: Global variable containing the API bearer token
        - COURSE_ID: Global variable containing the course ID
        - FULL_PATH_RESOURCES: Global variable containing the path to store
          resources
        - headers: Global variable with default HTTP headers
    """
    if not video_info.get("materialId"):
        print(
            "Warning: No materialId found for "
            f"{video_info['name']}. Skipping resource download."
        )
        return
    if not TOKEN:
        print("Error: No valid token available. Cannot download resources.")
        return
    if not config.COURSE_ID:
        print("Error: COURSE_ID not set in config. Cannot download resources.")
        return

    resources_url = (
        "https://api.platzi.com/materials/v1/"
        f"{video_info['materialId']}/course/{config.COURSE_ID}/links-files/"
    )
    new_headers = config.headers.copy()
    new_headers.pop("Accept", None)
    new_headers["Authorization"] = f"Bearer {TOKEN}"

    try:
        response = requests.get(resources_url, headers=new_headers, timeout=30)
        response.raise_for_status()
        resources = response.json().get("data") or {}
        links = resources.get("links", [])
        files = resources.get("files", [])

        if not links and not files:
            return

        os.makedirs(config.FULL_PATH_RESOURCES, exist_ok=True)
        save_links_to_file(links, video_info)
        save_files_from_url(files, video_info, new_headers)
    except requests.RequestException as exc:
        print(f"Error fetching resources for {video_info['name']}: {exc}")


def download_resources():
    """
    Load videos from a JSON file and download resources for each video.

    Reads a JSON file containing video data from FULL_PATH_VIDEOS,
    iterates through each video entry, and downloads resources
    associated with each video by calling download_resources_by_class.

    Returns:
        None
    """
    print("📚 Starting resource download...")
    try:
        with open(config.FULL_PATH_VIDEOS, "r", encoding="utf-8") as f:
            videos = json.load(f)
        for video in videos:
            download_resources_by_class(video)
        print("📚 Resource download completed.")
    except (FileNotFoundError, OSError, ValueError, TypeError) as exc:
        print(
            "Error loading videos from "
            f"{config.FULL_PATH_VIDEOS}. "
            "Ensure the file exists and is properly formatted. "
            f"Details: {exc}"
        )
