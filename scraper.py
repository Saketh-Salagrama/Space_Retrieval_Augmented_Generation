from bs4 import BeautifulSoup
import urllib.request
import os
import time
os.makedirs("scraped_data", exist_ok=True)

urls = {
    "isro_timeline": "https://www.isro.gov.in/Timeline.html",
    "isro_missions": "https://www.isro.gov.in/Missions.html",
    "isro_science": "https://www.isro.gov.in/Sciencedata.html",
    "isro_chandrayaan1": "https://www.isro.gov.in/Chandrayaan_1.html",
    "isro_chandrayaan3": "https://www.isro.gov.in/Chandrayaan3.html",
    "isro_mangalyaan": "https://www.isro.gov.in/MarsOrbiterMission.html",
    "isro_aditya_l1": "https://www.isro.gov.in/AdityaL1.html",
    "isro_gaganyaan": "https://www.isro.gov.in/Gaganyaan.html",
    "isro_astrosat": "https://www.isro.gov.in/Astrosat.html",
    "isro_chandrayaan2": "https://www.isro.gov.in/Chandrayaan_2.html",
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        web = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(web, 'html.parser')
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        #cleaning extra lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(lines)
        with open(f"scraped_data/page_{name}.txt", "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Saved {name}")
        time.sleep(2)
    except Exception as e:
        print(f"Failed {name}: {e}")
