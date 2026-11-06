import os
import shutil

import json
import config
import re
from pathlib import Path
from pyfiglet import Figlet
from textwrap import dedent


def extract_field(text, field):
    """Extract a string field from HTML or serialized React server data."""
    search_texts = []

    # Newer Platzi pages split the serialized RSC stream across vinext
    # ``rsc.push(...)`` calls. Decode string arguments individually, then join
    # them before looking for fields so a push boundary can fall inside a value.
    vinext_chunks = []
    push_pattern = re.compile(r"\.rsc\.push\(")
    for push in push_pattern.finditer(text):
        script_end = text.find("</script>", push.end())
        if script_end == -1:
            script_end = len(text)

        payload = text[push.end() : script_end]
        argument = _first_js_call_argument(payload)
        if argument is None:
            continue

        chunk = _decode_rsc_push_argument(argument)
        if chunk is not None:
            vinext_chunks.append(chunk)
    if vinext_chunks:
        search_texts.append("".join(vinext_chunks))

    chunk_pattern = re.compile(
        r'self\.__next_f\.push\(\[\d+,("(?:\\.|[^"\\])*")\]\)'
    )
    chunks = []
    for chunk in chunk_pattern.finditer(text):
        try:
            chunks.append(json.loads(chunk.group(1)))
        except json.JSONDecodeError:
            continue
    if chunks:
        search_texts.append("".join(chunks))
    search_texts.append(text)

    quoted_key = rf'(?:\\)*"{re.escape(field)}(?:\\)*"'
    unquoted_key = re.escape(field)
    pattern = (
        rf'(?:{quoted_key}|{unquoted_key})'
        rf'\s*:\s*(?:\\)*"'
        rf'((?:\\.|[^"\\])*?)'
        rf'(?:\\)*"'
    )

    for candidate in search_texts:
        match = re.search(pattern, candidate)
        if not match:
            continue
        value = match.group(1)
        try:
            return json.loads(f'"{value}"')
        except json.JSONDecodeError:
            return value
    return None


def _first_js_call_argument(payload):
    """Read the first argument up to its matching call parenthesis."""
    depth = 1
    quote = None
    escaped = False

    for index, char in enumerate(payload):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue

        if char in ('"', "'", "`"):
            quote = char
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
            if depth == 0:
                return payload[:index].strip()

    # Some streamed chunks are intentionally incomplete at the script edge.
    # Return the available fragment so a later push can complete the stream.
    return payload.strip() or None


def _decode_rsc_push_argument(argument):
    """Decode a vinext push string while retaining incomplete stream pieces."""
    if not argument:
        return None

    try:
        decoded = json.loads(argument)
    except json.JSONDecodeError:
        # A push can end mid-string when the server splits a stream. Preserve
        # its contents and decode any complete JSON escapes where possible.
        fragment = argument
        if fragment.endswith(")"):
            fragment = fragment[:-1].rstrip()
        if fragment.startswith('"'):
            fragment = fragment[1:]
        if fragment.endswith('"'):
            fragment = fragment[:-1]
        try:
            return json.loads(f'"{fragment}"')
        except json.JSONDecodeError:
            return fragment

    if isinstance(decoded, str):
        return decoded
    if isinstance(decoded, (dict, list)):
        return json.dumps(decoded, ensure_ascii=False, separators=(",", ":"))
    return str(decoded)


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
    opinions=None,
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
