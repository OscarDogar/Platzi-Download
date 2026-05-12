<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=220&color=0:0f172a,100:1e293b&text=Platzi-Download&fontColor=ffffff&fontSize=55&animation=fadeIn&fontAlignY=40&desc=Platzi%20Course%20Downloader&descAlignY=60" />

<br/>

<img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python" />
<img src="https://img.shields.io/github/v/release/OscarDogar/Platzi-Download?style=for-the-badge" />
<img src="https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge" />
<img src="https://img.shields.io/github/downloads/OscarDogar/Platzi-Download/total?style=for-the-badge" />
<img src="https://img.shields.io/github/last-commit/OscarDogar/Platzi-Download?style=for-the-badge" />
<img src="https://img.shields.io/github/repo-size/OscarDogar/Platzi-Download?style=for-the-badge" />
<!--<img src="https://img.shields.io/badge/Automation-Enabled-facc15?style=for-the-badge" />-->
<img src="https://img.shields.io/github/stars/OscarDogar/Platzi-Download?style=for-the-badge" />
<img src="https://img.shields.io/github/license/OscarDogar/Platzi-Download?style=for-the-badge" />
<img src="https://img.shields.io/badge/GHCR-Container-blue?style=for-the-badge&logo=docker" />
<img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" />

<a href="https://github.com/sponsors/OscarDogar">
  <img src="https://img.shields.io/badge/⭐%20Sponsor%20This%20Project-ff4d6d?style=for-the-badge&logo=githubsponsors&logoColor=white&labelColor=0f172a" height="45"/>
</a>

</div>

# 📌 Overview

**Downloader** is a Python automation tool designed to download **complete Platzi courses** in a structured and scalable way.

It handles everything from course parsing to video downloads and optional resources extraction.

# ⚙️ What It Does

The pipeline automatically processes each course URL:

- 🔐 Validates session cookie and course access
- 🔎 Extracts lesson links and metadata
- 🌐 Fetches lesson pages asynchronously (`aiohttp`)
- 🧠 Parses video URLs and lecture metadata
- 📎 Downloads course resources (optional)
- 🎥 Downloads videos using `yt-dlp`
- 🧹 Cleans temporary files (optional)
- 📊 Generates structured course output files

# ⚡ Performance Improvements & Usage Updates

## 🚀 Faster & More Stable

This new version is significantly:

- ⚡ **Faster** due to removal of browser automation (no Selenium/ChromeDriver)
- 🧠 **More stable** using direct HTTP/API-based requests
- 🛡️ **Less error-prone**, with improved retry and parsing logic
- 📦 Containerized for the default downloader workflow; optional Playwright/Chromium fallback requires additional browser setup

## 📚 Multi-Course Support

You can now download **one or multiple courses at the same time** using the `COURSE_URL` variable.

### 📌 Example

```env
COURSE_URL=https://course1,https://course2,https://course3
```

Just separate each course URL with a comma.

The downloader will process them sequentially in a single execution.

## 🔁 Resume & Retry Behavior

If any video fails to download:

- ❌ No need for manual recovery
- 🔄 Simply **run the program again**
- ✅ The downloader will automatically retry missing or failed videos

This makes the system resilient to network issues or temporary failures.

## 💡 Summary

- ⚡ Faster downloads
- 🧩 Fewer errors and better stability
- 📚 Multi-course download support
- 🔁 Easy retry system (just rerun the script)

# 🧱 Architecture

```txt
Course URL
   ↓
Extract Links
   ↓
Fetch HTML (async)
   ↓
Parse Video Metadata
   ↓
Generate videos.json
   ↓
Download Videos (yt-dlp)
   ↓
Optional Resources + Cleanup
```

# 📁 Project Structure

```
src/
 ├── main.py                 → Entry point
 ├── config.py               → Environment & validation
 ├── extractCourseLinks.py   → Course parsing
 ├── openLinks.py            → Async HTML fetching
 ├── getVideosLink.py        → Video extraction logic
 ├── downloadVideos.py       → yt-dlp downloader
 ├── downloadResourses.py    → Course resources
 ├── convertHTML2MD.py       → HTML → Markdown/PDF
 ├── convertMD2PDF.py        → Markdown → PDF
 ├── validateHtml.py         → Page validation
 ├── getToken.py             → Auth token handler
 ├── utils.py                → Shared utilities
```

# 📦 Requirements

- Python **3.12+**
- Valid **Platzi session cookie**
- Course URL access
- `ffmpeg`
- Chromium (Playwright fallback)

```bash
pip install -r requirements.txt
```

# 🔐 How to Get Your Cookie (Required Setup)

This project requires a valid **Platzi session cookie** to access course content.

## 📍 Where to Find It

You can extract it using your browser’s **Developer Tools**.

### 🧭 Steps (Chrome / Edge / Firefox)

1. Go to 👉 https://platzi.com
2. Log in with your account
3. Open Developer Tools:
   - Windows/Linux: `F12` or `Ctrl + Shift + I`
   - Mac: `Cmd + Option + I`
4. Go to the **Application** tab (or **Storage** in Firefox)
5. On the left panel, open:
   ```
   Cookies → https://platzi.com
   ```
6. Look for the cookie named:

```txt
s
```

7. Copy the value of the `s` cookie

## ⚙️ Example `.env`

```env
COOKIE=your_cookie_value_here
```

## ⚠️ Important Notes

- 🔒 This cookie is **personal and session-based**
- ⏳ It may expire after logout or time
- 🚫 Do NOT share it publicly
- 🔄 If downloads fail, refresh your login and update the cookie

## 💡 Tip

If you are logged out frequently, just re-copy the `s` cookie from DevTools and update your `.env` file.

# ⚙️ Configuration

All configuration is handled via `.env`.

| Variable                            | Required | Default    | Description                                  |
| ----------------------------------- | -------- | ---------- | -------------------------------------------- |
| COOKIE                              | ✅ Yes   | -          | Platzi session cookie                        |
| COURSE_URL                          | ✅ Yes   | -          | Course URLs (comma-separated)                |
| VIDEO_DOWNLOAD_MAX_PARALLEL         | Optional | `1`        | Maximum simultaneous video downloads         |
| VIDEO_DOWNLOAD_BATCH_SIZE           | Optional | `30`       | Number of downloads before cooldown          |
| VIDEO_DOWNLOAD_COOLDOWN             | Optional | `10`       | Delay between download batches (seconds)     |
| VIDEO_DOWNLOAD_START_DELAY          | Optional | `0.5`      | Delay before each download starts            |
| VIDEO_DOWNLOAD_LIMIT_RATE           | Optional | `100M`     | yt-dlp download rate limit                   |
| VIDEO_DOWNLOAD_CONCURRENT_FRAGMENTS | Optional | `3`        | Concurrent fragments downloaded by yt-dlp    |
| VIDEO_DOWNLOAD_FRAGMENT_RETRIES     | Optional | `20`       | Retry attempts per fragment                  |
| VIDEO_DOWNLOAD_RETRIES              | Optional | `20`       | Total retry attempts per video               |
| VIDEO_DOWNLOAD_RETRY_SLEEP          | Optional | `exp=1:20` | Retry backoff strategy                       |
| VIDEO_DOWNLOAD_SLEEP_REQUESTS       | Optional | `0`        | Delay between yt-dlp requests                |
| KEEP_TMP_FILES                      | Optional | `N`        | Keep temporary files (`Y/N`)                 |
| DOWNLOAD_RESOURCES                  | Optional | `Y`        | Download additional course resources (`Y/N`) |
| SHOW_DOWNLOAD_LOGS                  | Optional | `N`        | Enable verbose yt-dlp logs (`Y/N`)           |
| LECTURES_FORMAT_DOWNLOAD            | Optional | `pdf`      | Lecture export format (`md` or `pdf`)        |
| COURSE_NAME_DATE_FORMAT             | Optional | `%Y`       | Folder naming date format                    |

> 💡 Feel free to adjust the download configuration values based on your system performance, internet connection, or preferred behavior.
>
> Lower values may improve stability on slower systems, while higher values can increase download speed on more powerful machines or faster networks.
>
> You can experiment with:
>
> - ⚡ Parallel downloads
> - 📦 Batch sizes
> - 🔁 Retry limits
> - 🚦 Rate limits
> - ⏱️ Cooldowns and delays
>
> to achieve the best balance between speed, stability, and reliability for your environment.
>
> ⚠️ Using too many parallel downloads or extremely high download speeds may cause videos to fail, timeout, or trigger temporary rate limits from the platform.
>
> If you experience failed downloads, reduce:
>
> - `VIDEO_DOWNLOAD_MAX_PARALLEL`
> - `VIDEO_DOWNLOAD_LIMIT_RATE`
> - `VIDEO_DOWNLOAD_CONCURRENT_FRAGMENTS`
>
> for more stable results.

## 📄 Example `.env`

```env
COOKIE=your_cookie_here

COURSE_URL=https://platzi.com/cursos/example-course/

VIDEO_DOWNLOAD_MAX_PARALLEL=1
VIDEO_DOWNLOAD_BATCH_SIZE=30
VIDEO_DOWNLOAD_COOLDOWN=10
VIDEO_DOWNLOAD_START_DELAY=0.5
VIDEO_DOWNLOAD_LIMIT_RATE=100M
VIDEO_DOWNLOAD_CONCURRENT_FRAGMENTS=3
VIDEO_DOWNLOAD_FRAGMENT_RETRIES=20
VIDEO_DOWNLOAD_RETRIES=20
VIDEO_DOWNLOAD_RETRY_SLEEP=exp=1:20
VIDEO_DOWNLOAD_SLEEP_REQUESTS=0

KEEP_TMP_FILES=N
DOWNLOAD_RESOURCES=Y
SHOW_DOWNLOAD_LOGS=N

LECTURES_FORMAT_DOWNLOAD=pdf
COURSE_NAME_DATE_FORMAT=%Y
```

# 🐳 Docker Usage

## Compose

```yaml
services:
  Platzi-Download:
    container_name: Platzi-Download
    image: ghcr.io/oscardogar/platzi-download:latest
    user: "${UID:-1000}:${GID:-1000}"
    volumes:
      - /your/path/:/app/Videos
    env_file:
      - .env
```

You can configure everything directly inside `docker-compose.yml` without using a separate `.env` file.

```yaml
services:
  Platzi-Download:
    container_name: Platzi-Download
    image: ghcr.io/oscardogar/platzi-download:latest
    user: "${UID:-1000}:${GID:-1000}"

    volumes:
      - /your/path/:/app/Videos

    environment:
      # Required
      COOKIE: "your_cookie_here"

      # Required
      # Multiple courses supported (comma-separated)
      COURSE_URL: "https://platzi.com/cursos/course1/,https://platzi.com/cursos/course2/"

      # Optional (defaults shown below)
      VIDEO_DOWNLOAD_MAX_PARALLEL: "1"
      VIDEO_DOWNLOAD_BATCH_SIZE: "30"
      VIDEO_DOWNLOAD_COOLDOWN: "10"
      VIDEO_DOWNLOAD_START_DELAY: "0.5"
      VIDEO_DOWNLOAD_LIMIT_RATE: "100M"

      # Optional (defaults shown below)
      VIDEO_DOWNLOAD_CONCURRENT_FRAGMENTS: "3"
      VIDEO_DOWNLOAD_FRAGMENT_RETRIES: "20"
      VIDEO_DOWNLOAD_RETRIES: "20"

      # Optional (defaults shown below)
      VIDEO_DOWNLOAD_RETRY_SLEEP: "exp=1:20"
      VIDEO_DOWNLOAD_SLEEP_REQUESTS: "0"

      # Optional
      KEEP_TMP_FILES: "N"

      # Optional
      DOWNLOAD_RESOURCES: "Y"

      # Optional
      SHOW_DOWNLOAD_LOGS: "N"

      # Optional
      LECTURES_FORMAT_DOWNLOAD: "pdf"

      # Optional
      COURSE_NAME_DATE_FORMAT: "%Y"
```

Run:

```bash
docker compose up
```

---

## Build manually

```bash
docker build -t Platzi-Download .
docker run --rm --env-file .env -v "$PWD/Videos:/app/Videos" Platzi-Download
```

---

# 🚀 Usage

```bash
python src/main.py
```

Supports multiple courses:

```txt
COURSE_URL=https://course1,https://course2
```

---

# 📤 Output Structure

```
Videos/
 └── Course Name/
     ├── course_info.md
     ├── course_image.jpg
     ├── videos.json    → Present only if KEEP_TMP_FILES=Y
     ├── responses/     → Present only if KEEP_TMP_FILES=Y
     ├── VideosLinks/   → Present only if KEEP_TMP_FILES=Y
     ├── resources/
     └── *.mp4
```

# 💡 Key Features

- ⚡ Async scraping pipeline
- 🎥 yt-dlp optimized downloads
- 🔁 Retry & recovery system
- 📦 Batch + cooldown control
- 🧠 Metadata extraction engine
- 🧾 Course documentation generator
- 🐳 Docker-ready deployment

# 🤝 Contributing

Contributions are welcome:

- 🐛 Bug reports
- 💡 Feature requests
- 🔧 Pull requests

# ⭐ Support the Project

If this project saves you time or helps you, consider supporting it ❤️

<div align="center">

<a href="https://github.com/sponsors/OscarDogar">
  <img src="https://capsule-render.vercel.app/api?type=rect&height=120&color=0:ff4d6d,100:7c3aed&text=⭐%20SUPPORT%20THIS%20PROJECT%20ON%20GITHUB%20SPONSORS&fontColor=ffffff&fontSize=28&animation=fadeIn" />
</a>

</div>

# 📜 License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

You are free to:

- ✔️ Use
- ✔️ Modify
- ✔️ Distribute

But you must:

- 🔒 Keep source code open when distributing
- 🔒 Keep the same license (GPL-3.0)
- 🔒 Preserve copyright & license notices

👉 https://www.gnu.org/licenses/gpl-3.0.html

<div align="center">

### 🚀 Automate everything. Keep it open.

</div>
