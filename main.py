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

# callprocess
from process import callProcess
from utils import createFolder, create_env_file, remove_word_from_file, print_progress_bar, checkFolderExists, checkFileExists

# read .env file
from dotenv import load_dotenv
import os

#region Variables and selectors
webdriver_path = "C:/chromedriver.exe"
emailSelector = '//*[@id="login-v2"]/div/div/div/div[3]/form/div[2]/input'
pwdSelector = '//*[@id="login-v2"]/div/div/div/div[3]/form/div[3]/input'
submitLoginBtnSelector= '//*[@id="login-v2"]/div/div/div/div[3]/form/button'

checkCaptchaSelector = "MainLayout"
checkVideoSelector = "VideoPlayer"
checkLectureSelector = "styles_Lecture"
checkQuizSelector = "StartQuizOverview-buttons"
contentSelector = 'styles_IFrame'
checkExamSelector = 'StartExamOverview'

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
    checkDownloadableFileSelector: "There was an error finding the downloadable file"
}
#endregion

def downloadResources(driver, courseName, nameClass):
    #find the resource button
    checkResourceBtn = driver.find_element(By.CSS_SELECTOR, f"[data-qa='{resourceBtnSelector}']")
    if checkResourceBtn:
        checkResourceBtn.click()
    try:
        checkAvailableResources = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{checkAvailableResourcesSelector}')]")))
    except:
        checkAvailableResources = None
    if checkAvailableResources:
        download_elements = driver.find_elements(By.CSS_SELECTOR, "a[download]")
        if download_elements:
            if not checkFolderExists(f"\\videos\\{courseName}\\resources"):
                createFolder("\\videos\\" + courseName + "\\resources")
            #get the href of the download links
            for element in download_elements:
                link = element.get_attribute("href")
                #get the file name
                fileName = f"{nameClass.split('.')[0]}. {element.text}"
                #download the file
                if link != "":
                    if not checkFileExists(f"\\videos\\{courseName}\\resources\\{fileName}"):
                        response = requests.get(link)
                        if response.status_code == 200:
                            path = "./videos/{}/resources/".format(courseName)
                            with open(f"{path}{fileName}", "wb") as f:
                                f.write(response.content)

def menu():
    inputOption = input(
        "Do you want to download only this video or this and the following videos?\n1. Just this one\n2. This one and the following\nType: "
    )
    while inputOption != "1" and inputOption != "2":
        inputOption = input(
            "Do you want to download only this video or this and the following videos?\n1. Just this one\n2. This one and the following\nType: "
        )
    
    while True:
        # The input string containing the URL
        startUrl = input(
            "Please enter the URL of the class you want to download: "
        )
        if "clases" in startUrl:
            break
    return inputOption, startUrl

def main():
    create_env_file()
    work()
    
def getClassName(driver):
    # className = driver.find_element(By.XPATH, f"//*[contains(@class, '{classNameSelector}')]").text
    className = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(@class, '{classNameSelector}')]")))
    return re.sub(r"[^\w\s]", "", className.text)

def getClassNumber(driver):
    classNumber = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(@class, '{classNumberSelector}')]")))

    # classNumber = driver.find_element(By.XPATH, f"//*[contains(@class, '{classNumberSelector}')]").text
    number = [int(num) for num in re.findall(r'\d+', classNumber.text)]
    return number

def nextPage(driver):
    btnNext = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[contains(@class, '{nextClassBtnSelector}')]")))
    # check if the button is disabled
    if btnNext.is_enabled():
        btnNext.click()
    else:
        print("There was an error finding the next class button")
        
def format_entry(name, url):
    return f"#EXTINF:-1,{name}\n{url}"

def getVideoAndSubInfo (driver):
    video_info = None
    subs_info = None
    elements = driver.find_elements(By.XPATH,'//script[contains(text(), "serverC")]')
    for element in elements:
        # Extract the content of the script element using JavaScript
        script_content = driver.execute_script("return arguments[0].textContent;", element)
        # Clean up the content by removing escaped double quotes
        cleaned_script_content = script_content.replace('\\', '')
        videoPattern = r'\"serverC\":{(.*?)\}\}'
        # Use re.search to find the first matching pattern in the text
        videoMatch = re.search(videoPattern, cleaned_script_content)
        if videoMatch and video_info == None:
            video_info_str = videoMatch.group(0)
            #convert the string to json
            video_info = json.loads("{" + video_info_str)
            videoMatch = None
        # Define the regex pattern
        subPattern = r'\"movin\":{(.*?)\}\}'
        # Use regex to find the sub info
        subMatch = re.search(subPattern, cleaned_script_content)
        if subMatch and subs_info == None:
            sub_info_str = subMatch.group(0)
            subs_info = json.loads("{" + sub_info_str)
            subMatch = None
        if video_info and subs_info:
            break
    return video_info, subs_info

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
        # chrome_options.add_argument('headless')
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--incognito")
        # Startup the chrome webdriver with executable path and
        # pass the chrome options and desired capabilities as
        # parameters.
        service = Service(webdriver_path)
        driver = uc.Chrome(
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

        checkCaptcha = driver.find_elements(By.ID, checkCaptchaSelector)
        while not checkCaptcha:
            checkCaptcha = driver.find_elements(By.ID, checkCaptchaSelector)
        driver.get(startUrl)
        # Check the name of the video
        time.sleep(2)
        lecture = driver.find_elements(By.XPATH, f"//*[contains(@class, '{checkLectureSelector}')]")
        quiz = driver.find_elements(By.CLASS_NAME, checkQuizSelector)
        content = driver.find_elements(By.XPATH, f"//*[contains(@class, '{contentSelector}')]")
        checkCourseName = driver.find_element(By.CSS_SELECTOR, f"[data-qa='{courseNameSelector}']")
        if checkCourseName:
            courseName = checkCourseName.text
            courseName = re.sub(r"[^\w\s]", "", courseName)
            createFolder("\\videos\\{}".format(courseName))
        if len(quiz) == 0 and len(lecture) == 0 and len(content) == 0:
            videoPlayer = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, videoDivSelector)))
        else:
            videoPlayer = None
        print("Finding videos...")
        if not checkFileExists(f"\\videos\\{courseName}\\playlist.m3u"):
            with open(f"./videos/{courseName}/playlist.m3u", "w") as file:
                file.write("#EXTM3U\n")
        while (
            videoPlayer != None
            or lecture != None
            or len(quiz) != 0
            or len(content) != 0
        ):
            exam = driver.find_elements(By.CLASS_NAME, checkExamSelector)
            if len(exam) != 0:
                break
            lecture = None
            quiz = []
            content = []
            quiz = driver.find_elements(By.CLASS_NAME, checkQuizSelector)
            try:
                if len(quiz) == 0:
                    lecture = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(@class, '{checkLectureSelector}')]")))
                else:
                    lecture = None
            except:
                lecture = None
            content = driver.find_elements(By.XPATH, f"//*[contains(@class, '{contentSelector}')]")
            try:
                if len(quiz) == 0 and lecture == None and len(content) == 0:
                    videoPlayer = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, videoDivSelector)))
                else:
                    videoPlayer = None
            except:
                videoPlayer = None
            if len(quiz) == 0:
                number = getClassNumber(driver)
            if len(quiz) != 0:
                jumpNext = driver.find_element(
                    By.CLASS_NAME, skipQuizBtnSelector
                )
                jumpNext.click()
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
            elif videoPlayer:
                video_info = None
                subs_info = None
                nameClass = getClassName(driver)
                nameClass = f"{number[0]}. {nameClass}"
                video_info, subs_info = getVideoAndSubInfo(driver)
                if video_info:
                    video = video_info["serverC"]["hls"]
                    respVideo = requests.get(video)
                    # check the status code
                    if respVideo.status_code == 200:
                        videosUrl[nameClass] = video
                        with open(f"./videos/{courseName}/playlist.m3u", "a") as file:
                            file.write(format_entry(nameClass, video) + "\n")
                        video = ""
                if subs_info:
                    subtitles[nameClass] = subs_info["movin"]["subtitles"]
                downloadResources(driver, courseName, nameClass)
            if inputOption == "2":
                    print_progress_bar(int(number[0]), int(number[1]))
            if inputOption == "1":
                break
            if number[0] == number[1] :
                break
            elif len(quiz) == 0:
                nextPage(driver)
            time.sleep(2)
            driver.refresh()
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
