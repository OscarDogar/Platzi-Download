# Import the required modules
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import requests, re
import time
import multiprocessing
from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import os
from pyfiglet import Figlet

# callprocess
from process import callProcess
from utils import (
    createFolder,
    create_env_file,
    remove_word_from_file,
    print_progress_bar,
    checkFolderExists,
    checkFileExists,
    colorize_text,
    checkIfffmpegInstalled,
)


# region Variables and selectors
webdriver_path = "C:/chromedriver.exe"
emailSelector = "email"
continueBtnSelector = "continueBtn"
pwdSelector = "password"
submitLoginBtnSelector = '//*[@id="login-v2"]/div/div/div/div[3]/form/button'

checkCaptchaSelector = "MainLayout"
checkVideoSelector = "VideoPlayer"
checkLectureSelector = "styles_Lecture"
checkQuizSelector = "StartQuizOverview-buttons"
contentSelector = "styles_IFrame"
checkExamSelector = "StartExamOverview"

courseInfoLinkSelector = "MaterialHeading-course"
courseInfoSelector = "Hero-base"
promorBannerSelector = "PromoBanner-content"
courseNameSelector = "course_name"
videoDivSelector = "video-js"
resourceBtnSelector = "resources_tab"
checkAvailableResourcesSelector = "Archivos de la clase"

skipQuizBtnSelector = "StartQuizOverview-btn--skip"
classNameSelector = "MaterialHeading-title"
classNumberSelector = "MaterialHeading-tag"
nextClassBtnSelector = "Button--secondary"

checkDownloadableResourcesSelector = "FilesTree-download"
checkDownloadableFileSelector = "fa-download"
checkDownloadAllSelector = "FilesTree_FilesTree__Download"

selectorErrorMsgs = {
    checkCaptchaSelector: "An error has occurred while validating the captcha.",
    checkVideoSelector: "There was an error finding the video",
    checkLectureSelector: "There was an error finding the lecture",
    checkQuizSelector: "There was an error finding the quiz",
    courseNameSelector: "There was an error finding the course name",
    videoDivSelector: "There was an error finding the video",
    skipQuizBtnSelector: "There was an error finding the skip quiz button",
    classNameSelector: "There was an error finding the class name",
    nextClassBtnSelector: "There was an error finding the next class button",
    checkDownloadableResourcesSelector: "There was an error finding the downloadable resources",
    checkDownloadableFileSelector: "There was an error finding the downloadable file",
}
# endregion


def downloadResources(driver, courseName, nameClass):
    # find the resource button
    checkResourceBtn = driver.find_elements(
        By.CSS_SELECTOR, f"[data-qa='{resourceBtnSelector}']"
    )
    if not checkResourceBtn:
        return
    checkResourceBtn = checkResourceBtn[0]
    checkResourceBtn.click()
    try:
        downloadAllBtn = driver.find_elements(
            By.XPATH, f"//*[contains(@class, '{checkDownloadAllSelector}')]"
        )
        # get the href of the download links
        if downloadAllBtn:
            downloadAllBtn = downloadAllBtn[0]
            path = "./videos/{}/resources/".format(courseName)
            os.makedirs(path, exist_ok=True)
            link = downloadAllBtn.get_attribute("href")
            # get the download file name
            fileName = f"{nameClass}.zip"
            # download the file
            if link != "":
                if not checkFileExists(
                    f"\\videos\\{courseName}\\resources\\{fileName}"
                ):
                    response = requests.get(link)
                    if response.status_code == 200:
                        path = "./videos/{}/resources/".format(courseName)
                        with open(f"{path}{fileName}", "wb") as f:
                            f.write(response.content)
        else:
            # get the download elements by href
            download_elements = driver.find_elements(
                By.XPATH,
                "//a[contains(@href, 'https://static.platzi.com/media/public/uploads')]",
            )
            headers = {
                "Referer": "https://platzi.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            }
            path = "./videos/{}/resources/".format(courseName)
            os.makedirs(path, exist_ok=True)
            for element in download_elements:
                link = element.get_attribute("href")
                # get the file name
                fileName = f"{nameClass.split('.')[0]}. {element.text}"
                # download the file
                if link != "":
                    if not checkFileExists(
                        f"\\videos\\{courseName}\\resources\\{fileName}"
                    ):
                        response = requests.get(link, headers=headers)
                        if response.status_code == 200:
                            with open(f"{path}{fileName}", "wb") as f:
                                f.write(response.content)

        return
    except:
        downloadAllBtn = None

    try:
        checkAvailableResources = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//*[contains(text(), '{checkAvailableResourcesSelector}')]",
                )
            )
        )
    except:
        checkAvailableResources = None
    if checkAvailableResources:
        download_elements = driver.find_elements(By.CSS_SELECTOR, "a[download]")
        if download_elements:
            if not checkFolderExists(f"\\videos\\{courseName}\\resources"):
                createFolder("\\videos\\" + courseName + "\\resources")
            # get the href of the download links
            for element in download_elements:
                link = element.get_attribute("href")
                # get the file name
                fileName = f"{nameClass.split('.')[0]}. {element.text}"
                # download the file
                if link != "":
                    if not checkFileExists(
                        f"\\videos\\{courseName}\\resources\\{fileName}"
                    ):
                        response = requests.get(link)
                        if response.status_code == 200:
                            path = "./videos/{}/resources/".format(courseName)
                            with open(f"{path}{fileName}", "wb") as f:
                                f.write(response.content)


def menu():
    titleFont = Figlet(font="larry3d")

    # Print colored text
    print(colorize_text(titleFont.renderText("  Platzi Download")))
    print(colorize_text("By OscarDogar\n", "4;32"))

    while True:
        # The input string containing the URL
        startUrl = input("Please enter the URL of the class you want to download: ")
        if "clases" in startUrl:
            break
    print("")
    inputOption = input(
        "Do you want to download only this video or this and the following videos?\n\n1. Just this one\n2. This one and the following\nType: "
    )
    while inputOption != "1" and inputOption != "2":
        inputOption = input(
            "Do you want to download only this video or this and the following videos?\n\n1. Just this one\n2. This one and the following\nType: "
        )

    return inputOption, startUrl


def main():
    if not checkIfffmpegInstalled():
        print("Please install ffmpeg")
        input("Press enter to exit")
        return
    create_env_file()
    work()


def getClassName(driver):
    # className = driver.find_element(By.XPATH, f"//*[contains(@class, '{classNameSelector}')]").text
    className = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[contains(@class, '{classNameSelector}')]")
        )
    )
    result = re.sub(r"Clase\s\d.*$", "", className.text)
    return re.sub(r"[^\w\s]", "", result)


def getClassNumber(driver):
    classNumber = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[contains(@class, '{classNumberSelector}')]")
        )
    )

    # classNumber = driver.find_element(By.XPATH, f"//*[contains(@class, '{classNumberSelector}')]").text
    number = [int(num) for num in re.findall(r"\d+", classNumber.text)]
    return number


def nextPage(driver):
    btnNext = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//*[contains(@class, '{nextClassBtnSelector}')]")
        )
    )
    # check if the button is disabled
    if btnNext.is_enabled():
        btnNext.click()
    else:
        print("There was an error finding the next class button")


def format_entry(name, url):
    return f"#EXTINF:-1,{name}\n{url}"


def getVideoAndSubInfo(driver):
    video_info = None
    subs_info = None
    driver.refresh()
    time.sleep(2)
    elements = driver.find_elements(By.XPATH, '//script[contains(text(), "serverC")]')
    if len(elements) == 0:
        # try multiple times to get the video info
        tryInfo = 0
        while tryInfo < 3:
            driver.refresh()
            time.sleep(2)
            elements = driver.find_elements(
                By.XPATH, '//script[contains(text(), "serverC")]'
            )
            if len(elements) > 0:
                break
            else:
                tryInfo += 1

    for element in elements:
        # Extract the content of the script element using JavaScript
        script_content = driver.execute_script(
            "return arguments[0].textContent;", element
        )
        # Clean up the content by removing escaped double quotes
        cleaned_script_content = script_content.replace("\\", "")
        videoPattern = r"\"serverC\":{(.*?)\}\}"
        # Use re.search to find the first matching pattern in the text
        videoMatch = re.search(videoPattern, cleaned_script_content)
        if videoMatch and video_info == None:
            video_info_str = videoMatch.group(0)
            # convert the string to json
            video_info = json.loads("{" + video_info_str)
            videoMatch = None
        # Define the regex pattern
        subPattern = r"\"movin\":{(.*?)\}\}"
        # Use regex to find the sub info
        subMatch = re.search(subPattern, cleaned_script_content)
        if subMatch and subs_info == None:
            sub_info_str = subMatch.group(0)
            subs_info = json.loads("{" + sub_info_str)
            subMatch = None
        if video_info and subs_info:
            break
    return video_info, subs_info


def getCourseImage(driver, link, courseName):
    driver.get(link)
    time.sleep(0.5)
    try:
        # Check if the element is present
        banner = driver.find_element(By.CLASS_NAME, promorBannerSelector)
        driver.execute_script(
            "arguments[0].parentNode.removeChild(arguments[0]);", banner
        )
    except NoSuchElementException:
        pass
    try:
        # save the course link
        with open(f"./videos/{courseName}/Course Link.txt", "w") as f:
            f.write(link)
        courseInfo = driver.find_element(By.CLASS_NAME, courseInfoSelector)
        driver.execute_script("arguments[0].scrollIntoView();", courseInfo)

        # Wait for a moment to ensure the element is fully visible
        driver.implicitly_wait(5)

        # Get the location and size of the element
        location = courseInfo.location
        size = courseInfo.size
        filePath = f"videos/{courseName}/folder.png"
        # Take a screenshot of the element
        driver.save_screenshot(filePath)

        # Open the screenshot using PIL
        img = Image.open(filePath)

        # Calculate the coordinates for cropping
        left = location["x"]
        top = location["y"]
        right = left + size["width"] + 529
        bottom = top + size["height"] + 74.8

        # Crop and save the screenshot of the element
        img = img.crop((left, top, right, bottom))
        img.save(filePath)
        # this is to change the folder icon because only show the last thumbnail in the folder
        current_file_name = filePath
        new_file_name = filePath[:-3] + "jpg"
        os.rename(current_file_name, new_file_name)
    except:
        print("There was an error getting the course image")
        pass


def work():
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
        # chrome_options.add_argument('headless')
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--incognito")
        # Startup the chrome webdriver with executable path and
        # pass the chrome options and desired capabilities as
        # parameters.
        service = Service(webdriver_path)
        #!fix replace https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/
        #! with https://storage.googleapis.com/chrome-for-testing-public/ in undetected_chromedriver\patcher.py
        driver = uc.Chrome(
            service=service,
            options=chrome_options,
            desired_capabilities=desired_capabilities,
        )
        driver.get("https://platzi.com/login/")
        load_dotenv()
        emailInput = driver.find_element(By.ID, emailSelector)
        emailInput.send_keys(os.environ.get("EMAIL"))
        time.sleep(0.5)
        continueBtn = driver.find_element(
            By.CSS_SELECTOR, f"[data-qa='{continueBtnSelector}']"
        )
        # check if the button is disabled
        if continueBtn.is_enabled():
            continueBtn.click()
        else:
            print("There was an error finding the continue button")

        pwdInput = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    pwdSelector,
                )
            )
        )
        pwdInput.send_keys(os.environ.get("PWD"))
        time.sleep(0.5)
        continueBtn = driver.find_element(
            By.CSS_SELECTOR, f"[data-qa='{continueBtnSelector}']"
        )
        # check if the button is disabled
        if continueBtn.is_enabled():
            continueBtn.click()
        else:
            print("There was an error finding the login button")

        checkCaptcha = driver.find_elements(By.ID, checkCaptchaSelector)
        while not checkCaptcha:
            checkCaptcha = driver.find_elements(By.ID, checkCaptchaSelector)
        driver.get(startUrl)
        # Check the name of the video
        time.sleep(2)
        lecture = driver.find_elements(
            By.XPATH, f"//*[contains(@class, '{checkLectureSelector}')]"
        )
        quiz = driver.find_elements(By.CLASS_NAME, checkQuizSelector)
        content = driver.find_elements(
            By.XPATH, f"//*[contains(@class, '{contentSelector}')]"
        )
        checkCourseName = driver.find_element(
            By.CSS_SELECTOR, f"[data-qa='{courseNameSelector}']"
        )
        if checkCourseName:
            courseName = checkCourseName.text
            courseName = re.sub(r"[^\w\s]", "", courseName)
            createFolder("\\videos\\{}".format(courseName))
            courseInfoLink = driver.find_elements(
                By.XPATH, f"//*[contains(@class, '{courseInfoLinkSelector}')]"
            )
            # get href of the course
            courseLink = courseInfoLink[0].get_attribute("href")
            if not checkFileExists(
                f"\\videos\\{courseName}\\folder.png"
            ) and not checkFileExists(f"\\videos\\{courseName}\\folder.jpg"):
                getCourseImage(driver, courseLink, courseName)
                driver.get(startUrl)
        if len(quiz) == 0 and len(lecture) == 0 and len(content) == 0:
            videoPlayer = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, videoDivSelector))
            )
        else:
            videoPlayer = None
        print("Finding videos...")
        if not checkFileExists(f"\\videos\\{courseName}\\playlist.m3u"):
            with open(f"./videos/{courseName}/playlist.m3u", "w") as file:
                file.write("#EXTM3U\n")
        nameClass = ""
        countVideoErrors = 0
        while True:
            try:
                videoPlayer = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, videoDivSelector))
                )
            except:
                videoPlayer = None
            if not videoPlayer:
                try:
                    lecture = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located(
                            (
                                By.XPATH,
                                f"//*[contains(@class, '{checkLectureSelector}')]",
                            )
                        )
                    )
                except:
                    lecture = None
            if videoPlayer or lecture:
                number = getClassNumber(driver)
            if videoPlayer:
                video_info = None
                subs_info = None
                nameClass = getClassName(driver)
                nameClass = f"{number[0]}. {nameClass}"
                video_info, subs_info = getVideoAndSubInfo(driver)
                if video_info:
                    video = video_info["serverC"]["hls"]
                    video = f"https://mdstrm.com/{video.split('v1/')[1]}"
                    respVideo = requests.get(video)
                    # check the status code
                    if respVideo.status_code == 200:
                        videosUrl[nameClass] = video
                        with open(f"./videos/{courseName}/playlist.m3u", "a") as file:
                            ##check if the video is already in the playlist
                            if (
                                not format_entry(nameClass, video)
                                in open(f"./videos/{courseName}/playlist.m3u").read()
                            ):
                                file.write(format_entry(nameClass, video) + "\n")
                        video = ""
                    else:
                        countVideoErrors += 1
                        print(
                            colorize_text(
                                f"There was an error getting the video: {nameClass}", 31
                            )
                        )
                if subs_info:
                    subtitles[nameClass] = subs_info["movin"]["subtitles"]
                downloadResources(driver, courseName, nameClass)
            elif lecture != None:
                createFolder("\\videos\\" + courseName + "\\lectures")
                nameClass = getClassName(driver)
                nameClass = f"{number[0]}. {nameClass}"
                lecturesUrls.append(f"{number[0]}. {driver.current_url}")
                res = driver.execute_cdp_cmd("Page.captureSnapshot", {})
                # Write the file locally
                with open(
                    "./videos/{}/lectures/{}.mhtml".format(courseName, nameClass),
                    "w",
                    newline="",
                ) as f:
                    f.write(res["data"])
            else:
                quiz = driver.find_elements(By.CLASS_NAME, checkQuizSelector)
                if len(quiz) != 0:
                    jumpNext = driver.find_element(By.CLASS_NAME, skipQuizBtnSelector)
                    jumpNext.click()
                else:
                    content = driver.find_elements(
                        By.XPATH, f"//*[contains(@class, '{contentSelector}')]"
                    )
                    exam = driver.find_elements(By.CLASS_NAME, checkExamSelector)
                    if len(exam) != 0:
                        break
            if inputOption == "2":
                print_progress_bar(int(number[0]), int(number[1]))
            if inputOption == "1":
                break
            if number[0] == number[1]:
                break
            elif len(quiz) == 0:
                nextPage(driver)
            elif (
                videoPlayer != None
                and lecture != None
                and len(quiz) != 0
                and len(content) != 0
            ):
                break
            videoPlayer = None
            lecture = None
            quiz = []
            content = []
            time.sleep(1)
        driver.close()
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
        if countVideoErrors > 0:
            print(
                colorize_text(
                    f"There were {countVideoErrors} errors getting the videos.", 31
                )
            )
        end_time = time.time()
        elapsed_time = end_time - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        print(
            f"The download took {hours} hours, {minutes} minutes, and {seconds} seconds to run."
        )
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
                print(colorize_text(selectorErrorMsgs[selector], 31))
            else:
                print(colorize_text("There was an error finding the elements", 31))
        elif "target window already closed" in str(e):
            print(colorize_text("Chrome browser has been closed", 31))
        elif "no such element: Unable to locate element" in str(e):
            print("There was an error finding the elements")
        elif "Cannot determine loading status" in str(e):
            print("The page did not load completely")
        elif "stale element not found" in str(e):
            print(
                "It looks like the page has been refreshed and the element is no longer attached to the DOM"
            )
        elif "object has no attribute 'status_code'" in str(e):
            print("There was an error downloading the video")
        elif "Chrome failed to start'" in str(e):
            print("Chrome failed to start")
        elif "cannot access local variable 'video'" in str(e):
            print(
                "There was an error finding the video, it seems that the server is not available"
            )
        else:
            print(e)
    finally:
        input("Press enter to exit")


if __name__ == "__main__":
    # Pyinstaller fix
    multiprocessing.freeze_support()
    main()
