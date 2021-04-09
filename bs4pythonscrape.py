import requests
from bs4 import BeautifulSoup
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

with open('keyword_remaining.txt','r', encoding="utf-8") as f:
    keywords = f.readlines()
    keywords = [i.strip() for i in keywords]

total_keys = (len(keywords))
count = 0

for key in keywords:
    count += 1
    final_url = []
    print(f"Keyword: {key} {count} of {total_keys}")
    for page in range(1,18):
        print(f"Page Number: {page}")
        url = f"https://www.openrice.com/zh/hongkong/restaurants?what={key}&page={page}"
        def main():
            res = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
            return res.text
        url = main()

        soup = BeautifulSoup(url, 'html.parser')
        h2 = soup.find_all("h2")
        for anchor in h2:
            a = anchor.find("a")['href']
            a = "https://www.openrice.com"+a
            final_url.append(a)
        if soup.find_all("a", class_="pagination-button next js-next"):
            continue
        else:
            break
    with open("restaurant_url_remaining.txt","a") as f:
        for i in final_url:
            f.write(i+"\n")
