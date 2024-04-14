import requests
import json
from copy import deepcopy
import time
from tqdm.auto import tqdm

response = requests.get('https://club.forte.kz/partneroffers')

if response.status_code != 200:
    raise Exception(f'Error {response.status_code} when getting Forte partners.')

s = response.text.split('<script id="__NEXT_DATA__" type="application/json">')[1].split("</script>")[0]
data = json.loads(s)
data = data['props']['pageProps']['dynamicComponents'][2]['partners']

forte = [x for x in data if x['cashbak']]

cities = json.load(open('city_bcc.json'))
cities = [x['name'] for x in cities]

sub2parent = json.load(open('sub2parent.json'))

#save to file
with open('forte_all.json', 'w') as outfile:
    json.dump(forte, outfile, indent=4, ensure_ascii=False)

forte2cat = {
    'Авто': 'Авто и мото',
    'Дом и Сад': 'Ремонт',
    'Другие товары': 'Прочее',
    'Еда': 'Кафе и рестораны',
    'Здоровье': 'Здоровье',
    'Красота': 'Красота',
    'Одежда и Аксессуары': 'Одежда и обувь',
    'Развлечения': 'Развлечения',
    'Спорт': 'Спортивные товары',
    'Строительство': 'Ремонт',
    'Туризм и Отели': 'Туризм',
    'Услуги': 'Прочее',
    'Электроника': 'Техника и электроника',
}

forte_processed = []
for f in forte:
    x = {
        'title': f['title'],
        'address': f['addresses'],
        'city': f['city']['name'],
        'category': forte2cat[f['subCategory']['parentCategory']['title']] if f['subCategory']['parentCategory'] else None,
        'cashback': f['cashbak'],
        'bank': 'Forte',
    }
    
    x['main_category'] = sub2parent[x['category']] if x['category'] else None

    if x['city'] == 'Екибастуз':
        x['city'] = "Экибастуз"

    for card in ['Blue', 'Black', 'Solo']:
        x['card'] = card
        forte_processed.append(deepcopy(x))


res = []

begin = time.time()

cities = json.load(open('city_bcc.json'))

response = requests.get('https://partners.org.kz/api/getall')
if response.status_code != 200:
    raise Exception(f'Error {response.status_code} when getting BCC categories.')

categories = response.json()['categories']
id2cat = {x['cat_id']: x['title'].strip() for x in categories}


for city in tqdm(cities):
    for card in ['kartakarta', 'ironcard', 'juniorcard']:
        response = requests.get(f'https://partners.org.kz/api/getpartner?card={card}&page=1&city_id={city["id"]}&per_page=2000')

        if response.status_code != 200:
            raise Exception(f'Error {response.status_code} for city {city["id"]} and card {card} when getting BCC partners.')

        data = response.json()

        data = [x for x in data['data'] if x['cashback']]

        for x in data:
            if x['cashback']:
                x['city_name'] = city['name']
                x['category_name'] = id2cat[int(x['category'])] if x['category'] else None
                for place in x['places']:
                    place['city_name'] = city['name']
        
        res.extend(data)

print('Time taken in seconds ', time.time() - begin)

with open('bcc_all.json', 'w') as outfile:
    json.dump(res, outfile, indent=4, ensure_ascii=False)

bcc2cat = {
 'АЗС': 'АЗС',
 'Авто и мото': 'Авто и мото',
 'Аксессуары': 'Аксессуары',
 'Аптеки': 'Аптеки',
 'Детские товары': 'Детские товары',
 'Кафе и рестораны': 'Кафе и рестораны',
 'Красота и здоровье': 'Красота',
 'Мебель': 'Ремонт',
 'Медицинские центры': 'Здоровье',
 'Мобильные устройства и гаджеты': 'Техника и электроника',
 'Обучение': 'Образование',
 'Одежда и обувь': 'Одежда и обувь',
 'Прочее': 'Прочее',
 'Развлечения': 'Развлечения',
 'Ремонт': 'Ремонт',
 'Спортивные товары': 'Спортивные товары',
 'Стоматологии': 'Здоровье',
 'Супермаркеты': 'Супермаркеты',
 'Товары для дома': 'Ремонт',
 'Туризм': 'Туризм',
 'Украшения': 'Прочее',
 'Электроника': 'Техника и электроника',
}

bcc_processed = []

for b in res:
    for place in b['places']:
        x = {
            'title': b['title'],
            'address': place['city_address'],
            'city': place['city_name'],
            'category': bcc2cat[b['category_name']] if b['category_name'] else None,
            'cashback': b['cashback'],
            'bank': 'BCC',
            'card': b['card_partner']
        }

        x['main_category'] = sub2parent[x['category']] if x['category'] else None,

        bcc_processed.append(deepcopy(x))


halyk = json.load(open('halyk_all.json'))
halyk_cities = {
    "1501": "Астана",
    "1802": "Алматы",
    "0101": "Актобе",
    "0601": "Атырау",
    "1402": "Актау",
    "0702": "Байконыр",
    "1202": "Балкаш",
    "1401": "Жана Озен",
    "1201": "Жезказган",
    "2301": "Казкелен",
    "1101": "Караганда",
    "2201": "Кокшетау",
    "0701": "Кызылорда",
    "1601": "Костанай",
    "0501": "Павлодар",
    "1701": "Петропавлск",
    "0301": "Семей",
    "0901": "Талдыкорган",
    "1301": "Тараз",
    "0401": "Темиртау",
    "0802": "Туркистан",
    "0201": "Уральск",
    "1001": "Усть-Каменогорск",
    "1901": "Шелек",
    "0801": "Шымкент",
    "2001": "Экибастуз"
  }

halyk2cat = {
    "supermarketi": "Супер маркеты",
    "azs": "АЗС и СТО",
    "restorani_kafe": "Рестораны Кафе",
    "yuvelirnie_magazini_chasi": "Ювелирные магазины. Часы",
    "odezhda_muzhskaya_zhenskaya_detskaya_obuv_aksessuari": "Одежда (мужская, женская, детская). Обувь. Аксессуары",
    "universalnie_magazini": "Универсальные магазины",
    "tabachnie_magazini": "Табачные магазины",
    "elektronika": "Электроника",
    "tovari_dlya_doma_tekstil_mebel_posuda": "Товары для дома, текстиль, мебель, посуда",
    "audio_video_knizhnie_kantselyariya": "Аудио-видео. Книжные. Канцелярия",
    "magazini_kosmetiki": "Магазины косметики",
    "podarki_suveniri_antikvariat": "Подарки. Сувениры. Антиквариат",
    "stroitelnie_magazini": "Строительные магазины",
    "tsvetochnie_magazini": "Цветочные магазины",
    "passazhirskie_perevozki": "Пассажирские перевозки",
    "transportnie_perevozki_logistika_dostavka": "Транспортные перевозки. Логистика. Доставка",
    "professionalnie_uslugi": "Профессиональные услуги",
    "kureri_dostavka_tovara": "Курьеры. Доставка товара",
    "kommunalnie_uslugi_televidenie_internet": "Коммунальные услуги. Телевидение. Интернет",
    "uslugi_strakhovaniya": "Услуги страхования",
    "biznes_uslugi": "Бизнес услуги",
    "saloni_krasoti_parikmakherskie": "Салоны красоты. Парикмахерские",
    "fotosaloni_poligrafiya": "Фотосалоны. Полиграфия",
    "kliringovie_kompanii": "Клиринговые компании",
    "sotovaya_svyaz": "Сотовая связь",
    "detskie_sadi_shkoli_obrazovanie": "Детские сады. Школы. Образование",
    "detskie_tovari": "Детские товары",
    "meditsinskie_tsentri_kliniki": "Медицинские центры, клиники",
    "apteki": "Аптеки",
    "optika": "Оптика",
    "stomatologii": "Стоматологии",
    "sport": "Спорт",
    "avtotovari": "Автотовары",
    "avtouslugi": "Автоуслуги",
    "vetkliniki_i_zoomagazini": "Ветклиники и зоомагазины",
    "internet_magazini": "Интернет магазины",
    "zoopark": "Зоопарк",
    "galerei_vistavki_ekskursii": "Галереи. Выставки. Экскурсии",
    "kinoteatri": "Кинотеатры",
    "bilyard_i_bouling": "Бильярд и боулинг",
    "teatri_muzei_vistavki": "Театры. Музеи. Выставки",
    "parki_otdikha_i_razvlechenii": "Парки отдыха и развлечений",
    "oteli_i_moteli": "Отели и мотели",
    "turisticheskie_agentstva": "Туристические агентства",
    "zh_d_kassi": "Ж/Д кассы",
    "aviakompanii": "Авиакомпании",
    "dyuti_fri": "Дьюти фри",
    "optovie_postavshchiki_i_proizvoditeli": "Оптовые поставщики и производители",
    "komissionnie_magazini_second_hand": "Комиссионные магазины. Second hand",
    "internet_obyavleniya": "Интернет-объявления",
    "internet_banking": "Интернет-банкинг",
    "gosudarstvennie_uslugi": "Государственные услуги",
    "chlenskie_organizatsii": "Членские организации",
    "blagotvoritelnie_organizatsii": "Благотворительные организации",
    "kuponnie_servisi_prodazha_biletov": "Купонные сервисы. Продажа билетов",
    "mikrokrediti_finuslugi_lombardi_terminali_oplati": "Микрокредиты. Финуслуги. Ломбарды. Терминалы оплаты",
    "pryamoi_marketing_iskhodyashchii_telemarketing": "Прямой маркетинг – исходящий телемаркетинг"
  }

for x in halyk:
    x['city'] = halyk_cities[x['city']]
    x['category'] = halyk2cat[x['category']]
    x['main_category'] = sub2parent[x['category']]
    x['bank'] = 'Halyk'
    x['card'] = 'Halyk Bonus'
    if x['bonus']:
        x['cashback'] = float(x['bonus'].replace('%', ''))
    else:
        x['cashback'] = 0
    del x['bonus']
    x['address'] = None
    x['title'] = x['name']
    del x['name']

halyk = [x for x in halyk if x['cashback']]

combined = halyk + forte_processed + bcc_processed

for c in combined:
    if c['address'] is None:
        c['address'] = 'Не указано'

#save
with open('combined.json', 'w') as outfile:
    json.dump(combined, outfile, indent=4, ensure_ascii=False)

# delete
response = requests.delete('https://orca-app-mjl8a.ondigitalocean.app/partners/delete_all/')


for i in tqdm(range(0, len(combined), 200)):
    response = requests.post('https://orca-app-mjl8a.ondigitalocean.app/partners/', json=combined[i:i+200])
    if response.status_code != 200:
        print(response.text)
        break
    print(response.status_code)
    print(i)
    print()

print(len(combined))