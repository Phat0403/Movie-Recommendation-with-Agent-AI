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

def click_on_text(driver, text):
    try:
        element = driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
        element.click()
    except Exception as e:
        print(f"Error clicking on text '{text}': {e}")

def get_movie_info_from_link(link):
    driver = get_driver()
    go_to_url(driver, link)
    try:
        image = driver.find_elements(By.XPATH, "//img[@class='gallery-image']")
        poster_path = image[0].get_attribute("src") if image else None
        backdrop_path = image[1].get_attribute("src") if len(image) > 1 else None
        name = driver.find_element(By.XPATH, "//li[@class='product']").text
        director = driver.find_element(By.XPATH, "//div[contains(@class, 'movie-director')]").text.split("\n ")[1]
        actors = driver.find_element(By.XPATH, "//div[contains(@class, 'movie-actress')]").text.split("\n ")[1]
        genres = driver.find_element(By.XPATH, "//div[contains(@class, 'movie-genre')]").text.split("\n ")[1]
        release_date = driver.find_element(By.XPATH, "//div[contains(@class, 'movie-release')]").text.split("\n ")[1]
        duration = driver.find_elements(By.XPATH, "//div[contains(@class, 'movie-actress')]")[1].text.split("\n ")[1]
        language = driver.find_element(By.XPATH, "//div[contains(@class, 'movie-language')]").text.split("\n ")[1]
        rated = driver.find_element(By.XPATH, "//div[contains(@class, 'movie-rating')]").text.split("\n ")[1]
        description = driver.find_elements(By.XPATH, "//div[@class='tab-content']")[0].text
        click_on_text(driver, "Trailer")
        trailer_url = driver.find_elements(By.TAG_NAME, "iframe")
        trailer_url = [iframe.get_attribute("src") for iframe in trailer_url if "youtube" in iframe.get_attribute("src")]
        trailer_url = trailer_url[0] if trailer_url else None
        if trailer_url:
            trailer_url = trailer_url.split("?")[0]
            trailer_url = trailer_url.split("embed/")[-1]
            trailer_url = f"https://www.youtube.com/watch?v={trailer_url}"
        else:
            trailer_url = None
        info = {
            "name": name,
            "director": director,
            "actors": actors,
            "genres": genres,
            "release_date": release_date,
            "duration": duration,
            "language": language,
            "rating": rated,
            "description": description,
            "poster_path": poster_path,
            "backdrop_path": backdrop_path,
            "trailer": trailer_url,
        }
    except Exception as e:
        print(f"Error getting movie info from link '{link}': {e}")
        info = {
            "error": str(e),
            "link": link
        }
    finally:
        driver.quit()
        return info