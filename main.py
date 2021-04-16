from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

# Link to Google form - where data will be entered
GOOGLE_FORM = "your_google_form_link"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

apartment_search_url = "https://www.zillow.com/chicago-il/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B" \
                       "%7D%2C%22usersSearchTerm%22%3A%22Chicago%2C%20IL%22%2C%22mapBounds%22%3A%7B%22west%22%3A-88" \
                       ".14870397516606%2C%22east%22%3A-87.25743810602543%2C%22south%22%3A41.62229587325177%2C" \
                       "%22north%22%3A42.10808094448196%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A17426%2C" \
                       "%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22" \
                       "%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000" \
                       "%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22" \
                       "%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B" \
                       "%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22" \
                       "%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C" \
                       "%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C" \
                       "%22isListVisible%22%3Atrue%7D "

website_data = requests.get(apartment_search_url, headers=header)

soup = BeautifulSoup(website_data.text, "html.parser")

links = [tags['href'] for tags in soup.find_all("a", class_="list-card-link list-card-link-top-margin")]
prices = [prices.text[:6].replace("+", "").replace("/m", "").replace(" ", "") for prices in
          soup.find_all("div", class_="list-card-price")]
addresses = [address.text for address in soup.find_all("address", class_="list-card-addr")]

driver = webdriver.Chrome("/Users/nn-admin/Desktop/Python Course/chromedriver")
for i in range(len(links)):
    driver.get(GOOGLE_FORM)

    time.sleep(3)
    address_field = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    address_field.send_keys(addresses[i])
    price_field.send_keys(prices[i])
    link_field.send_keys(links[i])
    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span').click()
