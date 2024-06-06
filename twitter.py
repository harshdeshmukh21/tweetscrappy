from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
import random
import config
import datetime
import requests

# MongoDB setup
connection_string = "mongodb+srv://harshdeshmukh21:AFnQKoVpkZmJgLY6@harsh.wu5d5bs.mongodb.net/?retryWrites=true&w=majority&appName=Harsh"
client = MongoClient(connection_string)
db = client['trending_topics']
collection = db['trends']

def scrape_trending_topics():
    proxy_ip = random.choice(config.ips)

    # Set up the Chrome WebDriver
    path = "/Users/harshdeshmukh/Downloads/chromedriver-mac-arm64/chromedriver"
    service = Service(path)
    driver = webdriver.Chrome(service=service)
    
    driver.maximize_window()

    driver.get('https://twitter.com/login')
    
    wait = WebDriverWait(driver, 30)

    # Wait for the login form to load
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="username"]')))

    # Find the username field and enter the username
    username_field = driver.find_element(By.XPATH, '//input[@autocomplete="username"]')
    username_field.send_keys('harshd2110')

    # Find the next button and click it
    next_button = driver.find_element(By.XPATH, "//button[contains(., 'Next')]")
    next_button.click()

    # Wait for the password field to load
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))

    # Find the password field and enter the password
    password_field = driver.find_element(By.XPATH, '//input[@type="password"]')
    password_field.send_keys('qwertyuiopzxcvbnm')

    # Find the login button and click it
    login_button = driver.find_element(By.XPATH, '//button[@data-testid="LoginForm_Login_Button"]')
    login_button.click()
    
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="trend"]')))
    trending_topics = driver.find_elements(By.XPATH, '//div[@data-testid="trend"]')[:5]
    trend_names = [topic.text for topic in trending_topics]
    print(trend_names)

    print(proxy_ip)  # Print the proxy IP address

    # Get the current date and time
    now = datetime.datetime.now()

    # Store the data in MongoDB
    data = {
        'datetime': now,
        'proxy_ip': proxy_ip  # Add the proxy IP address to the data dictionary
    }

    # Add trend names to the data dictionary if available
    if len(trend_names) >= 1:
        data['trend1'] = trend_names[0]
    if len(trend_names) >= 2:
        data['trend2'] = trend_names[1]
    if len(trend_names) >= 3:
        data['trend3'] = trend_names[2]
    if len(trend_names) >= 4:
        data['trend4'] = trend_names[3]
    if len(trend_names) >= 5:
        data['trend5'] = trend_names[4]

    collection.insert_one(data)

    # Close the browser
    driver.quit()

# Call the scrape_trending_topics function
scraped_data = scrape_trending_topics()