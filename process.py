import subprocess

# from multiprocessing import Process
from multiprocessing import Pool
import os
import math
import re
import sys

#region Folder and file checks
def checkFolderExists(folder_path):
    fullPath = os.getcwd() + folder_path
    return os.path.exists(fullPath) and os.path.isdir(fullPath)


def checkFileExists(file_path):
    fullPath = os.getcwd() + file_path
    return os.path.isfile(fullPath)

def createFolder(path):
    if not checkFolderExists(path):
        subprocess.run('mkdir "{}"'.format(path[1:]), shell=True)
#endregion

#region Progress bar
def print_progress_bar(progress):
    bar_length = 50
    if progress > 100:
        progress = 100
    filled_length = int(progress * bar_length // 100)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\r[{bar}] {progress:.2f}%')
    sys.stdout.flush()

def checkDuration(process, command):
    duration = None
    progress = 0
    # Regular expression pattern to extract the duration and progress from FFmpeg's output
    duration_pattern = re.compile(r'Duration: (\d{2}):(\d{2}):(\d{2}).(\d{2})')
    progress_pattern = re.compile(r'time=(\d{2}):(\d{2}):(\d{2}).(\d{2})')
    for line in iter(process.stderr.readline, b''):
        line = line.decode('utf-8')  # Decode the bytes to string
        # Search for duration
        duration_match = duration_pattern.search(line)
        if duration_match:
            hours, minutes, seconds, milliseconds = map(int, duration_match.groups())
            duration = (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 100)
        # Search for progress
        progress_match = progress_pattern.search(line)
        if progress_match and duration:
            hours, minutes, seconds, milliseconds = map(int, progress_match.groups())
            current_time = (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 100)
            progress = (current_time / duration) * 100
            print_progress_bar(progress)
        
        if (
            "failed: Error number -138 occurred" in line
            or "Unable to open resource:" in line
            or " Failed to reload playlist 0" in line
        ):
            return f"Conversion failed for {command}"
    process.stderr.close()
    process.wait()
    if process.returncode != 0:
        return f"Conversion failed for {command}"
    else:
        return f"Conversion succeeded for {command}"
#endregion

def downloadSubs(subtitles, courseName):
    regex = r"\-[a-zA-Z]{2,3}\-"
    anotherRegex = r"\.[a-zA-Z]{2,3}\-"
    moreRegex = r"\-[a-zA-Z]{2,3}\."
    if not checkFolderExists(f"\\videos\\{courseName}\\Subs"):
        subprocess.run(f"cd videos/{courseName} && mkdir Subs", shell=True)
    for key, value in subtitles.items():
        for sub in value:
            name = key
            # region Get the language of the subtitle
            match = (
                re.search(regex, sub)
                or re.search(anotherRegex, sub)
                or re.search(moreRegex, sub)
            )
            checkSubtitleExtension = re.search(r"\.vtt", sub)
            if match and checkSubtitleExtension:
                language = sub[match.start() + 1 : match.end() - 1].lower()
                if language == "sp" or language == "es":
                    language = "spa"
                    name = name + f".{language}.vtt"
                    subprocess.run(
                        f'cd videos/{courseName}/Subs && curl {sub} -o "{name}"',
                        shell=True,
                    )
            elif "automatic" in sub.lower() or "transcribe" in sub.lower():
                language = "spa"
                name = name + f".{language}.vtt"
                subprocess.run(
                    f'cd videos/{courseName}/Subs && curl {sub} -o "{name}"', shell=True
                )
            else:
                print(f"No match found for {sub}")
            # endregion

#region Create and run commands
def createCommands(info, courseName):
    commands = []
    folder = 'cd videos/"{}" &&'.format(courseName)
    for key, value in info.items():
        if not checkFileExists(f"\\videos\\{courseName}\\{key}.mp4"):
            commands.append(
                '{} ffmpeg -i {} -c copy "{}.mp4"'.format(folder, value, key)
            )
        else:
            print(f"The file {key} already exists")
    return commands

def run_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    result = checkDuration(process, command)
    return result
#endregion

def callProcess(info, subtitles, courseName):
    # current working directory
    commands = createCommands(info, courseName)
    if len(subtitles) > 0:
        downloadSubs(subtitles, courseName)
    else:
        print("No subtitles to download")

    # Create a pool of 3 worker processes
    processNumber = 3
    pool = Pool(processes=processNumber)
    groupNumber = math.ceil(len(commands) / processNumber)
    print("------------------------")
    print(
        f"{len(commands)} videos will be downloaded divided into groups of {processNumber} for a total of {groupNumber} groups."
    )
    print("------------------------")
    # Divide the commands into groups of processNumber and run them in parallel
    for i in range(0, len(commands), processNumber):
        results = []
        group = commands[i : i + processNumber]
        results.append(pool.map(run_command, group))
        # check if the results have failed
        count = 0
        for sublist in results:
            for element in sublist:
                if "failed" in element:
                    print("\n" + element)
                    count += 1
        #print in a new line 
        print(f"\nGroup {i//processNumber + 1} of {groupNumber} completed with {count} failed conversions")

    # Close the pool and wait for all processes to complete
    # print(results)
    pool.close()
    pool.join()
