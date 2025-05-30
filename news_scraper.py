import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

news_urls = [
    'https://n.news.naver.com/mnews/article/001/0014371923',
    'https://n.news.naver.com/mnews/article/001/0014372548',
]

def scrap_news(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    try:
        title = soup.select_one('h2.media_end_head_headline').text.strip()
        body = soup.select_one('div#newsct_article').text.strip()
    except Exception as e:
        print(f"[오류] {url} - {e}")
        return None

    return {
        'url': url,
        'title': title,
        'body': body,
        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def save_to_file(news_data):
    if news_data is None:
        return
    os.makedirs('scraped_news', exist_ok=True)
    filename = f"scraped_news/{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"제목: {news_data['title']}\n")
        f.write(f"URL: {news_data['url']}\n")
        f.write(f"스크랩 시각: {news_data['scraped_at']}\n\n")
        f.write(news_data['body'])

for url in news_urls:
    news_data = scrap_news(url)
    save_to_file(news_data)
    print(f"스크랩 완료: {url}")
