"""
Author: OscarDogar
Main entry point for the course video downloader application.

This script orchestrates a multi-step process to download course videos:
    1. Extracts course links from a source and saves them to a configured path
    2. Opens all links asynchronously in batches and caches HTML responses
    3. Parses HTML files to extract video links and saves them as JSON
    4. Downloads course resources (if enabled via DOWNLOAD_RESOURCES environment variable)
    5. Downloads all videos from the extracted links
    6. Validates successful download completion and cleans up temporary files

Environment Variables:
    DOWNLOAD_RESOURCES (str): Set to "y" to enable resource downloads. Defaults to "y".

The script expects the following modules to be available:
    - extractCourseLinks: For extracting course links
    - openLinks: For asynchronously fetching and caching HTML
    - getVideosLink: For parsing video links from HTML
    - downloadVideos: For downloading video files
    - downloadResourses: For downloading course resources (optional)
    - utils: For utility functions (counting downloads, cleaning temporary files)

Exit Behavior:
    - Prints success message if all videos are downloaded
    - Prints warning with download count if some videos failed
    - Cleans up temporary files on successful completion
    - Suggests re-running the script if videos are missing
"""

import asyncio
import sys
import os
from extractCourseLinks import getLinks
from extractRouteLinks import is_route_url, getRouteCourseLinks
from openLinks import openLinks
import config
from getVideosLink import openVideoLinks
from downloadVideos import download_videos
from utils import clickable_link, count_download_videos, delete_tmp_files, menu


def process_course(url: str) -> None:
    """
    Process a single course URL:
    1. Extract lesson links
    2. Fetch HTML content
    3. Extract video URLs
    4. Download resources
    5. Download videos
    6. Validate downloads and clean temporary files
    """
    print(f"\n📚 Processing course: {url}")
    # 1. Extract course links
    names, links = getLinks(url)
    # 2. Fetch HTML responses
    asyncio.run(openLinks(links, names))
    # 3. Extract video links
    openVideoLinks()
    # 4. Download resources
    if config.DOWNLOAD_RESOURCES.lower() == "y":
        from downloadResourses import download_resources

        download_resources()
    # 5. Download videos
    download_videos()
    # 6. Validate downloads
    mp4_files, html_files = count_download_videos()
    if mp4_files == html_files:
        delete_tmp_files()
    else:
        print(f"\n⚠️ Download incomplete: {mp4_files}/{html_files} videos downloaded.")
        print("You can run the script again to retry missing downloads.")


def process_route(url: str) -> None:
    print(f"\n🛤️  Processing route: {url}")
    route_name, course_urls = getRouteCourseLinks(url)
    config.set_route_name(route_name)
    try:
        for course_url in course_urls:
            process_course(course_url)
    finally:
        config.set_route_name(None)


def main() -> None:
    """
    Main entry point for the application.
    """
    try:
        menu()
        config.validate_config()
        for url in config.COURSE_URL:
            if is_route_url(url):
                process_route(url)
            else:
                process_course(url)
        print("\n🚀 All done!")
        print(
            clickable_link(
                "\n❤️  If it was helpful, consider supporting it ❤️\n",
                "https://github.com/sponsors/OscarDogar",
                "4;32",
            )
        )
    except ValueError as error:
        print(f"\n❌ ValueError: {error}")
    except RuntimeError as error:
        print(f"\n❌ RuntimeError: {error}")
    except KeyboardInterrupt:
        print("\n\n⛔ Process interrupted by user.")
    except Exception as error:
        print(f"\n❌ Unexpected error: {error}")


if __name__ == "__main__":
    # region Adjust PATH for frozen executable (e.g., PyInstaller)
    if getattr(sys, "frozen", False):
        meipass = sys.__dict__.get("_MEIPASS")
        if meipass:
            os.environ["PATH"] = meipass + os.pathsep + os.environ.get("PATH", "")
    # endregion
    main()
