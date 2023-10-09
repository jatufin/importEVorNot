from bs4 import BeautifulSoup
import unicodedata
import re

def _parse_number(string):
    """Parse e.g. 43.400 € to 43400 or 12.500 km to 12500"""
    return ("").join(re.findall(r"\d+", string))

def _parse_capacity(s):
    return re.findall("(\d{2,3})\s*kWh", s.get_text(), re.I) if s else []

def _get_capacity(soup):
    res = _parse_capacity(soup.find(id="batteryCapacity-v"))
    if (res == []):
        res = _parse_capacity(soup.find("div", {"class": "listing-title"}).find("div", {"class": "listing-subtitle"}))
    if (res == []):
        res = _parse_capacity(soup.find("div", {"class", "g-col-12 description"}))
    if len(res):
        return sorted(res, reverse=True)[0]
    return None

def extract_car_data(html):
    page_n = unicodedata.normalize("NFKD", html)
    soup = BeautifulSoup(page_n, 'html.parser')

    data = {}
    data["make"], data["model"] = soup.find(id="ad-title").get_text().split(" ", 1)
    data["modelTypeName"] = soup.find_all(class_='listing-subtitle')[0].get_text()
    data["color"], color_type, *_ = s.get_text().split() + ["Nonmetallic"] if (s:=soup.find(id="color-v")) else [None, None]
    data["metallicColor"] = "Metallic" in color_type
    data["kilometers"] = _parse_number(soup.find(id="mileage-v").get_text())
    data["price"] = _parse_number(soup.find("span", {"data-testid" : "prime-price"}).get_text())
    data["registration"] = s.get_text() if (s:=soup.find(id="firstRegistration-v")) else None
    data["electric"] = soup.find(id="fuel-v").get_text() == "Electric"
    data["power"] = re.findall(r"\d+", soup.find(id="power-v").get_text())[0]
    data["batteryCapacity"] = _get_capacity(soup)
    data["automatic"] = s.get_text() == "Automatic transmission" if (s:=soup.find(id="transmission-v")) else None
    data["undamaged"] = s.get_text() == "Accident-free" if (s := soup.find(id="damageCondition-v")) else None
    data["seats"] = s.get_text() if (s:= soup.find(id="numSeats-v")) else None
    data["leather_upholstery"] = "leather" in s.get_text().lower() if (s:= soup.find(id="interior-v")) else None  
    data["isSUV"] = ("SUV" in s.get_text()) if (s:= soup.find(id="category-v")) else None
    data["airconditioning"] = ("no climatisation" not in s.get_text().lower()) if (s:= soup.find(id="climatisation-v")) else None

    s= soup.find(id="envkv.wltp.powerConsumption-v")
    res = re.findall(r"(\d+,\d+)", s.get_text()) if s else None
    data["elec_cons"] = res[0].replace(",", ".") if res and len(res) else None

    s = soup.find("div", {"class" : "key-feature key-feature--numberOfPreviousOwners"})
    s = s.find("div", {"class" : "key-feature__value"}) if s else None
    data["n_prev_owners"] = s.get_text() if s else None

    data["features"] = [item.get_text() for item in soup.find(id="features").find_all("div", {"class" : "bullet-list"})]
    if (s:= soup.find(id="parkAssists-v")):
        data["features"] = data["features"] + list(map(lambda x: f"Parking sensor: {x.strip()}", s.get_text().split(",")))
        
    return data

def parse_ad_ids(html):
    return re.findall(r"data-listing-id=(\d+)\s", html)