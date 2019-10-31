from selenium import webdriver
import webbrowser
import requests
from selenium.webdriver.common.keys import Keys
from SupremeInfo import SupremeURL as supremeurl
from SupremeInfo import SupremeData as supremedata
import datetime
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Item format is [keyword,color,catagory,size]
# If item has one size, put its size as "one size" 
items = [
    ['boxer','black','accessories','small'],
    ]

faileditems = []

information = {
    'Name'              :   'First and last name'           ,
    'Email'             :   'Email'                         ,
    'Telephone'         :   'Phone number'                  ,
    'Address'           :   'Street address'                ,
    'City'              :   'City'                          ,
    'Zipcode'           :   'zip code (5 digits)'           ,
    'State'             :   'State, with only 2 characters' ,
    'CreditCardNum'     :   'Card number'                   ,
    'CreditCardCode'    :   'Card security number'          ,
    'CreditCardExpMonth':   'Expiration number'             ,
    'CreditCardExpYear' :   'Expiration year'              
    }

GoogleInformation ={
    "Email"             :   'Google email for sign in',
    "Password"          :   'Password for email'
    }


headers = {
    'Origin': 'http://www.supremenewyork.com',
    'Accept-Encoding': 'gzip, deflate',
    'X-CSRF-Token': 'XD35ugy3PgIuEwQ2GBugO45kRufdJb6+g+QfpMueV0BBj55J/05GwKufSaEe5FDqWf159pP5BF0B3KlfT4hwTA==',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
    'Referer': 'http://www.supremenewyork.com/shop/all',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

def OpenChromedriver():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--window-size=800,800")
    driver = webdriver.Chrome('C:\Users\gurma\Downloads\Chromedriver.exe',chrome_options=chrome_options)

def GoogleSignIn():
    global driver
    driver.get('https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    useremail = driver.find_element_by_id("identifierId")
    useremail.send_keys(GoogleInformation["Email"])
    print("Entering email")
    nextbutton = driver.find_element_by_id("identifierNext").click()
    driver.implicitly_wait(2)
    password = driver.find_element_by_name("password")
    print("Filling in password")
    password.send_keys(GoogleInformation["Password"])
    time.sleep(.2)
    finalbutton = driver.find_element_by_id("passwordNext")
    #finalbutton = WebDriverWait(driver,10).until(
    #        EC.presence_of_element_located((By.ID,'passwordNext')))
    finalbutton.click()
    
def Supreme(s,item):
    keyword=item[0]
    color=item[1]
    catagory=item[2]
    size=item[3]
    foundlink = (supremeurl(keyword,color,catagory))
    print("Getting product link")
    print("Found link : {}".format(foundlink))
    s.get(foundlink)
    information = supremedata(size,foundlink)
    print("Finding add-to-cart information")
    data = [
      ('utf8', '\u2713'),
      ('st', information[1]),
      ('s', information[0]),
      ('commit', 'add to cart'),
    ]
    s.post('http://www.supremenewyork.com{}'.format(information[2]),headers=headers,data=data)

def SupremeAddtoCart(s):
    counter = 0
    itemcounter = 0
    if len(items) == 0:
        return False
    if len(faileditems) != 0:
        for num in faileditems:
            print('-----Item {}-----'.format(num+1))
            try:
                Supreme(s,items[num])
                print("Item {} added to cart".format(num + 1))
            except:
                print("Failed again at adding Item {} to cart".format(num + 1))
    else:
        for item in items:
            print('-----Item {}-----'.format(counter+1))
            try:
                Supreme(s,item)
                print("Item {} added to cart".format(counter + 1))
                itemcounter +=1
            except:
                print("Failed at adding Item {} to cart".format(counter + 1))
                faileditems.append(counter)
            counter +=1
        if itemcounter == 0:
            del faileditems[:]
            return False
        else:
            print("Item(s) added to cart")
    
            

def Checkoutpage(s):
    print("Loading Checkout Page")
    s.get("https://www.supremenewyork.com/checkout")
    for cookie in s.cookies:
        driver.add_cookie({
            'name': cookie.name, 
            'value': cookie.value,
            'path': '/',
            'domain': cookie.domain})
    driver.get("https://www.supremenewyork.com/checkout")
    name = driver.find_element_by_id("order_billing_name").send_keys(information["Name"])
    email = driver.find_element_by_id("order_email").send_keys(information["Email"])
    tel = driver.find_element_by_id("order_tel")
    address = driver.find_element_by_id("bo").send_keys(information["Address"])
    zipcode = driver.find_element_by_id("order_billing_zip").send_keys(information["Zipcode"])
    city = driver.find_element_by_id("order_billing_city").send_keys(information["City"])
    state = driver.find_element_by_id("order_billing_state").send_keys(information["State"])
    creditcard = driver.find_element_by_id("nnaerb")
    creditcardmonth = driver.find_element_by_id("credit_card_month").send_keys(information["CreditCardExpMonth"])
    creditcardyear = driver.find_element_by_id("credit_card_year").send_keys(information["CreditCardExpYear"])
    creditcardcode = driver.find_element_by_id("orcer").send_keys(information["CreditCardCode"])
    for i in (information["Telephone"]):
        tel.send_keys(i)
    for i in (information["CreditCardNum"]):
        creditcard.send_keys(i)
    termsbutton = driver.find_element_by_xpath('//*[@id="order_terms"]').click()
    processbutton = driver.find_element_by_xpath('//*[@id="pay"]/input').click()
    print("Done!")
    #dateSTR = datetime.datetime.now().strftime("%H:%M:%S")
    #print(dateSTR)

def main():
    OpenChromedriver()
    print("Starting to sign into Google")
    try:
        GoogleSignIn()
        print("Google Sign in complete")
    except:
        print("Google Signin failed, Try Manually")
    while True:
        fakeinput = raw_input("Press ENTER to start")
        if fakeinput == "":
            print("Starting")
            s = requests.Session()
            while True:
                print("Adding item(s) to cart")
                T = SupremeAddtoCart(s)
                if T == False:
                    print("None of the items could be added")
                else:
                    if len(faileditems) != 0:
                        SupremeAddtoCart(s)
                    print("-----Checking Out-----")
                    Checkoutpage(s)
                    break
            break



if __name__ == "__main__":
    print("Starting Bot")
    main()
        

