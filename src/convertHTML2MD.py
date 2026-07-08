from bs4 import BeautifulSoup
import markdownify
import os
import config
from convertMD2PDF import convert_html_to_pdf
from config import LECTURES_FORMAT_DOWNLOAD as checkFormatDownload


def convert_html_to_markdown(html, class_name, filepath):
    """
    Convert HTML content and save it as Markdown or PDF.

    Args:
        html (str): The HTML content to convert.
        class_name (str): The class name of the div element to extract.
        filepath (str): The output file path without the extension.

    Returns:
        None: This function writes the converted content to disk and does not
        return the generated Markdown content.
    """
    # Validate if the file already exists to avoid reprocessing
    filepath = f"{filepath}.md" if checkFormatDownload == "md" else f"{filepath}.pdf"
    if os.path.exists(filepath):
        return
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one(f'section[class*="{class_name}"]')
    if content is None:
        if config.SHOW_DOWNLOAD_LOGS == "y":
            print(
                f"[WARNING] Skipping conversion for {filepath.split('/')[-1]}. No content found for class '{class_name}' in HTML. "
            )
        return
    markdown_content = markdownify.markdownify(str(content), heading_style="ATX")
    # check if the directory exists, if not create it
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if checkFormatDownload == "md":
        save_markdown_to_file(markdown_content, filepath)
    elif checkFormatDownload == "pdf":
        convert_html_to_pdf(markdown_content, filepath)


def save_markdown_to_file(markdown_content, filepath):
    """
    Save Markdown content to a file.
    Args:
        markdown_content (str): The Markdown content to save.
        filepath (str): The path to the file to save the content to.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_content)