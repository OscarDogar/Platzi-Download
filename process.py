import subprocess

# from multiprocessing import Process
from multiprocessing import Pool
import os
import math
import re
import sys
from utils import checkFolderExists, checkFileExists, is_folder_empty, headers
from downloadVideoInfo import getInfo


# region Progress bar
def print_progress_bar(progress):
    bar_length = 50
    if progress > 100:
        progress = 100
    filled_length = int(progress * bar_length // 100)
    bar = "=" * filled_length + "-" * (bar_length - filled_length)
    sys.stdout.write(f"\r[{bar}] {progress:.2f}%")
    sys.stdout.flush()


def checkDuration(process, command):
    duration = None
    progress = 0
    # Regular expression pattern to extract the duration and progress from FFmpeg's output
    duration_pattern = re.compile(r"Duration: (\d{2}):(\d{2}):(\d{2}).(\d{2})")
    progress_pattern = re.compile(r"time=(\d{2}):(\d{2}):(\d{2}).(\d{2})")
    for line in iter(process.stderr.readline, b""):
        line = line.decode("utf-8")  # Decode the bytes to string
        # Search for duration
        duration_match = duration_pattern.search(line)
        if duration_match:
            hours, minutes, seconds, milliseconds = map(int, duration_match.groups())
            duration = (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 100)
        # Search for progress
        progress_match = progress_pattern.search(line)
        if progress_match and duration:
            hours, minutes, seconds, milliseconds = map(int, progress_match.groups())
            current_time = (
                (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 100)
            )
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


# endregion


def downloadSubs(subtitles, courseName):
    subsPath = f"videos/{courseName}/Subs"
    if not checkFolderExists(f"\\videos\\{courseName}\\Subs"):
        subprocess.run(f"cd videos/{courseName} && mkdir Subs", shell=True)
    for key, value in subtitles.items():
        if len(value) > 0:
            for sub in value:
                name = f"{key}.{sub['language']}.vtt"
                if not checkFileExists(f"\\videos\\{courseName}\\Subs\\{name}"):
                    userAgent = headers["User-Agent"]
                    subprocess.run(
                        f'cd videos/{courseName}/Subs && curl -A "{userAgent}" {sub["source"]} -o "{name}"',
                        shell=True,
                    )
                    # convert to srt
                    subprocess.run(
                        f'cd videos/{courseName}/Subs && ffmpeg -i "{name}" "{name[:-4]}.srt"',
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.DEVNULL,
                    )
                    # remove the vtt file
                    subprocess.run(
                        f'cd videos/{courseName}/Subs && del "{name}"', shell=True
                    )
    if is_folder_empty(subsPath):
        os.rmdir(subsPath)


# region Create and run commands
def createCommands(info, courseName):
    commands = []
    errorGettingClasses = []
    folder = 'cd videos/"{}" &&'.format(courseName)
    for key, value in info.items():
        if not checkFileExists(f"\\videos\\{courseName}\\{key}.mp4"):
            classError = getInfo(value, courseName, key)
            if classError:
                errorGettingClasses.append(classError)
                classError = None
            # commands.append(
            #     '{} ffmpeg -i {} -c copy "{}.mp4"'.format(folder, value, key)
            # )
        else:
            print(f"The file {key} already exists")
    if len(errorGettingClasses) > 0:
        print("xxxxxxxxxxxxxx ERRORS xxxxxxxxxxxxxx")
        print("The following classes failed to download:")
        for error in errorGettingClasses:
            print(error)
    return commands


def run_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    result = checkDuration(process, command)
    return result


# endregion


def callProcess(info, subtitles, courseName):
    if len(subtitles) > 0:
        downloadSubs(subtitles, courseName)
    else:
        print("No subtitles to download")
    # current working directory
    commands = createCommands(info, courseName)
    if checkFolderExists(f"\\videos\\{courseName}\\videoInfo"):
        subprocess.run(f"cd videos/{courseName}/ && rmdir videoInfo", shell=True)
    # Create a pool of 3 worker processes
    processNumber = 3
    pool = Pool(processes=processNumber)
    groupNumber = math.ceil(len(commands) / processNumber)
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
        # print in a new line
        print(
            f"\nGroup {i//processNumber + 1} of {groupNumber} completed with {count} failed conversions"
        )
    # Close the pool and wait for all processes to complete
    # print(results)
    pool.close()
    pool.join()
