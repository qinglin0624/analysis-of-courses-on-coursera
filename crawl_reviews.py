import pandas as pd
import requests
import urllib.request
import re
import datetime
import numpy as np

def get_page_num(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    source = requests.get(url=url + '/reviews', headers=headers)
    source.encoding='utf-8'
    source = source.text
    try:
        pages = re.findall('"Go to page \d+"',source)
        pages = sorted([int(p[12:-1]) for p in pages])
        page_num = pages[-1]
        return page_num
    except:
        return np.nan

def get_review(url, page_num):
    if page_num is np.nan:
        return np.nan
    
    dates = []
    for page in range(int(page_num)):
        page_url = url + f'/reviews?page={page+1}&sort=recent'
        try:
            source = urllib.request.urlopen(page_url)
            source = source.read().decode('utf-8')

            date = re.findall('dateOfReview p-x-1s m-b-0 text-secondary font-xs">[\d\s\w,]+', source)
            date = [d[50:] for d in date]
            dates = dates+date
        except:
            pass
    result = ';'.join(dates)
    print(result)
    return result

subject = 'Data Science.csv'
df = pd.read_csv('../input/coursera/'+subject)
urls = df['标题_链接']
reviews = []
start_time_sub = datetime.datetime.now()
print("Start",subject)
for url in urls:
    start_time_url = datetime.datetime.now()
    page_num = get_page_num(url)
    review = get_review(url, page_num)
    reviews.append(review)
    end_time_url = datetime.datetime.now()
    print(url,page_num,end_time_url-start_time_url)
end_time_sub = datetime.datetime.now()
print("End",end_time_sub-start_time_sub)
df["reviews"] = reviews
df.to_csv(subject)
