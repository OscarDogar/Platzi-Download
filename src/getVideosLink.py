import os
from pathlib import Path
import json
import re
import config
from utils import extract_field
from convertHTML2MD import convert_html_to_markdown


def validate_if_video_exist_in_json(name):
    """
    Check if a video with the given name exists in the videos JSON file.

    Args:
        name (str): The name of the video to search for.

    Returns:
        bool:   True if a video with the given name exists in the JSON file,
                False if the file doesn't exist or the video is not found.
    """
    if not os.path.exists(config.FULL_PATH_VIDEOS):
        return False
    with open(config.FULL_PATH_VIDEOS, "r", encoding="utf-8") as f:
        videos = json.load(f)
    for video in videos:
        if video["name"] == name:
            return True
    return False


def getVideos():
    """
    Collect video metadata from HTML response files.

    This function scans all `.html` files in `config.FULL_PATH_HTML`, extracts
    `media_url` and `materialId` values, and builds a list of video entries for
    files not already present in the videos JSON source (as determined by
    `validate_if_video_exist_in_json`).

    Behavior:
    - Skips HTML files whose stem already exists in the JSON index.
    - Removes any previously accumulated entry with the same name before appending
        a newly parsed one.
    - Appends a dictionary for each valid file:
        `{"name": <filename_without_ext>, "url": <media_url>, "materialId": <materialId>}`.
    - Deletes the HTML file if no `media_url` is found, to avoid reprocessing.

    Returns:
            list[dict]: A list of video metadata dictionaries discovered during the scan.

    Side Effects:
            - Reads files from `config.FULL_PATH_HTML`.
            - Deletes HTML files that do not contain a `media_url`.
    """
    # Open html files in responses folder
    video_links = []
    for html_file in Path(config.FULL_PATH_HTML).glob("*.html"):
        with open(html_file, "r", encoding="utf-8") as f:
            if validate_if_video_exist_in_json(html_file.stem):
                # print(f"[SKIP] {html_file.name} (already in videos.json)")
                continue
            html = f.read()
            video_links = [v for v in video_links if v["name"] != html_file.stem]
            media_url = extract_field(html, "media_url")
            materialId = extract_field(html, "materialId")
            class_number = html_file.stem.split(".")[
                0
            ]  # Assuming the format is "01_Class_Name.html"
            if media_url:
                if "m3u8" not in media_url:
                    pattern = r"https:\/\/api\.platzi\.com\/mdstrm\/v1\/video\/.*?\.m3u8.*?(?=(?:2a|29):)"
                    match = re.search(pattern, html, re.DOTALL)
                    if match:
                        media_url = match.group(0).replace("\\/", "/")
                        media_url = re.sub(
                            r'"\]\)</script><script>self\.__next_f\.push\(\[1,"',
                            "",
                            media_url,
                        )
                        (
                            print(
                                f"⚠️  [WARN] The media_url for {html_file.name} has been updated to {media_url}"
                            )
                            if config.SHOW_DOWNLOAD_LOGS == "y"
                            else None
                        )
                video_links.append(
                    {
                        "name": html_file.stem,
                        "url": media_url,
                        "materialId": materialId,
                        "class_number": class_number,
                    }
                )
            else:
                # check if it is a lecture
                convert_html_to_markdown(
                    html,
                    "Lecture_Lecture",
                    f"{config.FULL_PATH}/{html_file.stem} Class Lecture",
                )
                # delete the html file if no media_url is found to avoid processing it again in the future
                os.remove(html_file)
            convert_html_to_markdown(
                html,
                "Resources_Resources__section__",
                f"{config.FULL_PATH_RESOURCES}/{class_number}. Class Summary Lecture",
            )
    return video_links


def openVideoLinks():
    """
    Open and save video links to a file.

    Retrieves a list of videos using getVideos() and writes them to a JSON file
    specified in config.FULL_PATH_VIDEOS. If no videos are found, prints a message
    and returns early without creating the file.

    Returns:
        None
    """
    videos = getVideos()
    if not videos:
        print("No new video links found.")
        return
    with open(config.FULL_PATH_VIDEOS, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=4, ensure_ascii=False)
