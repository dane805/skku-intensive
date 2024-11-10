import time
import os
from pathlib import Path
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from sqlalchemy import text, create_engine
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_pg_connection():
    ## 환경 변수 셋업
    dotenv_path = Path('..') / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    db_host = os.environ["DB_HOST"]
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']

    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_name}')
    return engine

def check_pg_connection():
    engine = get_pg_connection()
    # 데이터베이스 연결
    with engine.connect() as connection:
        # 버전 확인 쿼리 실행
        result = connection.execute(text("SELECT version();"))
        
        # 결과 출력
        version = result.fetchone()
        print(version[0])

    # 엔진 종료
    engine.dispose()



def _scroll_down_to_bottom(driver):
    scroll_location = driver.execute_script("return document.body.scrollHeight")
    for _ in range(10):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        if scroll_location == scroll_height:
            break
        else:
            scroll_location = driver.execute_script("return document.body.scrollHeight")

def scroll_down_to_bottom(driver):
    ## 끝까지 내리려면 while True로 변경
    for _ in range(100):
        _scroll_down_to_bottom(driver)
        try:
            driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[2]/div[3]/div[2]/div/a/span').click()
        except:
            break


def parse_html(html, store_info):
    
    soup = BeautifulSoup(html, 'html.parser')
    ## 파싱
    res = []
    for li in soup.findAll("ul")[2].findAll("li"):
        user_name = li.find("span").text
        keywords = [key.text for key in li.find("a", attrs={"data-pui-click-code":"visitkeywords"}).findAll("span")]
        review_text = li.find("a", attrs={"data-pui-click-code":"rvshowmore"}).text
        review_dt = li.find("time").text
        raw_text = li.text
        temp_info = [user_name, keywords, review_text, review_dt, raw_text]
        res.append(temp_info)

    print(f"리뷰 수: {len(res)}")

    df = pd.DataFrame(res, columns = ["user_name", "keywords", "review_text", "review_dt", "raw_text"])
    df = df.assign(
        chef_name = store_info["chef_name"], 
        store_name = store_info["store_name"],
        scraped_at = datetime.now()
    )
    print(df.head().to_markdown())

    return df

def load_to_pg(df):

    engine = get_pg_connection()
    df.to_sql('review_raw', engine, if_exists='append', index=False)


def main():
    driver = webdriver.Chrome()

    store_info_list = [
        {"place_id":1477750254, "chef_name":"정지선", "store_name":"티엔미미"},
        {"place_id":1283188906, "chef_name":"히든천재", "store_name":"포노부오노"},
        {"place_id":1018077796, "chef_name":"나폴리맛피아", "store_name":"비아 톨레도 파스타바"},
        {"place_id":1775308300, "chef_name":"파브리", "store_name":"파브리키친"},
        {"place_id":1817207066, "chef_name":"철가방", "store_name":"도량"},
        # {"place_id":1570882425, "chef_name":"트리플스타", "store_name":"트리드"},
        {"place_id":1647309508, "chef_name":"요리하는돌아이", "store_name":"디핀"},
        {"place_id":1132840035, "chef_name":"만찢남", "store_name":"조광"},
        # {"place_id":280965665, "chef_name":"최현석", "store_name":"쵸이닷"},
        ]

    ## Extract
    for store_info in store_info_list[:4]:
        print(f"Start scrap: {store_info['store_name']}")

        driver.get(f"https://m.place.naver.com/restaurant/{store_info['place_id']}/review/visitor")
        ## 느리게 안되면 모바일 페이지로: 
        time.sleep(5) # Let the user actually see something!
        scroll_down_to_bottom(driver)

        ## Transform
        html = driver.page_source   
        df = parse_html(html, store_info)

        ## Load
        # load_to_pg(df)
        df.to_parquet(f"../outputs/temp_{store_info['store_name']}.parquet")
        print(f"End scrap: {store_info['store_name']}")


if __name__ == "__main__":
    main()