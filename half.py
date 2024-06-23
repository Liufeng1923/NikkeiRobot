import re

import requests
from bs4 import BeautifulSoup
from datetime import datetime


class SimplexUser:
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 Edg/122.0.0.0',
        })
        # self.login()

    def login(self):
        login_url = 'https://shi2024.market-price-forecast.com/json.certify.php'
        data = {
            'accountid': self.user_id,
            'password': self.password
        }
        login_response = self.session.post(login_url, data=data)
        print(login_response)
        if 'true' not in login_response.text:
            print("登陆失败, 账号密码错误")
            self.user_id = input("账号:")
            self.password = input("密码:")
            self.login()
        else:
            print("登陆成功")

    def vote(self, vote_date, price_yen, price_sen):
        vote_status_url = 'https://shi2024.market-price-forecast.com/forecast.daily.php'
        vote_status_soup = self.get_soup(vote_status_url)
        vote_status = vote_status_soup.find('span', class_='voteStatus').text
        if vote_status == '受付済' or vote_status == "受付中":
            vote_url = 'https://shi2024.market-price-forecast.com/json.voteClosingPrice.php'
            formatted_vote_date = datetime(*vote_date)
            date_str = formatted_vote_date.strftime('%Y/%m/%d')
            vote_data = {
                "date": date_str,
                "yen": str(price_yen),
                "sen": str(price_sen),
            }
            vote_response = self.session.post(vote_url, params=vote_data)
            if "true" in vote_response.text:
                print("投票成功")
            else:
                print("投票失败")

        elif vote_status == '受付终了':
            print("投票时间已过")

        else:
            pass

    def auto_vote(self, auto_vote_date, auto_vote_type='average'):
        pass

    def get_average_value(self):
        score_url = "日経平均フォーキャスト - shi2024.html"
        with open(score_url, 'r', encoding='utf-8') as f:
            a = f.read()
        score_soup = BeautifulSoup(a, 'html.parser')
        b = score_soup.find('table', class_='ranking').find_all('td')
        print(b)

    def get_soup(self, target_url):
        text = self.session.get(target_url)
        return BeautifulSoup(text.text, 'html.parser')


if __name__ == '__main__':
    test_user1 = SimplexUser("li.fe.qsbm93ev@gmail.com", "liufeng110")
    test_user1.get_average_value()
