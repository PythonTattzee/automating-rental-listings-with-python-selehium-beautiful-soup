import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# here we connect to the Service with rental linstings so we could scape the data that we need with BeautifulSoup
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
language = "en,en-US;q=0.9"
endpoint = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
headers = {
    "User-Agent": user_agent,
    "Accept-Language": language
}
response = requests.get(endpoint, headers=headers)
rental_page = response.text

# Now we can create the soup object and locate all the listings from a service,
# so we can work with it later for the for loop
soup = BeautifulSoup(rental_page, "html.parser")
articles = soup.find_all("article")

# Here we connect to the Google Form page to work with it using Selenium
chrome_driver_path = "C:/Development/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get("https://forms.gle/R18qdRntB3J9jhbR6")

# Here we locate all the inputs that need to be filled
what_address = driver.find_element(By.XPATH,
                                       '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
what_price = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
what_link = driver.find_element(By.XPATH,
                                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

# Now we will create the for loop to get a hold of a price, address and link for each listing and
# then record each data to the form
for article in articles:
    # locate links
    link = article.find(class_="property-card-link").get("href")
    # also, since some of the links are not full we check each link and if it is not full
    # we add "https://www.zillow.com" so it will become full
    if link[0] == "/":
        link = "https://www.zillow.com" + link
    time.sleep(1)
    # locate price
    price = article.find(name="span").get_text()
    # locate address
    address = article.find(name="address").get_text()
    # now we fill the Google Form with all the information, put each data into corresponding input field
    what_address.send_keys(address)
    what_price.send_keys(price)
    what_link.send_keys(link)
    # finally, locate the submit button and click it to submit the info
    submit_button = driver.find_element(By.CLASS_NAME, "NPEfkd")
    submit_button.click()
    time.sleep(1)
    # after we prompted to a next window we will locate 'next form' button and click it to fill new form
    refresh_form = driver.find_element(By.CLASS_NAME, "c2gzEf")
    refresh_form.click()
    time.sleep(1)
    # Lastly, we will need to locate the form elements again because apparently, after the refresh of the page
    # refresh all your elements (it is only for this case)
    # or you can work with Page object models
    driver.get("https://forms.gle/R18qdRntB3J9jhbR6")

    what_address = driver.find_element(By.XPATH,
                                       '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    what_price = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    what_link = driver.find_element(By.XPATH,
                                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')




