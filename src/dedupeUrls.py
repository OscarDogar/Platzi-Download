"""Deduplicate and normalize Platzi course/route URLs.

Used by the downloader so ``COURSE_URL`` is unique before any course is
processed. Trailing-slash and ``http``/``www`` variants count as the same
link. First occurrence is kept.
"""

from __future__ import annotations

import re
from pathlib import Path


def split_urls(value: str) -> list[str]:
    """Split a COURSE_URL value into individual URLs."""
    return [url.strip() for url in value.replace(",", " ").split() if url.strip()]


def canonical_url(url: str) -> str:
    """Normalize a URL so trailing-slash and scheme variants match."""
    url = url.strip().rstrip("/")
    url = re.sub(r"^http://", "https://", url, flags=re.IGNORECASE)
    url = re.sub(r"^https://www\.", "https://", url, flags=re.IGNORECASE)
    return url


def format_url(url: str) -> str:
    """Return a canonical URL with a trailing slash."""
    return f"{canonical_url(url)}/"


def dedupe_urls(urls: list[str]) -> list[str]:
    """Return unique URLs, preserving first-seen order."""
    seen: set[str] = set()
    unique: list[str] = []
    for url in urls:
        key = canonical_url(url)
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(format_url(url))
    return unique


def parse_course_urls(value: str) -> list[str]:
    """Split and deduplicate a raw COURSE_URL string."""
    return dedupe_urls(split_urls(value))


def urls_match(left: list[str], right: list[str]) -> bool:
    """True if both lists are the same URLs in the same order."""
    return [canonical_url(url) for url in left] == [canonical_url(url) for url in right]


def extract_course_url_assignment(text: str) -> tuple[str, str, str]:
    """Split .env text into (before, COURSE_URL value, after).

    Raises:
        ValueError: If COURSE_URL is missing or its quotes are unclosed.
    """
    idx = 0
    while idx < len(text):
        line_start = idx
        line_end = text.find("\n", idx)
        if line_end == -1:
            line_end = len(text)
        stripped = text[line_start:line_end].lstrip()
        if stripped.startswith("COURSE_URL"):
            eq = text.find("=", line_start)
            if eq == -1 or eq > line_end:
                break
            value_start = eq + 1
            while value_start < len(text) and text[value_start] in " \t":
                value_start += 1
            if value_start >= len(text):
                return text[:line_start], "", text[line_end:]
            quote = text[value_start] if text[value_start] in "'\"" else ""
            if quote:
                value_end = text.find(quote, value_start + 1)
                if value_end == -1:
                    raise ValueError("Unclosed quote in COURSE_URL")
                value = text[value_start + 1 : value_end]
                after = value_end + 1
                if after < len(text) and text[after] == "\n":
                    after += 1
                return text[:line_start], value, text[after:]
            value = text[value_start:line_end]
            after = line_end + 1 if line_end < len(text) else line_end
            return text[:line_start], value, text[after:]
        idx = line_end + 1 if line_end < len(text) else len(text)
    raise ValueError("COURSE_URL was not found in the .env file")


def format_course_url(urls: list[str]) -> str:
    """Format URLs as a quoted, one-per-line COURSE_URL assignment."""
    joined = "\n".join(urls)
    return f'COURSE_URL="{joined}"\n'


def write_course_urls(env_path: Path, urls: list[str]) -> None:
    """Replace COURSE_URL in *env_path* with *urls*."""
    text = env_path.read_text(encoding="utf-8")
    before, _, after = extract_course_url_assignment(text)
    env_path.write_text(before + format_course_url(urls) + after, encoding="utf-8")


def persist_deduped_course_urls(env_path: Path) -> tuple[list[str], int, bool]:
    """Dedupe COURSE_URL in *env_path* and write only when the list changes.

    Returns:
        A tuple of ``(unique_urls, duplicate_count, wrote_file)``.

    Raises:
        ValueError: If COURSE_URL is missing, unquoted, or empty after parsing.
        FileNotFoundError: If *env_path* does not exist.
    """
    text = env_path.read_text(encoding="utf-8")
    _, value, _ = extract_course_url_assignment(text)
    original = split_urls(value)
    unique = dedupe_urls(original)
    if not unique:
        raise ValueError("COURSE_URL does not contain any links")
    duplicates = len(original) - len(unique)
    if urls_match(original, unique):
        return unique, duplicates, False
    write_course_urls(env_path, unique)
    return unique, duplicates, True
