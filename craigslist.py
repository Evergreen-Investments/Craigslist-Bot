from zcrmsdk.src.com.zoho.api.logger import Logger
Logger.Levels,"."
from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
user = UserSignature(email="cragland@evergreeninvestments.co")
from zcrmsdk.src.com.zoho.crm.api.dc import USDataCenter
environment = USDataCenter.PRODUCTION()
from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken, TokenType
token = OAuthToken(client_id='1000.P2THT3GTDJFKHWY0EYJ4S5HMYOFUUR',client_secret='bbd2d32ced09473fb6e2ad222b6bed99945fec260f',
                   token='GRANT Token', token_type= TokenType.GRANT, redirect_url= 'www.craigslist.com')

# config = {
#     "sandbox":"False",
#     "applicationLogFilePath":"./log",
#     "client_id":"1000.P2THT3GTDJFKHWY0EYJ4S5HMYOFUUR",
#     "client_secret":"bbd2d32ced09473fb6e2ad222b6bed99945fec260f",
#     "redirect_uri":"www.craigslist.com",
#     "token_persistence_path":".",
#     "currentUserEmail":"cragland@evergreeninvestments.co",
# }
#Imports Selenium and connects the program to Chrome
# from selenium.webdriver.common.by import By
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# import os.path

# driver = webdriver.Chrome()

# driver.get('https://post.craigslist.org/')


# #Select Location
# driver.find_element(By.CLASS_NAME, "ui-selectmenu-text").click()

# driver.find_element(By.XPATH,'//li[@id="ui-id-3"]').click()

# driver.find_element(By.XPATH, '//button[@name="go"]').click()

# while True:
#     pass