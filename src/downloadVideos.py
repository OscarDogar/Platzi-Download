import subprocess
import glob
import os
import config
import json
import time
import random

MAX_PARALLEL = config.VIDEO_DOWNLOAD_MAX_PARALLEL
BATCH_SIZE = config.VIDEO_DOWNLOAD_BATCH_SIZE
COOLDOWN = config.VIDEO_DOWNLOAD_COOLDOWN
START_DELAY = config.VIDEO_DOWNLOAD_START_DELAY


# Header pools
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 Chrome/118 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Firefox/120.0",
]

ACCEPTS = [
    "*/*",
    "application/json, text/plain, */*",
]


def generate_headers():
    return {
        "Referer": "https://platzi.com/",
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": random.choice(ACCEPTS),
    }


def file_exists(name):
    base = os.path.join(config.FULL_PATH, name)
    for ext in (".mp4", ".mkv", ".webm"):
        if os.path.exists(base + ext):
            return True
    return False


def build_command(url, name):
    output_folder = config.FULL_PATH
    headers = generate_headers()
    header_args = []
    for k, v in headers.items():
        header_args.extend(["--add-header", f"{k}: {v}"])
    output_path = os.path.join(output_folder, f"{name}.%(ext)s")
    cmd = [
        "yt-dlp",
        url,
        "--concurrent-fragments",
        config.VIDEO_DOWNLOAD_CONCURRENT_FRAGMENTS,
        "--fragment-retries",
        config.VIDEO_DOWNLOAD_FRAGMENT_RETRIES,
        "--retries",
        config.VIDEO_DOWNLOAD_RETRIES,
        "--file-access-retries",
        config.VIDEO_DOWNLOAD_RETRIES,
        "--extractor-retries",
        config.VIDEO_DOWNLOAD_RETRIES,
        "--retry-sleep",
        config.VIDEO_DOWNLOAD_RETRY_SLEEP,
        "--sleep-requests",
        config.VIDEO_DOWNLOAD_SLEEP_REQUESTS,
        "--limit-rate",
        config.VIDEO_DOWNLOAD_LIMIT_RATE,
        "--downloader",
        "native",
        "--no-part",
        "--force-ipv4",
        "--write-subs",
        "--sub-langs",
        "all",
        "--convert-subs",
        "srt",
        "--embed-subs",
        "-o",
        output_path,
    ] + header_args
    return cmd


def run_download_command(url, name):
    print(f"[DOWNLOADING] {name}")
    cmd = build_command(url, name)
    if config.SHOW_DOWNLOAD_LOGS == "y":
        return subprocess.Popen(cmd)
    else:
        return subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def cleanup_files():
    output_folder = config.FULL_PATH
    patterns = (
        "*.vtt",
        "*.srt",
        "*.temp.mp4",
        "*.part*",
        "*.mkv.part*",
        "*.webm.part*",
        "*.ytdl",
    )
    for pattern in patterns:
        for f in glob.glob(os.path.join(output_folder, pattern)):
            try:
                os.remove(f)
            except:
                pass


def process_batch(video_list):
    processes = []
    failed = []
    completed = 0
    batch_counter = 0
    for video in video_list:
        name = video["name"]
        url = video["url"]
        if file_exists(name):
            continue
        p = run_download_command(url, name)
        processes.append((p, video))
        time.sleep(START_DELAY)
        if len(processes) >= MAX_PARALLEL:
            proc, vid = processes.pop(0)
            proc.wait()
            if file_exists(vid["name"]):
                completed += 1
                batch_counter += 1
            else:
                print(f"[ERROR] {vid['name']} failed")
                failed.append(vid)
            cleanup_files()
            if batch_counter >= BATCH_SIZE:
                print(
                    f"\n🧊 Cooling down for {COOLDOWN}s after {completed} downloads...\n"
                )
                time.sleep(COOLDOWN)
                batch_counter = 0
    for proc, vid in processes:
        proc.wait()
        if file_exists(vid["name"]):
            completed += 1
            batch_counter += 1
        else:
            print(f"[ERROR] {vid['name']} failed")
            failed.append(vid)
        if batch_counter >= BATCH_SIZE:
            print(f"\n🧊 Cooling down for {COOLDOWN}s after {completed} downloads...\n")
            time.sleep(COOLDOWN)
            batch_counter = 0
    cleanup_files()
    return failed


def download_videos():
    print("\n▶️  Starting video downloads...")
    with open(config.FULL_PATH_VIDEOS, "r", encoding="utf-8") as f:
        videos = json.load(f)
    failed = process_batch(videos)
    failed = [v for v in failed if not file_exists(v["name"])]
    if failed:
        print("\n❌ Failed downloads:")
        for v in failed:
            print(f" - {v['name']}")
    else:
        print("\n✅ All videos downloaded successfully")
