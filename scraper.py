import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # to wait for elements to load
from selenium.webdriver.support import expected_conditions as EC

game_deals_list = []

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # brave path
chromedriver_path = r"chromedriver-win64\chromedriver.exe"  # path to chromwdriver

service = Service(chromedriver_path)

# brave thingz
options = Options()
options.binary_location = brave_path
options.add_argument("--start-maximized")
options.add_argument("--headless=new")

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

    game_list_container = WebDriverWait(driver, 480).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_3EdZTDIisUpowxwm6uJ7Iq"))
    )

    # load more deals by clicking Show more button and waiting some
    # hahahahahahaha steam pls don't block, also dont use while true
    # while True:
    for _ in range(300):
        try:
            showMoreBtn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "_2tkiJ4VfEdI9kq1agjZyNz"))
            )

            showMoreBtn.click()

            print(f"Clicked 'Show More' button. ({_})") # lets me know what is happening

            time.sleep(random.uniform(9, 15))

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(5, 13))
        except StaleElementReferenceException as e:
            print(f"StaleElementReferenceException: {e}. Retrying.")
            continue  # retry
        except Exception as e:
            print(f"Error during clicking 'Show More': {e}")
            break  # if the button is no longer available

    individual_game_container = game_list_container.find_elements(By.CLASS_NAME, "gASJ2lL_xmVNuZkWGvrWg")

    for individual_game in individual_game_container:
        try:
            title = individual_game.find_element(By.CLASS_NAME, "StoreSaleWidgetTitle").text
        except:
            title = "N/A"

        try:
            rating = individual_game.find_element(By.CLASS_NAME, "_2nuoOi5kC2aUI12z85PneA").text
        except:
            rating = "N/A"

        try:
            rating_count = individual_game.find_element(By.CLASS_NAME, "_1wXL_MfRpdKQ3wZiNP5lrH").text
        except:
            rating_count = "N/A"

        try:
            discount_percent = individual_game.find_element(By.CLASS_NAME, "cnkoFkzVCby40gJ0jGGS4").text
        except:
            discount_percent = "N/A"

        try:
            current_price = individual_game.find_element(By.CSS_SELECTOR, "div._3NhLu7mTdty7JufpSpz6Re > div._3j4dI1yA7cRfCvK8h406OB").text
        except:
            current_price = "N/A"

        try:
            orig_price = individual_game.find_element(By.CSS_SELECTOR, "div._3NhLu7mTdty7JufpSpz6Re > div._3fFFsvII7Y2KXNLDk_krOW").text
        except:
            orig_price = "N/A"

        if title != "N/A":
            game_deals_list.append({
                "title": title,
                "rating": rating,
                "rating_count": rating_count,
                "orig_price": orig_price,
                "discount_percent": discount_percent,
                "current_price": current_price
            })

    # Output the result
    for game in game_deals_list:
        print(f"{game}\n")
    print(f"Found {len(game_deals_list)} elements")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    driver.quit()