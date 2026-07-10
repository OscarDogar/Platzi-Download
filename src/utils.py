import os
import shutil
import config
import re
from pathlib import Path
from pyfiglet import Figlet
from textwrap import dedent


def extract_field(text, field):
    try:
        matches = re.findall(r'push\(\[\d+,"(.*?)"\]\)', text)
        joined = "".join(matches)

        # This codec is much more lenient with truncated backslashes
        decoded = joined.encode("utf-8").decode("unicode_escape", errors="ignore")

        # Standard regex search
        match = re.search(rf'"{field}":"([^"]+)"', decoded)
        return match.group(1) if match else None
    except Exception as e:
        print(f"Error: {e}")
        return None


def count_files_in_folder(folder_path, extension):
    """
    Count the number of files with a specific extension in a given folder.

    Args:
        folder_path (str): The path to the folder where files should be counted.
        extension (str): The file extension to filter by (e.g., "mp4").

    Returns:
        int: The count of files with the specified extension in the folder.
    """
    return len(list(Path(folder_path).glob(f"*.{extension}")))


def count_download_videos():
    """
    Count the number of downloaded video files and HTML files.

    Returns:
        tuple: A tuple containing:
            - mp4_files (int): The number of MP4 files in the configured download path.
            - html_files (int): The number of HTML files in the configured HTML path.
    """
    # validate how many mp4 files are in the path
    mp4_files = count_files_in_folder(config.FULL_PATH, "mp4")
    html_files = count_files_in_folder(config.FULL_PATH_HTML, "html")
    return mp4_files, html_files


def delete_tmp_files():
    """
    Delete temporary files and directories based on configuration settings.

    Removes the following items if KEEP_TMP_FILES is set to "n":
    - FULL_PATH_HTML directory and all its contents
    - FULL_PATH_LINKS directory and all its contents
    - FULL_PATH_VIDEOS file

    Returns:
        None
    """
    if config.KEEP_TMP_FILES == "n":
        # delete FULL_PATH_HTML folder
        if os.path.exists(config.FULL_PATH_HTML):
            shutil.rmtree(config.FULL_PATH_HTML)
        # delete FULL_PATH_LINKS folder
        if os.path.exists(config.FULL_PATH_LINKS):
            shutil.rmtree(config.FULL_PATH_LINKS)
        # delete FULL_PATH_VIDEOS file
        if os.path.exists(config.FULL_PATH_VIDEOS):
            os.remove(config.FULL_PATH_VIDEOS)


def generate_course_md(
    courseName,
    launch_date,
    description,
    level,
    number_of_classes,
    duration_content,
    professors,
    professors_img,
    professors_description,
    reviews,
    opinions,
    url=None,
    output_path=None,
):
    """
    Generate a structured and clean Markdown file for a course.
    """

    if output_path and os.path.exists(output_path):
        return

    md = dedent(f"""
# 🎓 {courseName}

> *Descubre todo sobre el curso.*

---

## 📋 Detalles del Curso

| | |
| :-- | :-- |
| ⭐ **Rating** | {reviews or "N/A"} |
| 📝 **Opiniones** | {opinions or "N/A"} |
| 📅 **Publicación** | {launch_date or "N/A"} |
| 📊 **Nivel** | {level or "N/A"} |
| 🎬 **Total de Clases** | {number_of_classes or "N/A"} |
| ⏱️ **Duración** | {duration_content or "N/A"} |
| 🔗 **Enlace** | {f"[Acceder al curso 🚀]({url})" if url else "N/A"} |

---

## 📝 Acerca de este curso

{description or "> La descripción de este curso no está disponible en este momento."}

---

## 👨‍🏫 Instructor

### **{professors or "Instructor no especificado"}**

<table>
  <tr>
    <td width="20%" align="center" style="border: none; padding-right: 20px;">
      <img 
        src="{professors_img or 'https://via.placeholder.com/150'}" 
        alt="Foto del instructor" 
        width="140" 
        style="border-radius: 50%; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
      />
    </td>
    <td width="80%" style="border: none; vertical-align: top;">
      {professors_description or "La biografía del instructor no está disponible en este momento."}
    </td>
  </tr>
</table>

""").strip()

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md)

    return md


def colorize_text(text, color_code="1;36"):
    return f"\033[{color_code}m{text}\033[0m"


def clickable_link(text, url, color_code="4;32"):
    # Colored clickable terminal hyperlink
    return f"\033[{color_code}m\033]8;;{url}\033\\{text}\033]8;;\033\\\033[0m"


def menu():
    titleFont = Figlet(font="larry3d")

    print(colorize_text(titleFont.renderText("  Platzi Download")))

    print(clickable_link("By OscarDogar\n", "https://github.com/OscarDogar", "4;32"))
