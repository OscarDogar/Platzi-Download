import subprocess, glob, os, sys

headers = {
    "Referer": "https://platzi.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}


def remove_word_from_file(directory_path, words):
    file_paths = glob.glob(directory_path + "/*.mhtml")
    if not file_paths:
        return print("No lectures found")
    for file_path in file_paths:
        # Open the file in read mode
        with open(file_path, "r") as file:
            # Read the contents of the file
            contents = file.read()
        for word in words:
            # Replace the target string
            contents = contents.replace(word, "")
        # Open the file in write mode
        with open(file_path, "w") as file:
            # Write the modified contents back into the file
            file.write(contents)


def create_env_file():
    file_path = ".env"
    if not checkFileExists(file_path):
        env_variables = {
            "EMAIL": '"Your email"',
            "PWD": '"Your password"',
            "WORDS_TO_REMOVE": "Word1, Word2, Word3, Word4",
        }
        with open(file_path, "w") as env_file:
            for key, value in env_variables.items():
                env_file.write(f"{key} = {value}\n")


def colorize_text(text, color_code=32):
    # 32 = green, 31 = red ASCII color codes
    return f"\033[{color_code}m{text}\033[0m"


def print_progress_bar(progress, final_number):
    bar_length = 50
    filled_length = int(progress * bar_length // final_number)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    sys.stdout.write(
        colorize_text(
            f"\r[{bar}] {progress}/{final_number} {progress*100/final_number:.2f}%"
        )
    )
    sys.stdout.flush()

    if progress == final_number:
        sys.stdout.write("\n")
        sys.stdout.flush()


# region Folder and file checks
def checkFolderExists(folder_path):
    fullPath = os.getcwd() + folder_path
    return os.path.exists(fullPath) and os.path.isdir(fullPath)


def checkFileExists(file_path):
    fullPath = os.getcwd() + file_path
    return os.path.isfile(fullPath) or os.path.exists(file_path)


def createFolder(path):
    if not checkFolderExists(path):
        subprocess.run('mkdir "{}"'.format(path[1:]), shell=True)


def checkIfExtesionExists(directory, extension):
    return any(file.endswith(extension) for file in os.listdir(directory))


def is_folder_empty(folder_path):
    return len(os.listdir(folder_path)) == 0


def checkIfffmpegInstalled():
    try:
        subprocess.run(
            ["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except FileNotFoundError:
        return False


# endregion
