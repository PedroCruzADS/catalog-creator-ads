from selenium import webdriver
from selenium.webdriver.common.by import By
import json


def get_sku_list(url, num_pages):
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url)

    sku_list = []

    for page_num in range(1, num_pages+1):
        driver.implicitly_wait(10)

        body_tag = driver.find_element(By.TAG_NAME, 'body')

        script_tags = body_tag.find_elements(By.TAG_NAME, 'script')

        for script in script_tags:
            script_text = script.get_attribute('innerHTML')
            if script_text.startswith('{"@context":'):
                json_obj_length = len(json.loads(
                    script_text)['itemListElement'])
                for position in range(json_obj_length):
                    json_obj = json.loads(script_text)[
                        'itemListElement'][position]['item']['sku']
                    if json_obj not in sku_list:
                        sku_list.append(json_obj)

        # Navigate to the next page
        next_page_url = url + '?page=' + str(page_num+1)
        driver.get(next_page_url)

    driver.quit()
    return sku_list
