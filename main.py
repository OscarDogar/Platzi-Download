# Import the required modules
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
import json
import requests, re
import time

# callprocess
from process import callProcess
from utils import createFolder, create_env_file, remove_word_from_file

# read .env file
from dotenv import load_dotenv
import os


# Main Function
if __name__ == "__main__":
    start_time = time.time()
    create_env_file()
    createFolder("\\videos")
    videosUrl = {}
    subtitles = {}
    lecturesUrls = []
    words_to_remove = os.environ.get("WORDS_TO_REMOVE")
    # Enable Performance Logging of Chrome.
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    # Create the webdriver object and pass the arguments
    options = webdriver.ChromeOptions()
    options.add_argument("--mute-audio")
    # Ignores any certificate errors if there is any
    options.add_argument("--ignore-certificate-errors")
    # Chrome will start in Headless mode
    # options.add_argument('headless')

    # Startup the chrome webdriver with executable path and
    # pass the chrome options and desired capabilities as
    # parameters.
    inputOption = input(
        "Do you want to download only this video or this and the following videos?\n1. Just this one\n2. This one and the following\nType: "
    )
    while inputOption != "1" and inputOption != "2":
        inputOption = input(
            "Do you want to download only this video or this and the following videos?\n1. Just this one\n2. This one and the following\nType: "
        )
    
    # The regex pattern to match the URL until "clases"
    pattern = r'https:\/\/platzi\.com\/clases'

    while True:
        # The input string containing the URL
        startUrl = input(
            "Por favor ingresa la URL de la clase que quieres descargar: "
        )
        # Find all occurrences of the pattern in the input string
        matches = re.match(pattern, startUrl)
        if matches:
            break
    driver = webdriver.Chrome(
        executable_path="C:/chromedriver.exe",
        chrome_options=options,
        desired_capabilities=desired_capabilities,
    )

    driver.get("https://platzi.com/login/")
    load_dotenv()
    emailInput = driver.find_element(
        By.XPATH, '//*[@id="login-v2"]/div/div/div/div[3]/form/div[2]/input'
    )
    emailInput.send_keys(os.environ.get("EMAIL"))
    pwdInput = driver.find_element(
        By.XPATH, '//*[@id="login-v2"]/div/div/div/div[3]/form/div[3]/input'
    )
    pwdInput.send_keys(os.environ.get("PWD"))

    submitBtn = driver.find_element(
        By.XPATH, '//*[@id="login-v2"]/div/div/div/div[3]/form/button'
    )
    submitBtn.click()

    checkCaptcha = driver.find_elements(By.CLASS_NAME, "StudentHome-wrapper")
    while not checkCaptcha:
        checkCaptcha = driver.find_elements(By.CLASS_NAME, "StudentHome-wrapper")

    driver.get(startUrl)

    # Check the name of the video
    check = driver.find_elements(By.CLASS_NAME, "material-video")
    lecture = driver.find_elements(By.CLASS_NAME, "material-lecture")
    quiz = driver.find_elements(By.CLASS_NAME, "StartQuizOverview-buttons")
    playground = driver.find_elements(By.CLASS_NAME, "MaterialIframe")

    checkCourseName = driver.find_elements(By.CLASS_NAME, "Header-course-info-content")
    if len(checkCourseName) != 0:
        courseName = driver.find_element(
            By.CLASS_NAME, "Header-course-info-content"
        ).text.split("\n")[0]
        courseName = re.sub(r"[^\w\s]", "", courseName)
        createFolder("\\videos\\{}".format(courseName))

    print("Finding videos...")
    while (
        not len(check) == 0
        or len(lecture) != 0
        or len(quiz) != 0
        or len(playground) != 0
    ):
        # Check the name of the video
        check = driver.find_elements(By.CLASS_NAME, "material-video")
        lecture = []
        playground = []
        quiz = []
        content = []
        if len(check) == 0:
            quiz = driver.find_elements(By.CLASS_NAME, "StartQuizOverview-buttons")
            playground = driver.find_elements(By.CLASS_NAME, "MaterialIframe")
            lecture = driver.find_elements(By.CLASS_NAME, "material-lecture")
            content = driver.find_elements(By.CLASS_NAME, "MaterialView-video")
            if len(quiz) != 0:
                jumpNext = driver.find_element(
                    By.CLASS_NAME, "StartQuizOverview-btn--skip"
                )
                jumpNext.click()
            elif len(lecture) != 0:
                createFolder("\\videos\\" + courseName + "\\lectures")
                nameClass = driver.find_element(
                    By.CLASS_NAME, "Header-class-title"
                ).text.split("\n")[0]
                number = (
                    driver.find_element(By.CLASS_NAME, "Header-class-title")
                    .text.split("\n")[1]
                    .split("/")
                )
                # Remove characters for windows name file
                nameClass = re.sub(r"[^\w\s]", "", nameClass)
                nameClass = number[0] + ". " + nameClass
                lecturesUrls.append(number[0] + ". " + driver.current_url)
                # Execute Chrome dev tool command to obtain the mhtml file
                time.sleep(1)
                res = driver.execute_cdp_cmd("Page.captureSnapshot", {})
                # Write the file locally
                with open(
                    "./videos/{}/lectures/{}.mhtml".format(courseName, nameClass),
                    "w",
                    newline="",
                ) as f:
                    f.write(res["data"])
                if inputOption == "1":
                    break
                jumpNext = driver.find_element(
                    By.CLASS_NAME, "Header-course-actions-next"
                )
                jumpNext.click()
            elif len(content) != 0:
                jumpNext = driver.find_element(
                    By.CLASS_NAME, "Header-course-actions-next"
                )
                jumpNext.click()
            elif len(playground) != 0:
                jumpNext = driver.find_element(
                    By.CLASS_NAME, "Header-course-actions-next"
                )
                jumpNext.click()
            check = driver.find_elements(By.CLASS_NAME, "material-video")
        if not len(check) == 0:
            nameClass = driver.find_element(
                By.CLASS_NAME, "Header-class-title"
            ).text.split("\n")[0]
            number = (
                driver.find_element(By.CLASS_NAME, "Header-class-title")
                .text.split("\n")[1]
                .split("/")
            )
            # Remove characters for windows name file
            nameClass = re.sub(r"[^\w\s]", "", nameClass)
            nameClass = number[0] + ". " + nameClass
            # this is to the check if the video is already played
            videoDiv = driver.find_element(By.CLASS_NAME, "video-js")
            classes = videoDiv.get_attribute("class")
            if "vjs-has-started" not in classes:
                videoDiv.click()
                # play.click()
            # This is to change the server to C
            driver.execute_script(
                'const a = document.getElementById("ServerPicker"); const news = a["children"]; for (const child of news) { if (child.innerText === "Server C" && !child.classList.contains("className")) { child.click(); break; } }'
            )
            time.sleep(2)
            checkDownloadBtn = driver.find_elements(By.CLASS_NAME, "FilesTree-download")
            checkDownloadBtn2 = driver.find_elements(By.CLASS_NAME, "fa-download")
            href = ""
            fileName = ""
            extension = ""
            if checkDownloadBtn:
                createFolder("\\videos\\" + courseName + "\\resources")
                DownloadBtn = driver.find_element(By.CLASS_NAME, "FilesTree-download")
                # get href
                href = DownloadBtn.get_attribute("href")
            elif checkDownloadBtn2:
                createFolder("\\videos\\" + courseName + "\\resources")
                DownloadBtn = driver.find_element(By.CLASS_NAME, "fa-download")
                # get the parent element
                DownloadBtn = DownloadBtn.find_element(By.XPATH, "..")
                fileName = DownloadBtn.text
                href = DownloadBtn.get_attribute("href")
            if href != "":
                # get the file extension
                extension = href.split(".")[-1]
                #!! ERRORS
                response = requests.get(href)
                path = "./videos/{}/resources/".format(courseName)
                if response.status_code == 200:
                    if extension == "pdf":
                        with open(f"{path}{fileName}", "wb") as f:
                            f.write(response.content)
                    else:
                        with open(f"{path}/{nameClass}.{extension}", "wb") as f:
                            f.write(response.content)
            # Sleeps for 2 seconds
            time.sleep(1)
            # Gets all the logs from performance in Chrome
            logs = driver.get_log("performance")
            subtitles[nameClass] = []
            for log in logs:
                message = log["message"]
                if "Network.requestWillBeSent" in message:
                    data = json.loads(message)["message"]
                    if "params" in data and "request" in data["params"]:
                        request = data["params"]["request"]
                        if "url" in request:
                            url = request["url"]
                            if "https://mdstrm.com/video/" in url:
                                video = url
                                # print(url)
                            elif "vtt" in url:
                                subtitles[nameClass].append(url)
                                # print(url)
                    # close the browser
            respVideo = requests.get(video)
            if not len(subtitles[nameClass]) > 0:
                subtitles.pop(nameClass)
            # check the status code
            if respVideo.status_code == 200:
                videosUrl[nameClass] = video
                # strCommand = 'ffmpeg -i {} -c copy "{}.mp4"'.format(video, nameClass)
                # subprocess.run(strCommand, shell=True)
            if inputOption == "1":
                break
            btnNext = driver.find_element(By.CLASS_NAME, "Header-course-actions-next")
            # check if the button is disabled
            if number[0] == number[1] :
                break
            elif "disabled" not in btnNext.get_attribute("class"):
                btnNext.click()
            else:
                break
    driver.quit()
    if len(lecturesUrls) > 0:
        with open(f"./videos/{courseName}/lectures/Lectures Urls.txt", "a") as f:
            for item in lecturesUrls:
                f.write("%s\n" % item)
    if videosUrl or subtitles:
        callProcess(videosUrl, subtitles, courseName)
    if words_to_remove:
        # convert string to list and remove spaces
        words_to_remove = words_to_remove.split(",")
        words_to_remove = [x.strip() for x in words_to_remove]
        remove_word_from_file(f"./videos/{courseName}/lectures/", words_to_remove)
    print("--------Finished--------")
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    print(f"The download took {hours} hours, {minutes} minutes, and {seconds} seconds to run.")
