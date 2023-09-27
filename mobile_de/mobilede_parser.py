from bs4 import BeautifulSoup
import unicodedata
import re

def _parse_number(string):
    """Parse e.g. 43.400 € to 43400 or 12.500 km to 12500"""
    return ("").join(re.findall(r"\d+", string))

def extract_car_data(html):
    page_n = unicodedata.normalize("NFKD", html)
    soup = BeautifulSoup(page_n, 'html.parser')

    data = {}
    data["brand"], data["model"] = soup.find(id="ad-title").get_text().split(" ", 1)
    data["mileage_km"] = _parse_number(soup.find(id="mileage-v").get_text())
    data["price_e"] = _parse_number(soup.find("span", {"data-testid" : "prime-price"}).get_text())
    data["registration"] = soup.find(id="firstRegistration-v").get_text()
    data["electric"] = soup.find(id="fuel-v").get_text() == "Elektro" 
    data["power_kw"] = re.findall(r"\d+", soup.find(id="power-v").get_text())[0]
    data["capacity_kwh"] = _parse_number(s.get_text()) if (s:= soup.find(id="batteryCapacity-v")) else None
    data["automatic"] = soup.find(id="transmission-v") == "Automatik"
    data["undamaged"] = s.get_text() == "Unfallfrei" if  (s := soup.find(id="damageCondition-v")) else None
    data["el_cons_kwh100km"] = (".").join(re.findall(r"(\d+),(\d+)", s.get_text())[0]) if (s:= soup.find(id="envkv.wltp.powerConsumption-v")) else None
    data["features"] = [item.get_text() for item in soup.find(id="features").find_all("div", {"class" : "bullet-list"})]

    return data