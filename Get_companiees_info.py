import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Launch Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.emploidakar.com/les-10-meilleures-entreprises-btp-au-senegal/")

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

article = soup.find("div", class_="entry-content single-page")
companies = []

for blocks in article.find_all("h3"):
    company_name = blocks.get_text(strip=True).split('.')[1].strip()
    p_blocks = [p.get_text(strip=True) for p in blocks.find_next_siblings("p", limit=3)]

    info_block = p_blocks[0] if len(p_blocks) > 0 else "BTP"
    address_block = p_blocks[1] if len(p_blocks) > 1 else ""
    contact_block = p_blocks[2] if len(p_blocks) > 2 else ""

    email_match = re.search(r"[\w.-]+@[\w.-]+\.\w+", contact_block)
    email = email_match.group(0) if email_match else ""

    phone_match = re.findall(r"\+?\d[\d\s\-]+", contact_block)
    phones = phone_match if phone_match else []

    addr_match = re.search(r"Adresse\s*:?\s*(.+)", address_block)
    address = addr_match.group(1).strip() if addr_match else address_block

    companies.append({
        "name": company_name,
        "info": info_block,
        "address": address,
        "email": email,
        "phones": phones
    })

driver.quit()

def comp_type(name):
    info = name.get('info', '').lower()
    if 'mines' in info or 'minier' in info:
        name['info'] = 'BTP/MINIER'
    elif 'ong' in info:
        name['info'] = 'ONG'
    elif 'btp' in info or 'btp' not in info:
        name['info'] = 'BTP'
    else:
        name['info'] = 'OTHERS'

for company in companies:
    comp_type(company)

    # Clean up phones: always join if it's a list
    if isinstance(company['phones'], list):
        company['phones'] = ", ".join(company['phones'])
        company['phones'] = company['phones'].strip()
    else:
        company['phones'] = str(company['phones']) if company['phones'] else ""

    # Clean up address: if it's a list, take the first element
    if isinstance(company['address'], list):
        company['address'] = company['address'][0]

    print(company)


# for company in companies:
#     comp_type(company)
#
#     if company['phones']:
#         # Clean up phones: join list into string if multiple
#         if isinstance(company['phones'], list):
#             if len(company['phones']) > 1:
#                 company['phones'] = ", ".join(company['phones'])
#         # Clean up address: if it's a list, take the first element
#             if len(company['address']) == 1:
#                 company['address'] = company['address'][0]
#     else:
#         company['phones'] = ""
#     print(company)

df = pd.DataFrame(companies)
df.to_csv("companies.csv", index=False)
print(f"\\nCompanies saved: {len(df)} companies")
