import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # to wait for elements to load
from selenium.webdriver.support import expected_conditions as EC

element_list = []

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # brave path
chromedriver_path = r"chromedriver-win64\chromedriver.exe"  # path to chromwdriver

service = Service(chromedriver_path)

# brave thingz
options = Options()
options.binary_location = brave_path
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)

steamSpecials_url = "https://store.steampowered.com/specials/"
driver.get(steamSpecials_url)

try:
    # Wait for the page to fully load by checking if the document is ready
    WebDriverWait(driver, 480).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )

    time.sleep(5)

    # Scroll down to load more items
    for _ in range(1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    title = WebDriverWait(driver, 480).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "StoreSaleWidgetTitle"))
    )
    rating = WebDriverWait(driver, 480).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "_2nuoOi5kC2aUI12z85PneA"))
    )
    ratingCount = WebDriverWait(driver, 480).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "_1wXL_MfRpdKQ3wZiNP5lrH"))
    )
    # description = WebDriverWait(driver, 480).until(
    #     EC.presence_of_all_elements_located((By.CLASS_NAME, "StoreSaleWidgetShortDesc"))
    # )
    discountPercent = WebDriverWait(driver, 480).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "cnkoFkzVCby40gJ0jGGS4"))
    )
    currentPrice = WebDriverWait(driver, 480).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "_3j4dI1yA7cRfCvK8h406OB"))
    )
    origPrice = WebDriverWait(driver, 480).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "_3fFFsvII7Y2KXNLDk_krOW"))
    )

    # Collect all the elements into the list
    for i in range(len(title)):
        element_list.append({
            "title": title[i].text,
            "rating": rating[i].text if i < len(rating) else "N/A",
            "ratingCount": ratingCount[i].text if i < len(ratingCount) else "N/A",
            # "description": description[i].text if i < len(description) else "N/A",
            "origPrice": origPrice[i].text if i < len(origPrice) else "N/A",
            "discountPercent": discountPercent[i].text if i < len(discountPercent) else "N/A",
            "currentPrice": currentPrice[i].text if i < len(currentPrice) else "N/A"
        })

    # Output the result
    for i in range(len(element_list)):
        print(f"{element_list[i]}\n")
    print(f"Found {len(element_list)} elements")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    driver.quit()