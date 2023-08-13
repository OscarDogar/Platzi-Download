# Import the required modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
import json
import requests, re
import time
import multiprocessing

# callprocess
from process import callProcess
from utils import createFolder, create_env_file, remove_word_from_file

# read .env file
from dotenv import load_dotenv
import os

#region Variables and selectors
webdriver_path = "C:/chromedriver.exe"
emailSelector = '//*[@id="login-v2"]/div/div/div/div[3]/form/div[2]/input'
pwdSelector = '//*[@id="login-v2"]/div/div/div/div[3]/form/div[3]/input'
submitLoginBtnSelector= '//*[@id="login-v2"]/div/div/div/div[3]/form/button'

checkCaptchaSelector = "StudentHome-wrapper"
checkVideoSelector = "material-video"
checkLectureSelector = "material-lecture"
checkQuizSelector = "StartQuizOverview-buttons"
checkPlaygroundSelector = "MaterialIframe"

courseNameSelector = "Header-course-info-content"
videoDivSelector = "video-js"

skipQuizBtnSelector = "StartQuizOverview-btn--skip"
classNameSelector = "Header-class-title"
nextClassBtnSelector = "Header-course-actions-next"

checkDownloadableResourcesSelector = "FilesTree-download"
checkDownloadableFileSelector = "fa-download"

selectorErrorMsgs = {
    checkCaptchaSelector: "An error has occurred while validating the captcha.",
    checkVideoSelector: "There was an error finding the video",
    checkLectureSelector: "There was an error finding the lecture",
    checkQuizSelector: "There was an error finding the quiz",
    checkPlaygroundSelector: "There was an error finding the playground",
    courseNameSelector: "There was an error finding the course name",
    videoDivSelector: "There was an error finding the video",
    skipQuizBtnSelector: "There was an error finding the skip quiz button",
    classNameSelector: "There was an error finding the class name",
    nextClassBtnSelector: "There was an error finding the next class button",
    checkDownloadableResourcesSelector: "There was an error finding the downloadable resources",
    checkDownloadableFileSelector: "There was an error finding the downloadable file"
    
}
#endregion

def menu():
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
            "Please enter the URL of the class you want to download: "
        )
        # Find all occurrences of the pattern in the input string
        matches = re.match(pattern, startUrl)
        if matches:
            break
    return inputOption, startUrl

def main():
    create_env_file()
    work()

def work ():
    try:
        inputOption, startUrl = menu()
        start_time = time.time()
        createFolder("\\videos")
        videosUrl = {}
        subtitles = {}
        lecturesUrls = []
        words_to_remove = os.environ.get("WORDS_TO_REMOVE")
        # Enable Performance Logging of Chrome.
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        # Create the webdriver object and pass the arguments
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        # Ignores any certificate errors if there is any
        chrome_options.add_argument("--ignore-certificate-errors")
        # Chrome will start in Headless mode
        # options.add_argument('headless')

        # Startup the chrome webdriver with executable path and
        # pass the chrome options and desired capabilities as
        # parameters.
        
        service = Service(webdriver_path)
        driver = webdriver.Chrome(
            service = service,
            options = chrome_options,
            desired_capabilities = desired_capabilities,
        )

        driver.get("https://platzi.com/login/")
        load_dotenv()
        emailInput = driver.find_element(
            By.XPATH, emailSelector
        )
        emailInput.send_keys(os.environ.get("EMAIL"))
        pwdInput = driver.find_element(
            By.XPATH, pwdSelector
        )
        pwdInput.send_keys(os.environ.get("PWD"))

        submitBtn = driver.find_element(
            By.XPATH, submitLoginBtnSelector
        )
        submitBtn.click()

        checkCaptcha = driver.find_elements(By.CLASS_NAME, checkCaptchaSelector)
        while not checkCaptcha:
            checkCaptcha = driver.find_elements(By.CLASS_NAME, checkCaptchaSelector)

        driver.get(startUrl)

        # Check the name of the video
        check = driver.find_elements(By.CLASS_NAME, checkVideoSelector)
        lecture = driver.find_elements(By.CLASS_NAME, checkLectureSelector)
        quiz = driver.find_elements(By.CLASS_NAME, checkQuizSelector)
        playground = driver.find_elements(By.CLASS_NAME, checkPlaygroundSelector)

        checkCourseName = driver.find_elements(By.CLASS_NAME, courseNameSelector)
        if len(checkCourseName) != 0:
            courseName = driver.find_element(
                By.CLASS_NAME, courseNameSelector
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
            check = driver.find_elements(By.CLASS_NAME, checkVideoSelector)
            lecture = []
            playground = []
            quiz = []
            content = []
            if len(check) == 0:
                quiz = driver.find_elements(By.CLASS_NAME, checkQuizSelector)
                playground = driver.find_elements(By.CLASS_NAME, checkPlaygroundSelector)
                lecture = driver.find_elements(By.CLASS_NAME, checkLectureSelector)
                content = driver.find_elements(By.CLASS_NAME, "MaterialView-video")
                if len(quiz) != 0:
                    jumpNext = driver.find_element(
                        By.CLASS_NAME, skipQuizBtnSelector
                    )
                    jumpNext.click()
                elif len(lecture) != 0:
                    createFolder("\\videos\\" + courseName + "\\lectures")
                    nameClass = driver.find_element(
                        By.CLASS_NAME, classNameSelector
                    ).text.split("\n")[0]
                    number = (
                        driver.find_element(By.CLASS_NAME, classNameSelector)
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
                        By.CLASS_NAME, nextClassBtnSelector
                    )
                    jumpNext.click()
                elif len(content) != 0:
                    jumpNext = driver.find_element(
                        By.CLASS_NAME, nextClassBtnSelector
                    )
                    jumpNext.click()
                elif len(playground) != 0:
                    jumpNext = driver.find_element(
                        By.CLASS_NAME, nextClassBtnSelector
                    )
                    jumpNext.click()
                check = driver.find_elements(By.CLASS_NAME, checkVideoSelector)
            if not len(check) == 0:
                nameClass = driver.find_element(
                    By.CLASS_NAME, classNameSelector
                ).text.split("\n")[0]
                number = (
                    driver.find_element(By.CLASS_NAME, classNameSelector)
                    .text.split("\n")[1]
                    .split("/")
                )
                # Remove characters for windows name file
                nameClass = re.sub(r"[^\w\s]", "", nameClass)
                nameClass = number[0] + ". " + nameClass
                # this is to the check if the video is already played
                videoDiv = driver.find_element(By.CLASS_NAME, videoDivSelector)
                classes = videoDiv.get_attribute("class")
                if "vjs-has-started" not in classes:
                    videoDiv.click()
                    # play.click()
                # This is to change the server to C
                driver.execute_script(
                    'const a = document.getElementById("ServerPicker"); const news = a["children"]; for (const child of news) { if (child.innerText === "Server C" && !child.classList.contains("className")) { child.click(); break; } }'
                )
                time.sleep(2)
                checkDownloadBtn = driver.find_elements(By.CLASS_NAME, checkDownloadableResourcesSelector)
                checkDownloadBtn2 = driver.find_elements(By.CLASS_NAME, checkDownloadableFileSelector)
                href = ""
                fileName = ""
                extension = ""
                if checkDownloadBtn:
                    createFolder("\\videos\\" + courseName + "\\resources")
                    DownloadBtn = driver.find_element(By.CLASS_NAME, checkDownloadableResourcesSelector)
                    # get href
                    href = DownloadBtn.get_attribute("href")
                elif checkDownloadBtn2:
                    createFolder("\\videos\\" + courseName + "\\resources")
                    DownloadBtn = driver.find_element(By.CLASS_NAME, checkDownloadableFileSelector)
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
                btnNext = driver.find_element(By.CLASS_NAME, nextClassBtnSelector)
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
    except KeyboardInterrupt as e:
        print("The program was stopped")
    except Exception as e:
        # Regular expression pattern to match the selector
        pattern = r'"selector":"\.(.*?)"'
        # Find the match using the pattern
        match = re.search(pattern, str(e))
        if match:
            selector = match.group(1)
            if selector in selectorErrorMsgs:
                print(selectorErrorMsgs[selector])
            else:
                print("There was an error finding the elements")
        elif "target window already closed" in str(e):
            print("Chrome browser has been closed")
        elif "no such element: Unable to locate element" in str(e):
            print("There was an error finding the elements")
        elif "Cannot determine loading status" in str(e):
            print("The page did not load completely")
        elif "stale element not found" in str(e):
            print("It looks like the page has been refreshed and the element is no longer attached to the DOM")
        elif "object has no attribute 'status_code'" in str(e):
            print("There was an error downloading the video")
        elif "Chrome failed to start'" in str(e):
            print("Chrome failed to start")
        elif "cannot access local variable 'video'" in str(e):
            print("There was an error finding the video, it seems that the server is not available")
        else:
            print(e)
    finally:
        input("Press enter to exit")
    
if __name__ == "__main__":
    # Pyinstaller fix
    multiprocessing.freeze_support()
    main()
