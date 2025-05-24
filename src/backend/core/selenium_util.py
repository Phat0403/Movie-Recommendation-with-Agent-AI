from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

def get_driver():
    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--verbose")
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    return driver

def go_to_url(driver, url):
    driver.get(url)
    driver.implicitly_wait(10)  # Wait for elements to load

def scroll_down(driver, pixels):
    driver.execute_script(f"window.scrollBy(0, {pixels});")

def get_link_from_element(element):
    try:
        return element.get_attribute("href")
    except Exception as e:
        print(f"Error getting link from element: {e}")
        return None

def get_link_from_elements(elements):
    links = []
    for element in elements:
        link = get_link_from_element(element)
        if link:
            links.append(link)
    return links

def get_basic_info_from_link(link):
    driver = get_driver()
    go_to_url(driver, link)
    name = driver.find_element(By.XPATH, "//h1[@class='heading']").text
    txts = driver.find_elements(By.XPATH, "//span[@class='txt']")
    details = driver.find_elements(By.XPATH, "//div[@class='detail-ct-bd']")
    description = details[0].find_elements(By.TAG_NAME, "li")
    description = [desc.text for desc in description if desc.text]
    description = "\n".join(description)
    content = details[1].find_element(By.TAG_NAME, "p").text
    results = {
        "name": name,
        "category": txts[9].text,
        "duration": txts[10].text,
        "country": txts[11].text,
        "description": description,
        "content": content,
        "movie_link": link
    }
    driver.quit()
    return results