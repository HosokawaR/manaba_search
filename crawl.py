import pickle
from time import sleep, time

from anytree import Node, RenderTree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from config.config import SLEEP_TIME
from config.password import ID, PASSWORD

driver = webdriver.Chrome(
    executable_path='/mnt/d/works/manaba_search/driver/chromedriver.exe')
driver.set_window_position(-1920 / 2, 0)
wait = WebDriverWait(driver, 10)
driver.get('https://manaba.tsukuba.ac.jp/ct/home')
wait.until(EC.title_contains('統一認証システム'))
driver.find_element_by_id('username').send_keys(ID)
driver.find_element_by_id('password').send_keys(PASSWORD)
driver.find_element_by_name('_eventId_proceed').click()
wait.until(EC.title_contains('manaba'))

root = Node('root', parent=None, url=driver.current_url)

for course_url, course_text in tqdm([(l.get_attribute('href'), l.text) for l in
                                     driver.find_elements_by_css_selector('.courselist-title > a')], desc="コースをスキャン中"):
    # コーストップページ
    driver.get(course_url)
    course_top = Node(course_text, parent=root, url=driver.current_url)
    wait.until(EC.title_contains('manaba - course'))
    sleep(SLEEP_TIME)
    # コンテンツ一覧ページ
    driver.get(course_url + '_page')
    wait.until(EC.title_contains('manaba - course'))
    sleep(SLEEP_TIME)
    for content_url, content_text in [(l.get_attribute('href'), l.text) for l in
                                      driver.find_elements_by_css_selector('.about-contents > div > a')]:
        # コンテンツ一覧ページ
        driver.get(content_url)
        wait.until(EC.title_contains('manaba - page'))
        sleep(SLEEP_TIME)
        for page_url, page_text in [(l.get_attribute('href'), l.text) for l in
                                    driver.find_elements_by_css_selector('.GRIread > a')]:
            driver.get(page_url)
            wait.until(EC.title_contains('manaba - page'))
            sleep(SLEEP_TIME)
            Node(page_text, parent=course_top, url=driver.current_url,
                 content=driver.find_element_by_class_name('contentbody-left').text)

    # コースニュース一覧ページ
    driver.get(course_url + '_news')
    wait.until(EC.title_contains('manaba - course'))
    sleep(SLEEP_TIME)
    if driver.find_elements_by_class_name('description') and \
            'ニュースはありません。' in driver.find_element_by_class_name('description').text:
        continue
    news_count = int(driver.find_element_by_css_selector(
        '.navigator > div:nth-child(2) > span:nth-child(1)').text.replace('全', '').replace('件', ''))

    for i in range(news_count // 10 + 1):
        # コンテンツページ
        driver.get(course_url + '_news' + f'?start={i * 10 + 1}&pagelen=10')
        wait.until(EC.title_contains('manaba - course'))
        sleep(SLEEP_TIME)
        for news_url, news_text in [(l.get_attribute('href'), l.text) for l in
                                    driver.find_elements_by_css_selector('.newstext > a')]:
            driver.get(news_url)
            wait.until(EC.title_contains('manaba - course'))
            sleep(SLEEP_TIME)
            Node(news_text, parent=course_top, url=driver.current_url,
                 content=driver.find_element_by_class_name('msg-text').text)

tree = RenderTree(root)

with open(f'data/manaba_{int(time())}.pickle', 'wb') as f:
    pickle.dump(tree, f)

driver.quit()
driver.close()
