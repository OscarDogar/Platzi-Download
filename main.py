# Get the logs from a web page using selenium

# Import the required modules
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
import json
import requests, re
#callprocess
from process import callProcess
#read .env file
from dotenv import load_dotenv
import os

# Main Function
if __name__ == "__main__":
    videosUrl = {}
    # Enable Performance Logging of Chrome.
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    # Create the webdriver object and pass the arguments
    options = webdriver.ChromeOptions()

    # Chrome will start in Headless mode
    # options.add_argument('headless')

    # Ignores any certificate errors if there is any
    options.add_argument("--ignore-certificate-errors")

    # Startup the chrome webdriver with executable path and
    # pass the chrome options and desired capabilities as
    # parameters.
    inputOption = input("Do you want to download only this video or this and the following videos?\n1. Just this one\n2. This one and the following\nType: ")
    while inputOption != "1" and inputOption != "2":
        inputOption = input("Do you want to download only this video or this and the following videos?\n1. Just this one\n2. This one and the following\nType: ")
    driver = webdriver.Chrome(executable_path="C:/chromedriver.exe",
                              chrome_options=options,
                              desired_capabilities=desired_capabilities)

    driver.get("https://platzi.com/login/")
    load_dotenv()
    emailInput = driver.find_element(
        By.XPATH, '//*[@id="login-v2"]/div/div/div/div[3]/form/div[2]/input')
    emailInput.send_keys(os.environ.get('EMAIL'))
    pwdInput = driver.find_element(
        By.XPATH, '//*[@id="login-v2"]/div/div/div/div[3]/form/div[3]/input')
    pwdInput.send_keys(os.environ.get('PWD'))

    submitBtn = driver.find_element(
        By.XPATH, '//*[@id="login-v2"]/div/div/div/div[3]/form/button')
    submitBtn.click()

    checkCaptcha = driver.find_elements(By.CLASS_NAME, 'StudentsHome-wrapper')
    while not checkCaptcha:
        checkCaptcha = driver.find_elements(By.CLASS_NAME,
                                            'StudentsHome-wrapper')

    driver.get(os.environ.get('START_DOWNLOAD_URL'))
    #Check the name of the video
    check = driver.find_elements(By.CLASS_NAME, 'material-video')
    #get the number of the video
    # number = driver.find_element(
    #     By.CLASS_NAME, 'Header-class-title').text.split("\n")[1].split("/")
    subtitles = {}
    while not len(check) == 0:
        #Check the name of the video
        check = driver.find_elements(By.CLASS_NAME, 'material-video')
        if len(check) == 0:
            quiz = driver.find_elements(By.CLASS_NAME,
                                        'StartQuizOverview-buttons')
            lecture = driver.find_elements(By.CLASS_NAME, 'material-lecture')
            content = driver.find_elements(By.CLASS_NAME, 'MaterialView-video')
            if (len(quiz) != 0):
                jumpNext = driver.find_element(By.CLASS_NAME,
                                               'StartQuizOverview-btn--skip')
                jumpNext.click()
                check = driver.find_elements(By.CLASS_NAME, 'material-video')
            elif (len(lecture) != 0):
                jumpNext = driver.find_element(By.CLASS_NAME,
                                               'Header-course-actions-next')
                jumpNext.click()
                check = driver.find_elements(By.CLASS_NAME, 'material-video')
            elif (len(content) != 0):
                jumpNext = driver.find_element(By.CLASS_NAME,
                                               'Header-course-actions-next')
                jumpNext.click()
                check = driver.find_elements(By.CLASS_NAME, 'material-video')
        if not len(check) == 0:
            nameClass = driver.find_element(
                By.CLASS_NAME, 'Header-class-title').text.split("\n")[0]
            number = driver.find_element(
                By.CLASS_NAME,
                'Header-class-title').text.split("\n")[1].split("/")
            #Remove characters for windows name file
            nameClass = re.sub(r'[^\w\s]', '', nameClass)
            nameClass = number[0] + ". " + nameClass
            #this is to the check if the video is already played
            videoDiv = driver.find_element(By.CLASS_NAME, 'video-js')
            classes = videoDiv.get_attribute("class")
            if "vjs-has-started" not in classes:
                videoDiv.click()
                # play.click()
            #This is to change the server to C
            driver.execute_script(
                'const a = document.getElementById("ServerPicker"); const news = a["children"]; for (let i = 0; i < news.length; i++) { if (news[i].innerText === "Server C" && news[i].className === "") { news[i].click(); } }'
            )
            # Sleeps for 2 seconds
            time.sleep(2)
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
                                print(url)
                            elif "vtt" in url:
                                subtitles[nameClass].append(url)
                                print(url)
                    # close the browser
            respVideo = requests.get(video)
            if (not len(subtitles[nameClass]) > 0):
                subtitles.pop(nameClass)
            # check the status code
            if respVideo.status_code == 200:
                videosUrl[nameClass] = video
                # strCommand = 'ffmpeg -i {} -c copy "{}.mp4"'.format(video, nameClass)
                # subprocess.run(strCommand, shell=True)
            if inputOption == "1":
                break
            btnNext = driver.find_element(
                By.CLASS_NAME, 'Header-course-actions-next').click()
    driver.quit()
    callProcess(videosUrl, subtitles)