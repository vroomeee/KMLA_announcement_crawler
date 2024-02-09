from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Options
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)

# Get login info
import pickle
with open('../private/passwords.pickle', 'rb') as f:
    login_info = pickle.load(f)

# Instantiate a WebDriver object (for example, using Chrome)
driver = webdriver.Chrome(options=chrome_options)  # Change to appropriate web driver

# Navigate to the login page of the website
driver.get("https://kmlaonline.net/")

# Find the username and password input fields and fill them with your credentials
username_xpath = '//*[@id="downform_login"]/div/div[1]/div[1]/input'
password_xpath = '//*[@id="downform_login"]/div/div[1]/div[2]/input'
username_field = driver.find_element(By.XPATH, username_xpath)
password_field = driver.find_element(By.XPATH, password_xpath)
username_field.send_keys(login_info["kmlaonline"][0])
password_field.send_keys(login_info["kmlaonline"][1])

# Login
login_button_xpath = '//*[@id="cmdLoginPage"]'
login_button = driver.find_element(By.XPATH, login_button_xpath)
login_button.click()

# New announcement
def append_announcement():
    global history
    with open('../private/history/kmlaonline.txt', 'w', encoding='utf-8') as f:
        for title in titles:
            f.write(title)
            f.write('\n')

# Get announcements
titles = []
writers = []
driver.get("https://kmlaonline.net/board/all_announce")
Announcement_list = driver.find_elements(By.CLASS_NAME, "board_list_item")
for i in Announcement_list:
    comment_num = i.find_elements(By.TAG_NAME, "a")[0].find_elements(By.TAG_NAME, "span")
    if comment_num:
        comment_num_text = comment_num[0].text
        length = len(comment_num_text)
        titles.append(i.find_elements(By.TAG_NAME, "a")[0].text[:-length])
    else:
        titles.append(i.find_elements(By.TAG_NAME, "a")[0].text)
    writers.append(i.find_elements(By.TAG_NAME, "a")[1].text)

history = []
with open('../private/history/kmlaonline.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        history.append(line.rstrip("\n"))
    if history != titles:
        print(history)
        print("\n")
        print(titles)
        append_announcement()
        print("new announcement")
    else:
        print("no new announcements")

