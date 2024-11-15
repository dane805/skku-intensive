from bs4 import BeautifulSoup
from selenium import webdriver
import time
from openai import OpenAI
import pandas as pd

def collect_review_data(url):
    data = {}
    driver.get(url)
    time.sleep(2)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    try:
        tmp = soup.select('div.mrSZf > ul > li')
        for i in tmp:
            review_tag = i.select('div> span')
            title = review_tag[0].get_text()
            num=review_tag[1].get_text()
            index=num.find("원")
            num=num[index+1:]
            data[title]=int(num)
        return data
    except:
        return 1

def collect_UX_data(url):
    data = []
    driver.get(url)
    time.sleep(2)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    tmp = soup.select('div.place_section_content > ul > li')
    for i in range(10):
        try:
            review_tag = tmp[i].select('div.pui__vn15t2')
            title = review_tag[0].get_text()
            data.append(title)
        except:
            break
    return data

def comment_by_gpt(review):
    api= "OPENAPI"
    client=OpenAI(api_key=api)
    question=""
    for i in review:
        question+="'"+i+"', "
    question+="""위 식당 리뷰를 보고 이 식당을 추천하고 싶은 사람의 특징 5가지, 추천하고 싶지 않은 사람의 특징 5가지를 나열해주세요.
    출력 예시는 아래와 같습니다. 출력 형식은 차용하되, 예시의 내용은 사용하지 말아주세요.
    😀 이런 사람들께 추천해요!😀
    ✅ 한식을 현대적으로 재해석한 요리에 관심이 있는 사람
    ✅ 파인다이닝 경험을 처음 하려는 사람
    ✅ 기념일을 특별하게 보내고 싶은 사람
    ✅ 유명 셰프와의 만남을 기대하는 사람
    ✅ 와인 페어링에 관심 있는 사람
    
    😭 이런 사람들께는 추천하지 않아요!😭
    ❎ 푸짐한 식사를 원하는 사람
    ❎ 런치 코스에서 대표 메뉴를 기대하는 사람
    ❎ 즉흥적인 예약을 선호하는 사람
    ❎ 양 대비 가성비를 따지는 사람
    ❎ 조용하고 빠른 식사를 원하는 사람
    """
    completion=client.chat.completions.create(
        model="gpt-4o-mini",

        messages=[{"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}])
    return completion.choices[0].message.content

def solution(lst):
    keyreview=[]
    review=[]
    cnt=1
    for resid in lst:
        kr=""
        url = "https://m.place.naver.com/restaurant/"+resid+"/review/visitor"
        print(cnt,"-", url)
        cnt+=1
        keywords = collect_review_data(url)
        if keywords != 1:
            kr+="✨이런 점이 좋았어요!✨\n"
            for i, v in keywords.items():
                kr+=i+ " - "+ str(v)+"\n"
            keyreview.append(kr)
        else:
            keyreview.append("NaN")
        UXreview = collect_UX_data(url)
        review.append(comment_by_gpt(UXreview))
    return [keyreview, review]

restuarantID= ["1956611146", "1308638160", "1156901477", "1228463080", "1132840035", "195609594", "1165324605", "1141137916", "11845747", "1115814959", "1018077796", "1102909614", "1151061731", "20937806", "1275440974", "1277052112", "1283188906", "1264343790", "1251583945", "1095176086", "31076200", "1477750254", "1369870234", "1690484049", "1303967574", "1881172296", "1406914963", "1066385752", "1775308300", "1040490502", "1929812463", "1838135293", "1720610031", "1705916422", "1417399414", "1817207066", "280965665", "1006746212", "1680427154", "1240206856", "1148721944", "1177219000", "1167070143", "1111023886", "1570882425", "1731553966", "1067519480", "1647309508", "1558813376"]
chef_name = ["오세득", "원투쓰리", "캠핑맨", "최강록", "만찢남", "통닭맨", "남정석", "장호준", "조은주", "안유성", "나폴리 맛피아", "빙그레", "여경래", "최현석", "여경래", "정지선", "히든천재", "간귀", "조지현", "코리안 타코킹", "방기수", "정지선", "장호준", "요리하는 돌아이", "안산 백종원", "김도윤", "본업도 잘하는 남자", "이모카세 1호", "파브리", "최현석", "안유성", "조셉 리저우드", "4.8.100", "장호준", "돌아온 소년", "철가방 요리사", "최현석", "장호준", "오세득", "안산 백종원", "장사천재 조사장", "고프로", "셀럽의 셰프", "캠핑맨", "트리플스타", "평가절하", "고기깡패", "요리하는 돌아이", "장호준"]
driver = webdriver.Chrome()
df=pd.read_excel("excel.xlsx")
data=solution(restuarantID)
df['평가 요약']=data[0]
df["평가"]=data[1]
df["chef_name"]=chef_name
df.to_excel("excel.xlsx",index=False)

# ssh -i "C:\Users\yungg\Downloads\dane_private" natasma13@34.84.106.129
# nohup sudo /opt/app/gce/env/my-env/bin/streamlit run app.py --server.port 80 > output.log 2>&1 &