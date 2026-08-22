<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=220&color=0:0f172a,100:1e293b&text=Platzi-Download&fontColor=ffffff&fontSize=55&animation=fadeIn&fontAlignY=40&desc=Platzi%20Course%20Downloader&descAlignY=60" />

<br/>

<img src="https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge" />
<img src="https://img.shields.io/github/last-commit/OscarDogar/Platzi-Download?style=for-the-badge" />
<img src="https://img.shields.io/github/stars/OscarDogar/Platzi-Download?style=for-the-badge" />
<img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python" />
<img src="https://img.shields.io/github/v/release/OscarDogar/Platzi-Download?style=for-the-badge" />
<img src="https://img.shields.io/github/downloads/OscarDogar/Platzi-Download/total?style=for-the-badge" />
<img src="https://img.shields.io/github/repo-size/OscarDogar/Platzi-Download?style=for-the-badge" />
<!--<img src="https://img.shields.io/badge/Automation-Enabled-facc15?style=for-the-badge" />-->
<img src="https://img.shields.io/github/license/OscarDogar/Platzi-Download?style=for-the-badge&cacheSeconds=3600" />
<a href="https://github.com/OscarDogar/Platzi-Download/pkgs/container/platzi-download">
<img src="https://img.shields.io/badge/GHCR-Container-blue?style=for-the-badge&logo=docker" />
<img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</a>

<a href="https://github.com/sponsors/OscarDogar">
  <img src="https://img.shields.io/badge/⭐%20Sponsor%20This%20Project-ff4d6d?style=for-the-badge&logo=githubsponsors&logoColor=white&labelColor=0f172a" height="45"/>
</a>

</div>

# 📌 Overview

**Platzi-Download** is a Python automation tool designed to download **complete Platzi courses** in a structured and scalable way.

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

## 📚 Multi-Course & Route Support

You can download:

- ✅ A single course
- ✅ Multiple courses
- ✅ A complete Platzi Route
  💙 Special thanks to **[@a-peirogon](https://github.com/a-peirogon)** for contributing the Platzi Route implementation.

# 📦 Requirements

- Python **3.12+**
- Valid **Platzi session cookie**
- Course URL access
- [ffmpeg](https://www.ffmpeg.org/)
- Chromium (Playwright fallback)

```bash
pip install -r requirements.txt
```

## ⚡ Quick Start

1. Choose your installation method:
   - [🐧 Linux](#linux)
   - [🪟 Windows](#windows)
   - [🐳 Docker](#docker)

2. [Get your Platzi session cookie](#cookie).
3. [Configure your `.env` file](#env-file).
4. [Configure your course URL](#usage).
5. [Results](#output-structure).

---

# 📦 Installation

Choose your platform:

<a id="linux"></a>
<details>
<summary><h2>🐧 Linux</h2></summary>

### 1. Clone the repository

```bash
git clone https://github.com/OscarDogar/Platzi-Download.git
cd Platzi-Download
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install [FFmpeg](https://www.ffmpeg.org/)


### 5. Run

```bash
python src/main.py
```

</details>

<a id="windows"></a>
<details>
<summary><h2>🪟 Windows</h2></summary>

### Option 1 (Easiest): Download the `.exe`

1. Go to the [latest release](https://github.com/OscarDogar/Platzi-Download/releases/latest) and download the Windows executable.

```text
Platzi.Download.exe
```
2. Create a `.env` file in the same folder as the compose file and add your **Platzi session cookie** and **course URL**. You can check the [Environment File Configuration](#env-file) section for more details.

> You do not need to install Python when using the `.exe`.

> 📦 **Why is the `.exe` file large?**  
> The executable includes the required binaries for **FFmpeg**, **FFprobe**, and **yt-dlp**, so you do not need to install them separately.

> 💡 **Recommended:** Run the `.exe` from a terminal instead of double-clicking it. If you double-click the executable, the window may close automatically when the download finishes or when an error occurs.

Run it from **PowerShell** or **Command Prompt**:

```powershell
.\Platzi.Download.exe
```

Or open a terminal inside the folder:

```text
Right-click inside the folder → Open in Terminal
```

This allows you to see the download progress, final output, and any errors before closing the terminal.

### Option 2: Clone the repository

```powershell
git clone https://github.com/OscarDogar/Platzi-Download.git
cd Platzi-Download
```

Create a virtual environment:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
python src/main.py
```

</details>

<a id="docker"></a>
<details>
<summary><h2>🐳 Docker</h2></summary>

The official Docker image is available on GitHub Container Registry:

1. Download the image from https://github.com/OscarDogar/Platzi-Download/pkgs/container/platzi-download
2. Create a `.env` file in the same folder as the compose file and add your **Platzi session cookie** and **course URL**. You can check the [Environment File Configuration](#env-file) section for more details.

### Docker Compose

```yaml
services:
  platzi-download:
    container_name: Platzi-Download
    image: ghcr.io/oscardogar/platzi-download:latest
    user: "${UID:-1000}:${GID:-1000}"

    volumes:
      - /your/path/:/app/Videos

    env_file:
      - .env
```

Run:

```bash
docker compose up
```

<details>
<summary><b>Configure Docker without a separate .env file</b></summary>

```yaml
services:
  platzi-download:
    container_name: Platzi-Download
    image: ghcr.io/oscardogar/platzi-download:latest
    user: "${UID:-1000}:${GID:-1000}"

    volumes:
      - /your/path/:/app/Videos

    environment:
      s: "your_cookie_here"
      COURSE_URL: "https://platzi.com/cursos/python/"

      VIDEO_DOWNLOAD_MAX_PARALLEL: "1"
      VIDEO_DOWNLOAD_BATCH_SIZE: "30"
      VIDEO_DOWNLOAD_COOLDOWN: "10"
      VIDEO_DOWNLOAD_START_DELAY: "0.5"
      VIDEO_DOWNLOAD_LIMIT_RATE: "100M"
      VIDEO_DOWNLOAD_CONCURRENT_FRAGMENTS: "3"
      VIDEO_DOWNLOAD_FRAGMENT_RETRIES: "20"
      VIDEO_DOWNLOAD_RETRIES: "20"
      VIDEO_DOWNLOAD_RETRY_SLEEP: "exp=1:20"
      VIDEO_DOWNLOAD_SLEEP_REQUESTS: "0"
      KEEP_TMP_FILES: "N"
      DOWNLOAD_RESOURCES: "Y"
      SHOW_DOWNLOAD_LOGS: "N"
      LECTURES_FORMAT_DOWNLOAD: "pdf"
      COURSE_NAME_DATE_FORMAT: "%Y"
```

</details>

<details>
<summary><b>Build the Docker image manually</b></summary>

```bash
docker build -t Platzi-Download .
```

```bash
docker run --rm \
  --env-file .env \
  -v "$PWD/Videos:/app/Videos" \
  Platzi-Download
```

</details>

</details>

---

<a id="cookie"></a>
<details>
<summary><h2>🔐 How to Get Your Cookie (Required Setup)</h2></summary>

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
#COOKIE=your_cookie_value_here
s=ydioioapokxasoijqweopksdopic
```

## ⚠️ Important Notes

- 🔒 This cookie is **personal and session-based**
- ⏳ It may expire after logout or time
- 🚫 Do NOT share it publicly
- 🔄 If downloads fail, refresh your login and update the cookie

## 💡 Tip

If you are logged out frequently, just re-copy the `s` cookie from DevTools and update your `.env` file.

</details>

---

<a id="env-file"></a>
<details>
<summary><h2>⚙️ Environment File Configuration</h2></summary>

All configuration is handled via `.env`.

| Variable                            | Required | Default    | Description                                  |
| ----------------------------------- | -------- | ---------- | -------------------------------------------- |
| COOKIE                              | ✅ Yes   | -          | Platzi session cookie                        |
| COURSE_URL                          | ✅ Yes   | -          | Course and/or Route URLs (comma-separated)   |
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
s=your_cookie_here

# Single course
COURSE_URL=https://platzi.com/cursos/example-course/

# Multiple courses
# COURSE_URL=https://platzi.com/cursos/course1/,https://platzi.com/cursos/course2/

# Complete route
# COURSE_URL=https://platzi.com/ruta/administracion-de-servidores-linux/

# Mix routes and courses
# COURSE_URL=https://platzi.com/ruta/administracion-de-servidores-linux/,https://platzi.com/cursos/python/

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
</details>

---

</details>

<a id="usage"></a>
<details>
<summary><h2>🚀 Usage</h2></summary>

## Single Course

```env
COURSE_URL=https://platzi.com/cursos/python/
```

## Multiple Courses

```env
COURSE_URL=https://platzi.com/cursos/python/,https://platzi.com/cursos/docker/
```

## Complete Route

```env
COURSE_URL=https://platzi.com/ruta/administracion-de-servidores-linux/
```

## Mix Courses and Routes

```env
COURSE_URL=https://platzi.com/ruta/administracion-de-servidores-linux/,https://platzi.com/cursos/python/
```

The downloader automatically detects whether each URL is a course or a route.

For routes, it will:

1. Extract every course in the route.
2. Remove duplicate courses.
3. Download each course sequentially.

</details>

---

<a id="output-structure"></a>
<details>
<summary><h2>📤 Output Structure</h2></summary>

```
Videos/
├── Course Name/
│   ├── course_info.md
│   ├── course_image.jpg
│   ├── videos.json    → Present only if KEEP_TMP_FILES=Y
│   ├── responses/     → Present only if KEEP_TMP_FILES=Y
│   ├── VideosLinks/   → Present only if KEEP_TMP_FILES=Y
│   ├── resources/
│   └── *.mp4
│
└── Route Name/
    ├── Course 1/
    │   ├── course_info.md
    │   ├── course_image.jpg
    │   ├── videos.json    → Present only if KEEP_TMP_FILES=Y
    │   ├── responses/     → Present only if KEEP_TMP_FILES=Y
    │   ├── VideosLinks/   → Present only if KEEP_TMP_FILES=Y
    │   ├── resources/
    │   └── *.mp4
    │
    ├── Course 2/
    │   ├── course_info.md
    │   ├── course_image.jpg
    │   ├── videos.json    → Present only if KEEP_TMP_FILES=Y
    │   ├── responses/     → Present only if KEEP_TMP_FILES=Y
    │   ├── VideosLinks/   → Present only if KEEP_TMP_FILES=Y
    │   ├── resources/
    │   └── *.mp4
    │
    └── ...
```
</details>

---

# 🤝 Contributing

Contributions are welcome:

- 🐛 Bug reports
- 💡 Feature requests
- 🔧 Pull requests

# 🤝 Contributors

Every contribution, whether it's a bug report, feature request, documentation improvement, or code submission helps make **Platzi-Download** better for everyone.

A huge thank you to everyone who has taken the time to contribute to this project. ❤️

<div align="center">

<a href="https://github.com/oscardogar/platzi-download/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=oscardogar/platzi-download" alt="Contributors"/>
</a>

**Want to see your avatar here?**

Contributions of all sizes are welcome! Feel free to open an issue, submit a pull request, or help improve the documentation.

⭐ If you find this project useful, don't forget to star the repository!

</div>

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
