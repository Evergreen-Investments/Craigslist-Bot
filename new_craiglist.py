import requests
import json
import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
# from selenium.webdriver.support.ui import WebDriverWait
# import os.path
from selenium.webdriver.common.by import By

Scope = "ZohoCRM.users.ALL,ZohoCRM.modules.ALL,ZohoCreator.report.READ"
Account_URL = "https://accounts.zoho.com/oauth/v2/token"
Client_ID = "1000.3MT9HACEGK6LGL0FBQTR1A7X431JBE"
Client_Secret = "a607dce0132edb7fd9203e1bf151df54a0e25ac1bb"
Redirect_URI = "https://www.google.com/callback"
Generated_Code = "1000.48608c16dc0d8e020e37299f53b12354.d74686295a1aa3e705bbc381cf4748d4"
Refresh_Token = "1000.30675f2b6ca864315842cd612222485c.ea4452c6c836120f363ed888925aac87"


def generate_refresh_token(client_id, client_secret, redirect_uri, code):
    parameters = dict()
    parameters['grant_type'] = "authorization_code"
    parameters['client_id'] = client_id
    parameters['client_secret'] = client_secret
    parameters['redirect_uri'] = redirect_uri
    parameters['code'] = code
    response = requests.post(Account_URL, data=parameters)
    response_json = json.loads(response.text)
    return response_json['refresh_token']


Refresh_Token = generate_refresh_token(Client_ID, Client_Secret, Redirect_URI, Generated_Code)
print(Refresh_Token)


def generate_access_token(refresh_token, client_id, client_secret, redirect_uri):
    parameters = dict()
    parameters['grant_type'] = "refresh_token"
    parameters['refresh_token'] = refresh_token
    parameters['client_id'] = client_id
    parameters['client_secret'] = client_secret
    parameters['redirect_uri'] = redirect_uri
    # parameters['code'] = code
    response = requests.post(Account_URL, data=parameters)
    response_json = json.loads(response.text)
    return response_json["access_token"]


Access_Token = generate_access_token(Refresh_Token, Client_ID, Client_Secret, Redirect_URI)
print(Access_Token)


def get_users(access_token):
    url = 'https://www.zohoapis.com/crm/v3/users?type=AllUsers&page=1&per_page=100'

    headers = {
        'Authorization': 'Zoho-oauthtoken {}'.format(access_token)
    }

    response = requests.get(url=url, headers=headers)
    print(response)

    if response is not None:
        print("HTTP status Code : " + str(response.status_code))
        response_json = response.json()
        users = response_json['users']
        for user in users:
            print(user['full_name'])


get_users(Access_Token)


def get_properties_database(access_token):

    authtoken = access_token
    url = 'https://www.zohoapis.com/crm/v3/PropertyDatabase/actions/count'

    headers = {
        'Authorization': 'Zoho-oauthtoken {}'.format(authtoken)
    }

    response = requests.get(url=url, headers=headers)
    response_json = json.loads(response.text)
    count = response_json['count']

    if count > 0:
        pages = count/200
        if 0 < pages < 1:
            no_of_page = 1
        else:
            if pages.is_integer():
                no_of_page = pages
            else:
                no_of_page = int(pages) + 1

    property_database = []
    print(no_of_page)
    for page in range(no_of_page+1):
        if page == 0:
            continue
        elif page == 1:
            url = f"https://www.zohoapis.com/crm/v3/PropertyDatabase?fields=City,State,Postal_Code,Listing_Price,Square_Feet,Beds,Baths,Property_Type,Ticket_Notes&batch_size=200&page={page}"
            headers = {"Authorization": f"Zoho-oauthtoken {authtoken}"}
            response = requests.get(url, headers=headers)
            response_data = response.json().get("data")
            property_database = property_database + response_data
            page_token = response.json().get("info").get("next_page_token")
        else:
            url = f"https://www.zohoapis.com/crm/v3/PropertyDatabase?fields=City,State,Postal_Code,Listing_Price,Square_Feet,Beds,Baths,Property_Type,Ticket_Notes&batch_size=200&page_token={page_token}"
            headers = {"Authorization": f"Zoho-oauthtoken {authtoken}"}
            response = requests.get(url, headers=headers)
            response_data = response.json().get("data")
            if response_data is None:
                print("Response data is None")
                break
            page_token = response.json().get("info").get("next_page_token")
            property_database = property_database + response_data
    return property_database


property_list = get_properties_database(Access_Token)


def week_number():

    today = datetime.date.today()
    iso_week = today.isocalendar()[1]
    return iso_week

# my_list = ["sample" + str(i) for i in range(1, 51)]
# print(my_list)


week_odd = ['sample1', 'sample2', 'sample3', 'sample4', 'sample5', 'sample6', 'sample7', 'sample8', 'sample9', 'sample10', 'sample11', 'sample12', 'sample13', 'sample14', 'sample15', 'sample16', 'sample17', 'sample18', 'sample19', 'sample20', 'sample21', 'sample22', 'sample23', 'sample24', 'sample25', 'sample26', 'sample27', 'sample28', 'sample29', 'sample30', 'sample31', 'sample32', 'sample33', 'sample34', 'sample35', 'sample36', 'sample37', 'sample38', 'sample39', 'sample40', 'sample41', 'sample42', 'sample43', 'sample44', 'sample45', 'sample46', 'sample47', 'sample48', 'sample49', 'sample50', 'sample51']
week_even = week_odd[::-1]
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


def email_assignment():
    mail_assignment = {}
    if week_number() % 2 == 0:
        for mail in week_even:
            mail_assignment[states[week_even.index(mail)]] = mail
    else:
        for mail in week_odd:
            mail_assignment[states[week_odd.index(mail)]] = mail
    # itr = 1
    for prop in property_list:
        # print(prop["State"])
        if prop["State"] is not None and prop["State"] != "" and len(prop) != 0 and prop["State"] in states:
            prop["email"] = mail_assignment[prop["State"]]
            # itr += 1
            # if itr < 10:
            #     print(prop)
            #     itr += 1

    # print(itr)


email_assignment()

# print(get_properties_database(Access_Token))

browser = webdriver.Chrome('/Applications/PythonBotClass/selenium_tutorial/chromedriver')

browser.get('https://post.craigslist.org/')

browser.find_element(By.CLASS_NAME, "ui-selectmenu-text").click()
browser.find_element(By.XPATH,'//li[@id="ui-id-3"]').click()
browser.find_element(By.XPATH, '//button[@name="go"]').click()

browser.find_element(By.XPATH, '//input[@name="id" and @value="ho"]').click()

browser.find_element(By.XPATH, '//input[@name="id" and @value="144"]').click()

browser.find_element(By.XPATH, '//button[@name="go"]').click()

title_area = browser.find_element(By.XPATH, '//input[@name="PostingTitle" and @id="PostingTitle"]')
title_area.send_keys("Bed, Baths, city, State")

city = browser.find_element(By.XPATH,'//input[@name= "geographic_area" and @id="geographic_area"]')
city.send_keys("atlanta")

postal = browser.find_element(By.XPATH,'//input[@name= "postal" and @id="postal_code"]')
postal.send_keys("30033")

description = browser.find_element(By.XPATH,'//textarea[@name= "PostingBody" and @id="PostingBody"]')
description.send_keys("ticket notes")

price = browser.find_element(By.XPATH,'//input[@name= "price"]')
price.send_keys("1000")

sqft = browser.find_element(By.XPATH,'//input[@name= "surface_area"]')
sqft.send_keys("123")

house_type = browser.find_element(By.XPATH,'//span[@id = "ui-id-1-button"]').click()

actions = ActionChains(browser)

for x in range (5):
    actions.send_keys(Keys.ARROW_DOWN)
actions.send_keys(Keys.ENTER).click()
actions.perform()


laundry = browser.find_element(By.XPATH,'//span[@id = "ui-id-2-button"]').click()
actions = ActionChains(browser)
for x in range (2):
    actions.send_keys(Keys.ARROW_DOWN)
actions.send_keys(Keys.ENTER).click()
actions.perform()

parking  = browser.find_element(By.XPATH,'//span[@id = "ui-id-3-button"]').click()
actions = ActionChains(browser)

for x in range (5):
    actions.send_keys(Keys.ARROW_DOWN)
actions.send_keys(Keys.ENTER).click()
actions.perform()

browser.find_element(By.XPATH, '//input[@name="show_phone_ok" and @value="1"]').click()
phone_number = browser.find_element(By.XPATH,'//input[@name= "contact_phone"]')
phone_number.send_keys("888-299-4429")

contact_name = browser.find_element(By.XPATH,'//input[@name= "contact_name"]')
contact_name.send_keys("Evergreen Investments.co")

browser.find_element(By.XPATH, '//input[@name="has_license" and @value="1"]').click()
license = browser.find_element(By.XPATH,'//input[@name= "license_info"]')
license.send_keys("342184")
email = browser.find_element(By.XPATH,'//input[@name= "FromEMail"]')
email.send_keys("destiny.barbery@gmail.com")
browser.find_element(By.XPATH, '//button[@name="go" and @value="continue"]').click()
browser.find_element(By.XPATH, '//button[@class="continue bigbutton"]').click()
time.sleep(3)

browser.find_element(By.XPATH, '//button[@value="Done with Images"]').click()
browser.find_element(By.XPATH, '//button[@class="button"]').click()
time.sleep(15)
