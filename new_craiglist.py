import requests
import json
import datetime
from datetime import  datetime, timedelta
from zoneinfo import ZoneInfo
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support.select import Select
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


# def generate_refresh_token(client_id, client_secret, redirect_uri, code):
#     parameters = dict()
#     parameters['grant_type'] = "authorization_code"
#     parameters['client_id'] = client_id
#     parameters['client_secret'] = client_secret
#     parameters['redirect_uri'] = redirect_uri
#     parameters['code'] = code
#     response = requests.post(Account_URL, data=parameters)
#     response_json = json.loads(response.text)
#     return response_json['refresh_token']
#
#
# Refresh_Token = generate_refresh_token(Client_ID, Client_Secret, Redirect_URI, Generated_Code)
# print(Refresh_Token)


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
    us_eastern_dt = str(datetime.now(tz=ZoneInfo("America/New_York")).strftime("%Y-%m-%d"))
    us_eastern_dt_week = str((datetime.now(tz=ZoneInfo("America/New_York")) + timedelta(days=7)).strftime("%Y-%m-%d"))
    authtoken = access_token
    url = f'https://www.zohoapis.com/crm/v3/PropertyDatabase/actions/count?criteria=(Created_Date:equals:{us_eastern_dt} and {us_eastern_dt_week})'

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
    else:
        no_of_page = 0

    property_database = []
    print(no_of_page)
    for page in range(no_of_page+1):
        if page == 0:
            continue
        # elif page == 1:
        #     url = f"https://www.zohoapis.com/crm/v3/PropertyDatabase?fields=City,State,Postal_Code,Listing_Price,Square_Feet,Beds,Baths,Property_Type,Ticket_Notes&batch_size=200&page={page}"
        #     headers = {"Authorization": f"Zoho-oauthtoken {authtoken}"}
        #     response = requests.get(url, headers=headers)
        #     response_data = response.json().get("data")
        #     property_database = property_database + response_data
        #     page_token = response.json().get("info").get("next_page_token")
        else:
            # url = f"https://www.zohoapis.com/crm/v3/PropertyDatabase?fields=City,State,Postal_Code,Listing_Price,Square_Feet,Beds,Baths,Property_Type,Ticket_Notes&batch_size=200&page_token={page_token}"
            # headers = {"Authorization": f"Zoho-oauthtoken {authtoken}"}
            # response = requests.get(url, headers=headers)
            # response_data = response.json().get("data")
            # if response_data is None:
            #     print("Response data is None")
            #     break
            # page_token = response.json().get("info").get("next_page_token")
            # property_database = property_database + response_data

            url = f"https://www.zohoapis.com/crm/v3/PropertyDatabase/search?criteria=(Created_Date:between:{us_eastern_dt} and )&page={page}"
            headers = {"Authorization": f"Zoho-oauthtoken {authtoken}"}
            response = requests.get(url, headers=headers)
            print(response)
            response_data = response.json().get("data")
            print(response_data)
            if response_data is None:
                print("Response data is None")
                break
            property_database = property_database + response_data
    return property_database


property_list = get_properties_database(Access_Token)
print(property_list)

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
    states_dict = {}
    i = 0
    for st in states:
        i += 1
        if 0 <= states.index(st) <= 12:
            states_dict[st] = [1, i]
        elif 13 <= states.index(st) <= 25:
            states_dict[st] = [1, i - 13]
        elif 26 <= states.index(st) <= 38:
            states_dict[st] = [1, i - 26]
        else:
            states_dict[st] = [1, i - 39]
    for prop in property_list:
        # print(prop["State"])
        if prop["State"] is not None and prop["State"] != "" and len(prop) != 0 and prop["State"] in states:
            prop["email"] = mail_assignment[prop["State"]]
            prop["xpath_rule"] = states_dict[prop["State"]]
            # itr += 1
            # if itr < 10:
            #     print(prop)
            #     itr += 1

    # print(itr)


email_assignment()

# print(get_properties_database(Access_Token))


def assign_xpath_to_state():
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    states_dict = {}
    i = 0
    for st in states:
        i += 1
        if 0 <= states.index(st) <= 12:
            states_dict[st] = [1, i]
        elif 13 <= states.index(st) <= 25:
            states_dict[st] = [1, i-13]
        elif 26 <= states.index(st) <= 38:
            states_dict[st] = [1, i-26]
        else:
            states_dict[st] = [1, i - 39]
    return states_dict


def navigate_to_craigslist(property):
    driver = webdriver.Chrome('C://Users//parth//Downloads//chromedriver_win32//chromedriver.exe')
    while True:
        try:
            # Initialize driver object and go to login site
            driver.get('https://www.craigslist.org/about/sites#US')

            # 'wait' variable, meant to give webpage time to load before accessing elements

            xr = property["xpath_rule"]

            xpath_rule = f"/html/body/article/section/div[3]/div[{xr[0]}]/h4[{xr[1]}]/li[1]/a"
            wait = WebDriverWait(driver, 30)
            city_btn = wait.until(
                EC.visibility_of_element_located((By.XPATH, xpath_rule)))
            city_btn.click()
            for_sale_btn = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="sss"]/h3/a')))
            for_sale_btn.click()
            post_btn = wait.until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'bd-button text-only cl-goto-post link-like')))
            post_btn.click()
            return driver
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException) as exception:
            print(f"ERROR: {exception}")
            continue


def post_on_craigslist(driver, property):
    while True:
        try:
            wait = WebDriverWait(driver, 30)

            title_area = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//input[@name="PostingTitle" and @id="PostingTitle"]')))
            title_area.send_keys(f"{property['Beds']}, {property['Baths']}, {property['City']}, {property['State']}")

            city = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//input[@name= "geographic_area" and @id="geographic_area"]')))
            city.send_keys(f"{property['City']}")

            postal = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//input[@name= "postal" and @id="postal_code"]')))
            postal.send_keys(f"{property['Postal_Code']}")

            description = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//textarea[@name= "PostingBody" and @id="PostingBody"]')))
            description.send_keys(f"{property['Ticket_Notes']}")

            price = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//input[@name= "price"]')))
            price.send_keys(f"{property['Listing_Price']}")

            sqft = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//input[@name= "surface_area"]')))
            sqft.send_keys(f"{property['Square_Feet']}")

            # house type

            house_type = driver.find_element(By.XPATH, '//span[@id = "ui-id-1-button"]').click()
            actions = ActionChains(driver)

            for x in range(5):
                actions.send_keys(Keys.ARROW_DOWN)
            actions.send_keys(Keys.ENTER).click()
            actions.perform()

            # laundry
            laundry = driver.find_element(By.XPATH, '//span[@id = "ui-id-2-button"]').click()
            actions = ActionChains(driver)
            for x in range(2):
                actions.send_keys(Keys.ARROW_DOWN)
            actions.send_keys(Keys.ENTER).click()
            actions.perform()

            # parking
            parking = driver.find_element(By.XPATH, '//span[@id = "ui-id-3-button"]').click()
            actions = ActionChains(driver)

            for x in range(5):
                actions.send_keys(Keys.ARROW_DOWN)
            actions.send_keys(Keys.ENTER).click()
            actions.perform()

            driver.find_element(By.XPATH, '//input[@name="show_phone_ok" and @value="1"]').click()
            phone_number = driver.find_element(By.XPATH, '//input[@name= "contact_phone"]')
            phone_number.send_keys("729591396")

            contact_name = driver.find_element(By.XPATH, '//input[@name= "contact_name"]')
            contact_name.send_keys("Evergreen Investments.co")

            driver.find_element(By.XPATH, '//input[@name="has_license" and @value="1"]').click()
            license = driver.find_element(By.XPATH, '//input[@name= "license_info"]')
            license.send_keys("342184")
            email = driver.find_element(By.XPATH, '//input[@name= "FromEMail"]')
            email.send_keys(f"{property['email']}")
            driver.find_element(By.XPATH, '//button[@name="go" and @value="continue"]').click()
            driver.find_element(By.XPATH, '//button[@class="continue bigbutton"]').click()
            time.sleep(3)

            driver.find_element(By.XPATH, '//button[@value="Done with Images"]').click()
            driver.find_element(By.XPATH, '//button[@class="button"]').click()
            time.sleep(15)

            return driver
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException) as exception:
            print(f"ERROR: {exception}")
            continue




