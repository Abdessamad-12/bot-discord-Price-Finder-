from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from amazoncaptcha import AmazonCaptcha



def scrape_amazon(query):
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.amazon.com/")

    # Solve Captcha
    link = driver.find_element(By.XPATH, "//div[@class='a-row a-text-center']//img").get_attribute('src')
    captcha = AmazonCaptcha.fromlink(link)
    solution = captcha.solve()
    input_solution = driver.find_element(By.ID, "captchacharacters")
    input_solution.clear()
    input_solution.send_keys(solution + Keys.ENTER)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))

    # Search for the provided query
    input_element = driver.find_element(By.ID, "twotabsearchtextbox")
    input_element.clear()
    input_element.send_keys(query + Keys.ENTER)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-component-type='s-search-result']")))




    product_names = []
    product_prices = []
    product_rating = []
    product_link = []


    all_products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

    for product in all_products:
        # name
        name_element = product.find_element(By.XPATH, ".//span[@class='a-size-medium a-color-base a-text-normal']")
        product_names.append(name_element.text)

        # price
        try:
            price_element = product.find_element(By.XPATH, ".//span[@class='a-price-whole']")
            fraction_price = product.find_element(By.XPATH, ".//span[@class='a-price-fraction']")
            product_prices.append(price_element.text + "." + fraction_price.text)
        except:
            product_prices.append("Price not available")

        # rating
        try:
            rating_element = product.find_element(By.XPATH, ".//span[@class='a-icon-alt']")
            product_rating.append(rating_element.get_attribute("textContent"))
        except:
            product_rating.append("Rating not available")
        #link
        link = product.find_element(By.XPATH, ".//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']").get_attribute('href')
        product_link.append(link)



    driver.quit()

    # Convert prices to float and find minimum price
    for price in product_prices:
        if ',' in price:
            float(price.replace(',', ''))
        elif price == 'Price not available':
            pass
        else:
            float(price)

    #product_prices = list(map(float, product_prices))
    price_min = min(product_prices)
    index_min_price = product_prices.index(price_min)

    return product_names[index_min_price] , product_prices[index_min_price], product_rating[index_min_price], product_prices, product_link[index_min_price]





