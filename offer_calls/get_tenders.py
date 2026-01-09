from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

page_number = 21
count, n_page = 0, 1
html_pages =[]
contents = []
STEPS = ['container_s context-page', # div step 1: class
         'leadCyclelist2', 'leadCycleCContainer', # ul step 2: id, class
         'simple', # li(offer box) step 3: class
         'TitreOffre', # div step 4: class
         'a' # substeps of step 4
         'bx-inf' # div step 5: class
         ]

print('\nStarting webdriver...')
url=f'https://www.business-senegal.com/fre/opportunites/index/page:{n_page}'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Getting the pages to scrap
for page in range(page_number):
    n_page += 1
    driver.get(url)
    html_page = driver.page_source

    print(f'\nCharging Page number: {page}...')
    soup_page = BeautifulSoup(html_page, 'lxml')
    if soup_page and soup_page not in html_pages:
        html_pages.append(soup_page)
        print('page successfully charged...\nAwaiting Parsing..')
        sleep(4)
    else:
        print(f'Page number {page} not successfully charged...')

for html_page in html_pages:
    print('\tParsing Page...')
    div = html_page.find('div', class_=STEPS[0])
    if div:
        print(f'Step 1 successful {len(div)} {STEPS[0]}')
        ul = div.find_all('ul', class_=STEPS[2], id=STEPS[1])
        if ul:
            print(f'\tStep 2 successful: {len(ul)} {STEPS[1]} from {STEPS[0]}')
        else:
            print(f'\tFailed to charge {STEPS[1]} from {STEPS[0]}')

        # li = ul.find('li', class_=STEPS[3])
        # if len(li) > 1:
        #     pass

    else:
        print('Could not parse page...')

def get_tenders(ul):
    for box in ul.find_all('li'):
        offer = box.find('div', class_=STEPS[4])
        if offer:
            title = offer.get_text(strip=True).strip()
            link_for_next = offer.find('a')['href']
