from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
# from playwright.async_api import async_playwright
import time
import re


class Parking_management:
    def __init__(self, car_number):
        self.login_id = "oomool"
        self.login_pw = "764026"
        self.parking_url = "http://112.220.29.190/login"
        self.car_number = car_number
        self.page = None
        self.program = None
        self.button_list = [60, 120, 180, 240, 600, 1440]

    def connect(self):
        self.program = sync_playwright().start()
        browser = self.program.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(self.parking_url)
        self.page = page
        # return page

    def login(self):
        self.page.fill("input[name='userId']", self.login_id)
        self.page.fill("input[name='userPwd']", self.login_pw)
        self.page.click("input[id='btnLogin']")

    def search_car_number(self):
        self.page.fill("input[id='schCarNo']", self.car_number)
        self.page.keyboard.down('Enter')
        # self.page.click("input[type='button'][value='검색']")

    def make_minutes(self, time_string):
        # 정규식 패턴 - '5시간 20분 ' 을 시간과 분으로 구분
        pattern = r'(?P<hours>\d+)시간\s*(?P<minutes>\d+)분\s*'
        # 정규식 매칭
        match = re.match(pattern, time_string)
        if match:
            hours = int(match.group('hours'))
            minutes = int(match.group('minutes'))
            result = {
                'hours': hours,
                'minutes': minutes
            }
            return result
        else:
            # 프로그램 종료
            print("매칭되지 않았습니다.")
            self.program.stop()
            return False

    def calculate_time(self):
        # 주차한 시간 - id가 differentTime 인 span 태그의 text
        content = self.page.content()
        soup = BeautifulSoup(content, 'html.parser')
        parking_time = soup.find("span", id="differentTime").text
        # parking_time = self.page.querySelector("#differentTime")
        print(parking_time)
        # parking_time 에서 시간과 분을 뽑아서 전체 분으로 계산.
        # 계산된 분 + 15분을 기준 으로 할인유형을 선택 하는 버튼의 조합을 만든다.
        time_data = self.make_minutes(parking_time)
        print(f"time_data : {time_data}")
        total_minutes = (time_data['hours'] * 60 + time_data['minutes']) + 15
        if total_minutes > 15:
            self.click_button(total_minutes)
        else:
            print("15분 미만 주차입니다.")
            self.program.stop()

    def click_button(self, total_minutes):
        combination = (self.min_buttons_to_exceed_sum(total_minutes))
        for btn, count in combination.items():
            for i in range(count):
                print(btn, count)
                self.page.click(f"a[price='{btn}']")
                time.sleep(2)
                self.page.click("a[class='modal-btn']")
                time.sleep(2)

        self.program.stop()

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
        self.connect()
        time.sleep(2)
        self.login()
        time.sleep(2)
        self.page.click("a[class='modal-btn']")
        time.sleep(2)
        self.search_car_number()
        time.sleep(2)
        self.calculate_time()
        time.sleep(5)
