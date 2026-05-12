import json
import os
import config
from getToken import TOKEN
import requests


def save_links_to_file(links, videoInfo):
    if links:
        txt_file_path = os.path.join(
            config.FULL_PATH_RESOURCES,
            f"{videoInfo['class_number']}. Lecturas Recomendadas.txt",
        )
        # check if the file already exists to avoid downloading it again
        if os.path.exists(txt_file_path):
            # print(f"Recommended reading links for {videoInfo['name']} already exist. Skipping download.")
            return
        # save links in a file
        with open(
            txt_file_path,
            "w",
            encoding="utf-8",
        ) as f:
            print(f"Saving recommended reading links for {videoInfo['name']}...")
            for resource in links:
                f.write(f"{resource['title']}: {resource['link']}\n")


def save_files_from_url(files, videoInfo, newHeaders):
    if files:
        for resource in files:
            file_url = resource.get("archive")
            if not file_url:
                print(
                    f"Warning: No URL found for resource '{resource['name']}' in {videoInfo['name']}. Skipping this resource."
                )
                continue
            filename = os.path.join(
                config.FULL_PATH_RESOURCES,
                f"{videoInfo['class_number']}. {resource['name']}",
            )
            # check if the file already exists to avoid downloading it again
            if os.path.exists(filename):
                continue
            file_response = requests.get(file_url, headers=newHeaders)
            file_response.raise_for_status()
            with open(filename, "wb") as f:
                f.write(file_response.content)
            print(f"Downloaded resource '{resource['name']}' for {videoInfo['name']}.")


def download_resources_by_class(videoInfo):
    """
    Download educational resources (links and files) for a given video lecture.

    This function checks if resources already exist locally to avoid redundant downloads.
    If not present, it fetches recommended reading links and associated files from the
    Platzi API and saves them to the local resources directory.

    Args:
        videoInfo (dict): A dictionary containing video information with the following keys:
            - 'name' (str): The name of the video/lecture used for file naming.
            - 'materialId' (str, optional): The material ID required to fetch resources from the API.

    Returns:
        None

    Raises:
        requests.RequestException: Caught and printed if API request or file download fails.

    Side Effects:
        - Creates a text file with recommended reading links named "{videoInfo['name']}_Lecturas_Recomendadas.txt"
        - Downloads and saves resource files with names formatted as "{videoInfo['name']}_{resource['name']}"
        - Creates the FULL_PATH_RESOURCES directory if it doesn't exist
        - Prints warning messages if required data is missing or download errors occur
        - Prints success messages when resources are downloaded

    Requires:
        - TOKEN: Global variable containing the API bearer token
        - COURSE_ID: Global variable containing the course ID
        - FULL_PATH_RESOURCES: Global variable containing the path to store resources
        - headers: Global variable with default HTTP headers
    """
    if not videoInfo.get("materialId"):
        print(
            f"Warning: No materialId found for {videoInfo['name']}. Skipping resource download."
        )
        return
    if not TOKEN:
        print("Error: No valid token available. Cannot download resources.")
        return
    if not config.COURSE_ID:
        print("Error: COURSE_ID not set in config. Cannot download resources.")
        return
    resoursesURL = f"https://api.platzi.com/materials/v1/{videoInfo['materialId']}/course/{config.COURSE_ID}/links-files/"
    newHeaders = config.headers.copy()
    newHeaders.pop("Accept", None)
    newHeaders["Authorization"] = f"Bearer {TOKEN}"
    try:
        response = requests.get(resoursesURL, headers=newHeaders)
        response.raise_for_status()
        resources = response.json().get("data", [])
        if not resources["links"] and not resources["files"]:
            # print(f"No resources found for {videoInfo['name']}.")
            return
        os.makedirs(config.FULL_PATH_RESOURCES, exist_ok=True)
        save_links_to_file(resources["links"], videoInfo)
        save_files_from_url(resources["files"], videoInfo, newHeaders)
    except requests.RequestException as e:
        print(f"Error fetching resources for {videoInfo['name']}: {e}")


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
    except:
        print(
            f"Error loading videos from {config.FULL_PATH_VIDEOS}. Ensure the file exists and is properly formatted."
        )
