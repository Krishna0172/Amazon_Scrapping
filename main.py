from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

# Initialize Chrome WebDriver with appropriate service and options
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0 Chrome/103.0.0.0"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-3d-apis")
chrome_options.add_argument("--output=/dev/null")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options, service=Service())

# Navigate to Amazon website
web = 'https://www.amazon.in'
driver.get(web)

driver.implicitly_wait(5)

keyword = "wireless charger"
search = driver.find_element(By.ID, 'twotabsearchtextbox')
search.send_keys(keyword)


# click search button
search_button = driver.find_element(By.ID, 'nav-search-submit-button')
search_button.click()
sleep(1)

driver.implicitly_wait(5)

product_asin = []
product_name = []
product_price = []
product_ratings = []
product_ratings_num = []
product_link = []

items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, '
                                                                                       '"s-result-item s-asin")]')))

for item in items:


    # find name
    name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
    product_name.append(name.text)
    print("product Name : ", name.text)


    # find ASIN number
    data_asin = item.get_attribute("data-asin")
    product_asin.append(data_asin)
    print('asin : ', data_asin)


    # find prices
    whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
    if whole_price:
        price = whole_price[0].text
    else:
        price = 0
    print('price : ', price)
    product_price.append(price)


    # find ratings box
    ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

    # find ratings and ratings_num
    if ratings_box:
        ratings = ratings_box[0].get_attribute('aria-label')
        ratings_num = ratings_box[1].get_attribute('aria-label')
    else:
        ratings, ratings_num = 0, 0

    print('ratings : ', ratings)
    print('ratings_num : ', ratings_num)
    product_ratings.append(ratings)
    product_ratings_num.append(str(ratings_num))

    # //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/div/div/span/div/div/div/div[2]/div/div/div[1]/h2/a


    # find link
    link = item.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div['
                                       '3]/div/div/div/div/span/div/div/div/div[2]/div/div/div['
                                       '1]/h2/a').get_attribute("href")
    print('link : ', link)
    product_link.append(link)

    print('..........................................................................................................')

# Create a DataFrame using the scraped data
data = {
    'Product Name': product_name,
    'ASIN': product_asin,
    'Price': product_price,
    'Ratings': product_ratings,
    'Number of Ratings': product_ratings_num,
    'Link': product_link
}
df = pd.DataFrame(data)

save_directory = 'C:/Users/Admin/Downloads'

# Define the path where you want to save the Excel file

excel_file_name = 'scraped_data.xlsx'

excel_file_path = os.path.join(save_directory, excel_file_name)

# Save the DataFrame to an Excel file

df.to_excel(excel_file_path, index=False)

print("Data has been saved to:", excel_file_path)
