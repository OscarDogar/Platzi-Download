"""Utilities to convert HTML content into Markdown or PDF files."""

import os
import re
import markdownify
from bs4 import BeautifulSoup
from convert_md_2_pdf import convert_html_to_pdf
import config
from config import LECTURES_FORMAT_DOWNLOAD as checkFormatDownload


def clean_markdown(markdown):
    """Fix common Markdown formatting issues generated from HTML."""

    # 1. Fix headings wrapped in bold: **### Heading** -> ### Heading
    markdown = re.sub(r"(?m)^\s*\*\*(#{1,6})\s+(.+?)\*\*\s*$", r"\1 \2", markdown)

    # 2. Fix escaped unordered list markers: \* item -> - item
    markdown = re.sub(r"(?m)^[ \t]*\\\*[ \t]+", "- ", markdown)

    # 3. Fix malformed nested Markdown links
    markdown = re.sub(
        r"\[([^\]]+)\]\(\[(https?://[^\]]+)\]\((https?://[^)]+)\)\)",
        r"[\1](\3)",
        markdown,
    )

    # 4. Fix malformed arrow functions emphasis
    markdown = re.sub(r"\*\\\*(.*?)\\\*\*", r"**\1**", markdown)

    # 5. Normalize excessive blank lines
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    return markdown.strip() + "\n"


def convert_html_to_markdown(html, class_name, filepath):
    """
    Convert HTML content and save it as Markdown or PDF.

    Args:
        html (str): The HTML content to convert.
        class_name (str): The class name of the div element to extract.
        filepath (str): The output file path without the extension.

    Returns:
        None
    """

    filepath = f"{filepath}.md" if checkFormatDownload == "md" else f"{filepath}.pdf"

    # Avoid reprocessing existing files
    if os.path.exists(filepath):
        return

    soup = BeautifulSoup(html, "html.parser")

    content = soup.select_one(f'section[class*="{class_name}"]') or soup.select_one(
        f'div[class*="{class_name}"]'
    )

    if content is None:
        if config.SHOW_DOWNLOAD_LOGS == "y":
            print(
                f"[WARNING] Skipping conversion for "
                f"{os.path.basename(filepath)}. "
                f"No content found for class '{class_name}'."
            )
        return

    # Remove unnecessary UI elements
    for button in content.select("button"):
        button.decompose()

    # Convert custom Platzi headings into standard HTML headings
    for heading in content.select('[role="heading"][aria-level]'):
        try:
            level = int(heading["aria-level"])
            heading.name = f"h{min(max(level, 1), 6)}"
        except (ValueError, TypeError):
            continue

    # Convert HTML to Markdown
    markdown_content = markdownify.markdownify(str(content), heading_style="ATX")

    # Normalize generated Markdown
    markdown_content = clean_markdown(markdown_content)

    # Create output directory
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

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
