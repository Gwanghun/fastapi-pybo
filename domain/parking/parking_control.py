from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re


class parking_control:
    def __init__(self, car_number):
        self.car_number = car_number
        self.login_id = "oomool"
        self.login_pw = "764026"
        self.parking_url = "http://112.220.29.190/login"
        self.button_list = [60, 120, 180, 240, 600, 1440]
        self.driver = None

    def open_browser(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.parking_url)
        time.sleep(2)

    def login(self):
        self.driver.find_element(By.ID, value="userId").send_keys(self.login_id)
        self.driver.find_element(By.NAME, value="userPwd").send_keys(self.login_pw)
        self.driver.find_element(By.ID, value="btnLogin").click()
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME, value="modal-btn").click()

    def search_car_number(self):
        input_box = self.driver.find_element(By.ID, value="schCarNo")
        input_box.send_keys(self.car_number)
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

    def calculate_time(self):
        pattern = r'(?P<hours>\d+)시간\s*(?P<minutes>\d+)분\s*'
        different_time = self.driver.find_element(By.ID, value="differentTime").text
        print(different_time)

        match = re.match(pattern, different_time)
        total_minutes = 0
        if match:
            hours = int(match.group('hours'))
            minutes = int(match.group('minutes'))
            total_minutes = (hours * 60 + minutes) + 15  # 여분의 15분 추가

        print(total_minutes)
        if total_minutes > 15:
            self.click_button(total_minutes)
        else:
            print("15분 미만 주차시간입니다.")
            self.driver.quit()

        time.sleep(5)

    def click_button(self, total_minutes):
        combination = (self.min_buttons_to_exceed_sum(total_minutes))
        for btn, count in combination.items():
            for i in range(count):
                print(btn, count)
                self.driver.find_element(By.XPATH, f"//*[@price='{btn}']").click()
                time.sleep(1)
                self.driver.find_element(By.CLASS_NAME, value="modal-btn").click()
                time.sleep(1)

        # self.driver.stop()
        time.sleep(10)

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

    def run(self):
        self.open_browser()
        self.login()
        self.search_car_number()
        self.calculate_time()
        # self.program.stop()
