import subprocess
# from multiprocessing import Process
from multiprocessing import Pool
import os
import math
import re

def checkFolderExists (folder_path):
    fullPath = os.getcwd() + folder_path
    return os.path.exists(fullPath) and os.path.isdir(fullPath)

def checkFileExists (file_path):
    fullPath = os.getcwd() + file_path
    return os.path.isfile(fullPath)

def run_command (command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    res1 = stdout.decode()
    res2 = stderr.decode()
    exit_code = process.returncode
    if exit_code == 0:
        if "failed: Error number -138 occurred" in stderr.decode() or "Unable to open resource:" in stderr.decode():
            return (f'Conversion failed with exit code {exit_code} for {command}')
        else:
            return (f'Conversion succeeded for {command}')
    else:
        return (f'Conversion failed with exit code {exit_code} for {command}')
    
def createCommands (info):
    commands = []
    folder = 'cd videos &&'
    for key, value in info.items():
        if not checkFileExists(f"\\videos\\{key}.mp4"):
            commands.append('{} ffmpeg -i {} -c copy "{}.mp4"'.format(folder, value, key))
        else:
            print(f"The file {key} already exists")
    return commands

def downloadSubs (subtitles):
    regex = r"\-[a-zA-Z]{2,3}\-" 
    anotherRegex = r"\.[a-zA-Z]{2,3}\-" 
    if not checkFolderExists("\\videos\\Subs"):
        subprocess.run("cd videos && mkdir Subs", shell=True)
    for key, value in subtitles.items():
        for sub in value:
            name = key
            #region Get the language of the subtitle
            match = re.search(regex, sub) or re.search(anotherRegex, sub)
            if match:
                language = sub[match.start() + 1:match.end() - 1]
                if language == "sp":
                    language = "spa"
            else:
                print(f"No match found for {sub}")
            #endregion
            name = name + f".{language}.vtt"
            subprocess.run(f'cd videos/Subs && curl {sub} -o "{name}"', shell=True)

def callProcess(info, subtitles):
    #current working directory
    commands = createCommands(info)
    if len(subtitles) > 0:
        downloadSubs(subtitles)
    else:
        print("No subtitles to download")
    if not checkFolderExists("\\videos"):
        subprocess.run("mkdir videos", shell=True)
    # Create a pool of 3 worker processes
    processNumber = 3
    pool = Pool(processes=processNumber)
    
    print(f"{len(commands)} videos will be downloaded divided into groups of {processNumber} for a total of {math.ceil(len(commands)/3)} groups.")
    # Divide the commands into groups of processNumber and run them in parallel
    for i in range(0, len(commands), processNumber):
        results = []
        group = commands[i:i+processNumber]
        results.append(pool.map(run_command, group))
        #check if the results have failed 
        count = 0
        for sublist in results:
            for element in sublist:
                if 'failed' in element:
                    count += 1
        print(f"Group {i//processNumber + 1} completed with {count} failed conversions")

    # Close the pool and wait for all processes to complete
    # print(results)
    pool.close()
    pool.join()

