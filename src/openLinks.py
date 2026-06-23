import asyncio
import os
import random
from curl_cffi.requests import AsyncSession
from playwright.async_api import async_playwright
import config

MAX_RETRIES = 2
BATCH_SIZE = 30


async def fetch_http(session, url, filename, semaphore):
    async with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # await asyncio.sleep(random.uniform(0.5, 1.5))
                response = await session.get(
                    url,
                    headers=config.headers,
                    timeout=60,
                )
                if response.status_code != 200:
                    raise Exception(f"HTTP {response.status_code}")
                text = response.text
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text)
                if config.SHOW_DOWNLOAD_LOGS == "y":
                    print(f"[HTTP OK] {url}")
                return {"status": "success", "url": url, "filename": filename}
            except Exception as e:
                print(f"[HTTP FAILED] {url} -> {e} (Attempt {attempt}/{MAX_RETRIES})")
                if attempt == MAX_RETRIES:
                    return {"status": "failed", "url": url, "filename": filename}
                await asyncio.sleep(2**attempt)


async def fetch_playwright(page, url, filename):
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(2)  # Respiro para JS dinámico
        html = await page.content()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[PW RESCUE OK] {url}") if config.SHOW_DOWNLOAD_LOGS == "y" else None
        return "success"
    except Exception as e:
        print(f"[PW FAILED] {url} -> {e}")
        return "failed"


async def openLinks(urls, names):
    PATH = config.FULL_PATH_HTML
    os.makedirs(PATH, exist_ok=True)
    use_playwright_permanently = False
    sem = asyncio.Semaphore(10)
    # Inicialización diferida de Playwright
    pw_instance = {"p": None, "browser": None, "page": None}

    async def init_pw():
        if pw_instance["p"] is None:
            print("\n⚙️  Iniciando Playwright...")
            pw_instance["p"] = await async_playwright().start()
            pw_instance["browser"] = await pw_instance["p"].chromium.launch(
                headless=True
            )
            context = await pw_instance["browser"].new_context(
                user_agent=config.headers["User-Agent"]
            )
            pw_instance["page"] = await context.new_page()

    async with AsyncSession(
        headers=config.headers,
        cookies=config.COOKIES,
        impersonate="chrome",
    ) as session:
        for i in range(0, len(urls), BATCH_SIZE):
            batch_urls = urls[i : i + BATCH_SIZE]
            batch_names = names[i : i + BATCH_SIZE]
            tasks = []
            pending_batch = []
            for j, (url, name) in enumerate(zip(batch_urls, batch_names)):
                idx = i + j + 1
                filename = f"{PATH}/{idx}. {name}.html"
                if not os.path.exists(filename):
                    pending_batch.append((url, filename))
            if not pending_batch:
                continue
            if not use_playwright_permanently:
                tasks = [
                    fetch_http(session, url, fname, sem) for url, fname in pending_batch
                ]
                results = await asyncio.gather(*tasks)
                # Revisar si hubo fallos
                failed_items = [r for r in results if r["status"] == "failed"]
                if failed_items:
                    print(
                        f"\n⚠️ {len(failed_items)} fallos detectados. Cambiando a modo playwright..."
                    )
                    use_playwright_permanently = True
                    await init_pw()
                    # Rescatar los que fallaron en este batch
                    for item in failed_items:
                        await fetch_playwright(
                            pw_instance["page"], item["url"], item["filename"]
                        )
            else:
                await init_pw()
                for url, fname in pending_batch:
                    await fetch_playwright(pw_instance["page"], url, fname)
            await asyncio.sleep(random.uniform(2, 4))
    if pw_instance["browser"]:
        await pw_instance["browser"].close()
    if pw_instance["p"]:
        await pw_instance["p"].stop()
