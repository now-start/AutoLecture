import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time

chrome_driver_dir = 'chromedriver'  # 수정
options = webdriver.ChromeOptions()
options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
driver = webdriver.Chrome(chrome_driver_dir, options=options)
url = 'https://lms.yc.ac.kr/login.php'
driver.get(url)
driver.minimize_window()
driver.implicitly_wait(10)

# 로그인
id = input("ID : ")
password = input("PASSWORD : ")
driver.find_element_by_id('input-username').send_keys(id)
driver.find_element_by_id('input-password').send_keys(password)
driver.find_element_by_name('loginbutton').click()

# 팝업창 제거
driver.implicitly_wait(10)
driver.maximize_window()
popUp = driver.find_elements_by_xpath('//div[@class="modal notice_popup ui-draggable"]//button')
for i in popUp:
    i.click()
driver.minimize_window()

print('------------------------------------------------------------------------------------\n')

# 강의 선택
driver.implicitly_wait(10)
lecture = driver.find_elements_by_xpath('//ul[@class="my-course-lists coursemos-layout-0"]/li')
j = 1
for i in lecture:
    print(j, i.text, '\n')
    j += 1

n = int(input("Lecture : "))
driver.find_elements_by_xpath('//ul[@class="my-course-lists coursemos-layout-0"]//a')[n - 1].click()

# 주차 선택
week = int(input("Week(current : 0) : "))

# 강의 목록
start = int(input("n ~ end(first ~ end : 1) : "))

def play(week, start):
    # 강의 재생 목록
    if week == 0:
        vod = driver.find_elements_by_xpath(
            '//div[@class="course_box course_box_current"]//a[contains(@href,"https://lms.yc.ac.kr/mod/vod/")]')
    else:
        xpath = "// *[ @ id = 'section-"
        xpath += str(week)
        xpath += "']//a[contains(@href,'https://lms.yc.ac.kr/mod/vod/')]"
        vod = driver.find_elements_by_xpath(xpath)

    print('------------------------------------------------------------------------------------\n')

    # 강의 재생
    pp = 1
    for i in vod:
        # 강의 패스
        if pp != start:
            pp = pp + 1
            continue
        else:
            driver.maximize_window()
            driver.implicitly_wait(10)
            i.click()
            window_before = driver.window_handles[0]
            window_after = driver.window_handles[1]
            driver.minimize_window()
            driver.switch_to.window(window_after)
            driver.implicitly_wait(10)

            # 플레이
            try:
                Alert(driver).accept()
            except:
                driver.find_element_by_xpath('//div[@class="jw-icon jw-icon-display jw-button-color jw-reset"]').send_keys(
                    Keys.ENTER)
                driver.find_element_by_xpath(
                    '//div[@class="jw-icon jw-icon-inline jw-button-color jw-reset jw-icon-playback"]').send_keys(Keys.ENTER)
                driver.find_element_by_xpath('//*[@id="vod_player"]/div[8]/div[4]/div[1]/div[1]').send_keys(Keys.ENTER)

            driver.minimize_window()
            time.sleep(20)

            # 제목 출력
            title = driver.find_element_by_xpath('/html/head/title').get_attribute('outerHTML')
            title = title.split(">")[1]
            title = title.split("<")[0]
            print(title)

            # 플레이 타임 설정
            end_time = driver.find_element_by_xpath('//span[@class="jw-text jw-reset jw-text-duration"]').get_attribute(
                'outerHTML')
            end_time = end_time.split(">")[1]
            end_time = end_time.split("<")[0]
            end_time = int(end_time.split(":")[0]) * 60 + int(end_time.split(":")[1])

            current_time = driver.find_element_by_xpath('//span[@class="jw-text jw-reset jw-text-elapsed"]').get_attribute(
                'outerHTML')
            current_time = current_time.split(">")[1]
            current_time = current_time.split("<")[0]
            current_time = int(current_time.split(":")[0]) * 60 + int(current_time.split(":")[1])

            print(current_time)
            print(end_time)

            time.sleep(end_time - current_time)
            while end_time - current_time:
                current_time = driver.find_element_by_xpath(
                    '//span[@class="jw-text jw-reset jw-text-elapsed"]').get_attribute(
                    'outerHTML')
                current_time = current_time.split(">")[1]
                current_time = current_time.split("<")[0]
                current_time = int(current_time.split(":")[0]) * 60 + int(current_time.split(":")[1])

            driver.switch_to.window(window_after)
            driver.close()
            driver.switch_to.window(window_before)

    print("end")

# 실행
# 여러 동영상을 실행시키고 싶을 경우
# play(6, 3)
# play(7, 1)
# play(8, 1)
play(week, start)