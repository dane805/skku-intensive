import pandas as pd
from geopy.geocoders import Nominatim
import re

geo_local = Nominatim(user_agent='South Korea')

def simplify_address(address):
    pattern = r"(.+?(로|길) \d+)"
    match = re.search(pattern, address)
    if match:
        return f"{match.group(1)}"
    else:
        return "주소 형식이 맞지 않습니다."

def geocoding(address):
    try:
        geo = geo_local.geocode(address,timeout=10)
        x_y = [geo.latitude, geo.longitude]
        return x_y
    except:
        return [0,0]

df=pd.read_excel("excel.xlsx")
longitude=[]
latitude=[]
for i in df["store_location"]:
    simple_address=simplify_address(i)
    print(simple_address)
    address=geocoding(simple_address)
    longitude.append(address[1])
    latitude.append(address[0])

df["경도"]=longitude
df["위도"]=latitude
print(df.head())
df.to_excel("excel2.xlsx",index=False)
