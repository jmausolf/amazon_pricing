import selenium, time, argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#Your Amazon Credentials File
from credentials import *

#2-Factor Code File
from get_code import *

def two_factor():
    print("[*] Collecting second-factor authentication code...please wait...")
    time.sleep(10)
    #import pdb; pdb.set_trace()
    security_code = return_amazon_code()
    code_box = driver.find_element_by_name("otpCode")
    code_box.send_keys(security_code)
    time.sleep(5)
    code_box.send_keys(Keys.RETURN)
    time.sleep(7)

def login(second_factor=False):
    url = "https://sellercentral.amazon.com/inventory/ref=id_invmgr_dnav_xx_?tbla_myitable=sort:%7B%22sortOrder%22%3A%22DESCENDING%22%2C%22sortedColumnId%22%3A%22date%22%7D;search:;pagination:1;"
    driver.get(url)

    try:
        #Login
        print("Logging into Amazon seller account. The price war will begin momentarily.")
        username = driver.find_element_by_name("email")
        username.send_keys(amazon_email)
        time.sleep(5)

        password = driver.find_element_by_name("password")
        password.send_keys(amazon_password)
        time.sleep(15)
        password.send_keys(Keys.RETURN)

        print(second_factor)
        
        if second_factor is False:
            print("passing second_factor")
            pass
        else:
            print("trying second factor")
            two_factor()

    except:
        #Captcha Catch
        print("[*] Error in Price War: Thrwarted by Captchas")
        pass


## USER FUNCTIONS FOR PRICE CHANGES

#Price Match Inventory (new)
def match_prices(inventory_item):
    #price_match = driver.find_elements_by_link_text("Match price")
    #print(len(price_match))
    for link in inventory_item:
        try:
            link.click()
            time.sleep(2)
        except:
            print("...exception in price matching")
            pass


def beat_price(price):
    price = float(price)
    new_price = round(price - 0.01, 2)
    return str(new_price)


def lower_price(inventory_item):
    current_price = inventory_item.get_attribute('value')
    print("...current price for item = ${}".format(current_price))
    new_price = beat_price(current_price)
    inventory_item.clear()
    inventory_item.send_keys(new_price)
    time.sleep(1)


def save_changes():
    try:
        save_all = driver.find_element_by_link_text("Save all")
        save_all.click()
    except:
        save_all = driver.find_element_by_xpath("//a[@id='a-autoid-2-announce-floating']")
        save_all.click()
    finally:
        pass



## MAIN FUNCTION TO RUN PRICE WAR

def price_war():
    #Select Only Active Inventory
    time.sleep(2)
    radio = driver.find_element_by_xpath("//div[@data-filter-id='Open']")
    radio.click()
    time.sleep(3)

    items = driver.find_elements_by_xpath("//tr[@class='mt-row']")
    len(items)

    index = -1
    matches = 0
    for row in items:
        index +=1
        better_price = row.find_elements_by_link_text("Match price")

        if len(better_price) >= 1:
            #Match price
            matches += 1
            print("Matching price for item {}".format(index))
            match_prices(better_price)

            #Select Inventory Item
            inventory_item = row.find_elements_by_xpath("//input[@maxlength='23']")[index]
            lower_price(inventory_item)
            print("...lowering price for item {}".format(index))

        else:
            pass

    #Save Changes
    save_changes()
    print("[*] Offered better prices for {} items in inventory. The price war is strong.".format(matches))



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", default=900, type=float, help="time in seconds")
    parser.add_argument("-s", "--second_factor", default=False, type=bool, help="enter 2-factor code")
    args = parser.parse_args()

    def deploy_price_war():
        print("[*] DEPLOYING PRICE WAR")

        try:
            login(args.second_factor)
            price_war()
        except:
            print("[*] Error in Price War")
            pass

        print("....the price war will continue in {} minutes. Current time: {}".format(int(args.time/60), time.strftime('%l:%M%p %Z on %b %d, %Y')))


    #Start Price War Loop
    starttime=time.time()
    while True:
        #Start Driver, Run, Close
        driver = webdriver.Firefox()
        driver.implicitly_wait(0)
        deploy_price_war()
        time.sleep(5)
        driver.close()

        #Time Delay: While Loop
        time.sleep(args.time - ((time.time() - starttime) % args.time))
