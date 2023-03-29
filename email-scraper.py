from bs4 import BeautifulSoup # BeautifulSoup kütüphanesini HTML içeriği ayrıştırmak için,
import requests # requests kütüphanesini HTTP istekleri yapmak için,
import requests.exceptions
import urllib.parse # urllib.parse kütüphanesini URL ayrıştırmak için,
from collections import deque # deque kütüphanesini verimli bir şekilde öğeler eklemek ve çıkarmak için,
import re # re kütüphanesini düzenli ifadeler için içe aktarır.

user_url = str(input("[+] Taranacak Hedef URL'yi Girin: "))
urls = deque([user_url])

scraped_urls = set() # Taranmış olan URL'leri depolar
emails = set() # Tüm e-postaları depolar

count = 0 # count değişkeni, tarama sırasında taranan URL sayısını tutar
try:
    while len(urls):
        count += 1
        if count == 100: # Tarama sınırı 100 verilmiştir    
            break
        # Her tarama döngüsü başlangıcında, bir sonraki URL deque'den çıkarılır ve scraped_urls setine eklenir. 
        # URL, requests.get() fonksiyonu ile alınır ve response adlı değişkene atanır. Ancak, istek bir hata oluşturursa, 
        # except bloğu bu hatayı yakalar ve tarama sırasını devam ettirir
        url = urls.popleft()
        scraped_urls.add(url)

        print("[%d] İşleniyor %s" % (count, url))
        try:
            response = requests.get(url) # URL'deki sayfayı alıyoruz 
        except requests.exceptions.RequestException: # Herhangi bir hata alırsak diğer URL'leri taramaya devam edilir
            continue
        
        # re.findall() kullanılarak sayfadaki e-posta adresleri bulunur ve new_emails adlı bir set'e eklenir
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails) # Oluşturduğumuz emails setine bulduğumuz emailleri update yöntemiyle ekliyoruz 

        soup = BeautifulSoup(response.text, features="lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if "href" in anchor.attrs else ''
            if link.startswith("/"):
                link = urllib.parse.urljoin(user_url, link)
            elif not link.startswith("http"):
                link = urllib.parse.urljoin(url, link)
            if not link in urls and not link in scraped_urls:
                urls.append(link)
except KeyboardInterrupt:
    print("[-] Kapanış!")

for mail in emails:
    print(mail)