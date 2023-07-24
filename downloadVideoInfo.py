
import subprocess
import requests
import re
from utils import createFolder, checkIfExtesionExists

def getInfo(url, courseName, className):
    folderPath = f'videos/{courseName}/videoInfo'
    createFolder("\\"+folderPath)
    res = requests.get(url)
    if res.status_code == 200:
        #desktop
        checkFullHD = re.search(r'1920x1080', res.text)
        checkHD = re.search(r'1280x720', res.text)
        #mobile
        checkFullHD2 = re.search(r'1080x1920', res.text)
        checkHD2 = re.search(r'720x1280', res.text)
        if checkFullHD:
            positions = checkFullHD.regs[0]
            newUrl = res.text[positions[1]+1:positions[1]+1000]
        elif checkHD:
            positions = checkHD.regs[0]
            newUrl = res.text[positions[1]+1:positions[1]+1000]
        elif checkFullHD2:
            positions = checkFullHD2.regs[0]
            newUrl = res.text[positions[1]+1:positions[1]+1000]
        elif checkHD2:
            positions = checkHD2.regs[0]
            newUrl = res.text[positions[1]+1:positions[1]+1000]
    headers = {
        "Referer": "https://platzi.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    newRes = requests.get(newUrl, headers=headers)
    if newRes.status_code == 200:
        #get the URI
        findUri = re.search(r'URI="(.*)"', newRes.text)
        resUri = None
        if findUri:
            uriUrl = findUri.group(1)
            resUri = requests.get(uriUrl, headers=headers)
        
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
        with open(f'{folderPath}/info.m3u8', 'w') as f:
            f.write(infom3u8)
        if resUri:
            if resUri.status_code == 200:
                with open(f'{folderPath}/encryption.key', 'ab') as f:
                        f.write(resUri.content)
        #remove text starting with #
        text = re.sub(r'#.*\n', '', newRes.text)
        #split the text by \n
        array = text.split('\n')
        #remove the last element of the array
        array.pop()
        i = 0
        for url in array:
            resTs = requests.get(url, headers=headers)
            if resTs.status_code == 200:
                with open(f'{folderPath}/{matchesTs[i]}', 'ab') as f:
                    f.write(resTs.content)
            else:
                print(f'error downloading ts file {matchesTs[i]}')
                break
            i += 1
            
        #run command to convert the ts files to mp4
        process = subprocess.check_output(f'cd {folderPath} && ffmpeg -protocol_whitelist file,tls,tcp,https,crypto -allowed_extensions ALL -i info.m3u8 -c copy "{className}".mp4 && move "{className}.mp4" ..\\"{className}.mp4"', shell=True)
        #remove the ts files
        if checkIfExtesionExists(folderPath, '.ts'):
            removeTs = subprocess.check_output(f'cd {folderPath} && del *.ts', shell=True)
        if checkIfExtesionExists(folderPath, '.m3u8'):
            removem3u8 = subprocess.check_output(f'cd {folderPath} && del *.m3u8', shell=True)
        if checkIfExtesionExists(folderPath, '.key'):
            removeKey = subprocess.check_output(f'cd {folderPath} && del *.key', shell=True)