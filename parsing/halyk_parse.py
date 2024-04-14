from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
import json
import re

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    return driver

def scrape_city_category(city, category):
    driver = setup_driver()
    try:
        url = f"https://halykbank.kz/halykclub#!/{city}/list?category_code={category}&filter"
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'block')))
        blocks = driver.find_elements(By.CLASS_NAME, 'block')

        results = []
        for block in blocks:
            name_elements = block.find_elements(By.XPATH, ".//*[not(contains(text(), ':'))]")
            bonus_elements = block.find_elements(By.XPATH, ".//*[contains(text(), '%')]")

            name = next((el.text for el in name_elements if el.text), None)
            bonus = next((el.text for el in bonus_elements if '%' in el.text and re.match(r'\d{1,2}%', el.text)), None)

            if name and bonus:
                results.append({'city': city, 'category': category, 'name': name, 'bonus': bonus})
        return results
    finally:
        driver.quit()

def main():
    cities = ["1501", "1802", "0101", "0601", "1402", "0702", "1202", "1401", "1201", "2301", "1101", "2201", "0701", "1601", "0501", "1701", "0301", "0901", "1301", "0401", "0802", "0201", "1001", "1901", "0801", "2001"]
    categories = ["supermarketi", "azs", "restorani_kafe", "yuvelirnie_magazini_chasi", "odezhda_muzhskaya_zhenskaya_detskaya_obuv_aksessuari", "universalnie_magazini", "tabachnie_magazini", "elektronika", "tovari_dlya_doma_tekstil_mebel_posuda", "audio_video_knizhnie_kantselyariya", "magazini_kosmetiki", "podarki_suveniri_antikvariat", "stroitelnie_magazini", "tsvetochnie_magazini", "passazhirskie_perevozki", "transportnie_perevozki_logistika_dostavka", "professionalnie_uslugi", "kureri_dostavka_tovara", "kommunalnie_uslugi_televidenie_internet", "uslugi_strakhovaniya", "biznes_uslugi", "saloni_krasoti_parikmakherskie", "fotosaloni_poligrafiya", "kliringovie_kompanii", "sotovaya_svyaz", "detskie_sadi_shkoli_obrazovanie", "detskie_tovari", "meditsinskie_tsentri_kliniki", "apteki", "optika", "stomatologii", "sport", "avtotovari", "avtouslugi", "vetkliniki_i_zoomagazini", "internet_magazini", "zoopark", "galerei_vistavki_ekskursii", "kinoteatri", "bilyard_i_bouling", "teatri_muzei_vistavki", "parki_otdikha_i_razvlechenii", "oteli_i_moteli", "turisticheskie_agentstva", "zh_d_kassi", "aviakompanii", "dyuti_fri", "optovie_postavshchiki_i_proizvoditeli", "komissionnie_magazini_second_hand", "internet_obyavleniya", "internet_banking", "gosudarstvennie_uslugi", "chlenskie_organizatsii", "blagotvoritelnie_organizatsii", "kuponnie_servisi_prodazha_biletov", "mikrokrediti_finuslugi_lombardi_terminali_oplati", "pryamoi_marketing_iskhodyashchii_telemarketing"]
    results = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for city in cities:
            for category in categories:
                futures.append(executor.submit(scrape_city_category, city, category))
        for future in futures:
            results.extend(future.result())

    with open('halyk_all.json', 'w') as file:
        json.dump(results, file, indent=4, ensure_ascii=False)
        print('Data has been written to halyk_all.json')

if __name__ == "__main__":
    main()
