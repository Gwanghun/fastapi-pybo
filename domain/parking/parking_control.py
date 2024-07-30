from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager


class parking_control:
    def __init__(self, car_number):
        self.car_number = car_number
        self.login_id = "oomool"
        self.login_pw = "764026"
        self.parking_url = "http://112.220.29.190/login"
        self.button_list = [60, 120, 180, 240, 600, 1440]
        self.driver = None

    def open_browser(self):
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # options.add_argument("disable-gpu")
        # options.add_argument("lang=ko_KR")
        # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
        #
        # service = Service(executable_path=ChromeDriverManager().install())
        # self.driver = webdriver.Chrome(service=service, options=options)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = "/usr/bin/google-chrome"

        # service = Service('/path/to/chromedriver')
        service = Service('/home/ubuntu/projects/fastapi-pybo/chromedriver-linux64/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get(self.parking_url)
        # print("브라우저 열기")
        # print(self.driver.title)
        time.sleep(0.5)

    def local_open_browser(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.parking_url)
        time.sleep(0.5)

    def login(self):
        self.driver.find_element(By.ID, value="userId").send_keys(self.login_id)
        self.driver.find_element(By.NAME, value="userPwd").send_keys(self.login_pw)
        self.driver.find_element(By.ID, value="btnLogin").click()
        time.sleep(0.5)
        self.driver.find_element(By.CLASS_NAME, value="modal-btn").click()

    def search_car_number(self):
        input_box = self.driver.find_element(By.ID, value="schCarNo")
        input_box.send_keys(self.car_number)
        # input_box.send_keys(Keys.ENTER)
        self.driver.find_element(By.CLASS_NAME, value="btnS1_1").click()
        time.sleep(0.5)

    def calculate_time(self):
        pattern = r'(?P<hours>\d+)시간\s*(?P<minutes>\d+)분\s*'
        different_time = self.driver.find_element(By.ID, value="differentTime").text

        match = re.match(pattern, different_time)
        total_minutes = 0
        if match:
            hours = int(match.group('hours'))
            minutes = int(match.group('minutes'))
            total_minutes = (hours * 60 + minutes) + 15  # 여분의 15분 추가

        # print(total_minutes)
        if total_minutes > 15:
            return_data = self.click_button(total_minutes)
            return return_data
        else:
            # print("15분 미만 주차시간입니다.")
            self.driver.quit()
            return {
                'result': False,
                'msg': '15분 미만 주차시간 입니다.'
            }
        # time.sleep(5)

    def click_button(self, total_minutes):
        combination = (self.min_buttons_to_exceed_sum(total_minutes))
        for btn, count in combination.items():
            for i in range(count):
                print(btn, count)
                self.driver.find_element(By.XPATH, f"//*[@price='{btn}']").click()
                time.sleep(0.5)
                self.driver.find_element(By.CLASS_NAME, value="modal-btn").click()
                time.sleep(0.5)

        # self.driver.stop()
        time.sleep(0.5)
        return {
            'result': True,
            'msg': '주차등록  완료'
        }

    def min_buttons_to_exceed_sum(self, target):
        # 버튼 값을 큰 순서대로 정렬
        buttons = self.button_list
        buttons.sort(reverse=True)

        total = 0
        clicks = {button: 0 for button in buttons}
        results = []

        def find_combination(total, index, current_clicks):
            if total > target:
                results.append((total, current_clicks.copy()))
                return
            if index >= len(buttons):
                return

            # 현재 버튼을 클릭하는 경우
            current_clicks[buttons[index]] += 1
            find_combination(total + buttons[index], index, current_clicks)

            # 현재 버튼을 클릭하지 않는 경우
            current_clicks[buttons[index]] -= 1
            find_combination(total, index + 1, current_clicks)

        find_combination(total, 0, clicks)

        # 결과 중에서 목표값을 초과하는 최소 합계를 찾기
        min_result = min(results, key=lambda x: x[0])

        return min_result[1]

    def in_car_check(self):
        print("in_car_check")
        find_element = self.driver.find_element(By.CLASS_NAME, value="ev_dhx_skyblue")
        car_number_string = str(self.car_number)
        if car_number_string in find_element.text:
            return_data = self.calculate_time()
            return return_data
        else:
            self.driver.quit()
            return {
                "result": False,
                "msg": "차량번호가 일치하지 않습니다."
            }

    def capture(self):
        self.driver.save_screenshot("capture.png")
        # self.driver.quit()

    def run(self):
        # local 실행인지 server 실행인지
        # self.local_open_browser()
        self.open_browser()
        self.login()
        # self.capture()
        self.search_car_number()
        return self.in_car_check()
        # self.calculate_time()
        # self.program.stop()
