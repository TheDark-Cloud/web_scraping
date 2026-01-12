import requests
from bs4 import BeautifulSoup
import re

def get_business_info(url, data=None):
    try:
        print(f"\nScraping: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")
        # data = {"link": url}

        # Organization name (bold/strong)
        name_tag = soup.find("b") or soup.find("strong")
        if name_tag:
            data["organization"] = name_tag.get_text(strip=True)

        # Website: first <a> tag
        first_link = soup.find("a", href=True)
        if first_link:
            data["web_site"] = first_link["href"]

        # Address: first <em> tag
        address_tag = soup.find("em")
        if address_tag:
            data["address"] = address_tag.get_text(strip=True)

        # Phone numbers: extract digits only
        phone_numbers = []
        for text in soup.stripped_strings:
            if "(221)" in text or "Tel" in text or "Fax" in text:
                # Extract digits
                digits = re.findall(r"\d+", text)
                if digits:
                    # Format as +221 XXXXXXXX
                    num = "".join(digits)
                    if num.startswith("221"):
                        num = "+221 " + num[3:]
                    phone_numbers.append(num)
        data["phones"] = list(set(phone_numbers))  # deduplicate

        return data

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None