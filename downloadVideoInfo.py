import subprocess
import requests
import re
import time
from utils import createFolder, checkIfExtesionExists, print_progress_bar
from customRequest import request_with_random_user_agent


def make_request_with_retries(url, max_retries=3, retry_delay=1):
    for retry in range(max_retries):
        try:
            response = request_with_random_user_agent(url)
            if response.status_code == 200:
                return response  # Return the response if successful
        except requests.exceptions.RequestException as e:
            print(f"\nRequest failed (retry {retry + 1}/{max_retries})")
        # Wait before the next retry (using a simple backoff strategy)
        time.sleep(retry_delay)
        retry_delay *= 2  # Double the waiting time for the next retry
    # All retries failed, handle the failure here
    print("All retries failed.")
    return None


def getInfo(url, courseName, className):
    errorGettingClasses = None
    folderPath = f"videos/{courseName}/videoInfo"
    createFolder("\\" + folderPath)
    res = requests.get(url)
    if res.status_code == 200:
        # desktop
        checkFullHD = re.search(r"1920x1080", res.text)
        checkHD = re.search(r"1280x720", res.text)
        # mobile
        checkFullHD2 = re.search(r"1080x1920", res.text)
        checkHD2 = re.search(r"720x1280", res.text)
        if checkFullHD:
            positions = checkFullHD.regs[0]
            newUrl = res.text[positions[1] + 1 : positions[1] + 1000]
        elif checkHD:
            positions = checkHD.regs[0]
            newUrl = res.text[positions[1] + 1 : positions[1] + 1000]
        elif checkFullHD2:
            positions = checkFullHD2.regs[0]
            newUrl = res.text[positions[1] + 1 : positions[1] + 1000]
        elif checkHD2:
            positions = checkHD2.regs[0]
            newUrl = res.text[positions[1] + 1 : positions[1] + 1000]
    newRes = request_with_random_user_agent(newUrl)
    if newRes.status_code == 200:
        # get the URI
        findUri = re.search(r'URI="(.*)"', newRes.text)
        resUri = None
        if findUri:
            uriUrl = findUri.group(1)
            resUri = request_with_random_user_agent(uriUrl)
        matchesTs = re.findall(r"/([^/]+\.ts)", newRes.text)
        matchesHttp = re.findall(r"https://.*", newRes.text)
        i = 0
        infom3u8 = newRes.text
        for match in matchesHttp:
            if "encryption.key" in match:
                infom3u8 = infom3u8.replace(match, 'encryption.key"')
            else:
                infom3u8 = infom3u8.replace(match, matchesTs[i])
                i += 1
        with open(f"{folderPath}/info.m3u8", "w") as f:
            f.write(infom3u8)
        if resUri:
            if resUri.status_code == 200:
                with open(f"{folderPath}/encryption.key", "ab") as f:
                    f.write(resUri.content)
        # remove text starting with #
        text = re.sub(r"#.*\n", "", newRes.text)
        # split the text by \n
        array = text.split("\n")
        # remove the last element of the array
        array.pop()
        i = 0
        print(f"Started downloading {className}")
        for url in array:
            resTs = make_request_with_retries(url)
            # resTs = requests.get(url, headers=headers)
            if resTs == None:
                break
            if resTs.status_code == 200:
                print_progress_bar(i + 1, len(array))
                with open(f"{folderPath}/{matchesTs[i]}", "ab") as f:
                    f.write(resTs.content)
            else:
                print(f"error downloading ts file {matchesTs[i]}")
                break
            i += 1
        if resTs == None:
            print(f"ERROR downloading {className}")
            errorGettingClasses = className
        else:
            # run command to convert the ts files to mp4
            command = f'cd {folderPath} && ffmpeg -protocol_whitelist file,tls,tcp,https,crypto -allowed_extensions ALL -i info.m3u8 -c copy "{className}".mp4 && move "{className}.mp4" ..\\"{className}.mp4"'
            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
            )
            # print(f'Finished downloading {className}')
        # remove files
        if checkIfExtesionExists(folderPath, ".ts"):
            removeTs = subprocess.check_output(
                f"cd {folderPath} && del *.ts", shell=True
            )
        if checkIfExtesionExists(folderPath, ".m3u8"):
            removem3u8 = subprocess.check_output(
                f"cd {folderPath} && del *.m3u8", shell=True
            )
        if checkIfExtesionExists(folderPath, ".key"):
            removeKey = subprocess.check_output(
                f"cd {folderPath} && del *.key", shell=True
            )
    else:
        print(f"error getting info for {className}")
        errorGettingClasses = className
    return errorGettingClasses
