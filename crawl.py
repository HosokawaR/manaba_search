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


def get_page(url):
    sleep(SLEEP_TIME)
    try:
        driver.get(url)
        return False
    except:
        print(f"エラーが発生しました。"
              f"指定されたURL: {url}"
              f"現在のドライバのURL: {driver.current_url}")
        return True


for course_url, course_text in tqdm([(l.get_attribute('href'), l.text) for l in
                                     driver.find_elements_by_css_selector('.courselist-title > a')], desc="コースをスキャン中"):
    # コーストップページ
    if get_page(course_url): continue
    course_top = Node(course_text, parent=root, url=driver.current_url)
    wait.until(EC.title_contains('manaba - course'))
    # コンテンツ一覧ページ
    if get_page(course_url + '_page'): continue
    wait.until(EC.title_contains('manaba - course'))
    for content_url, content_text in [(l.get_attribute('href'), l.text) for l in
                                      driver.find_elements_by_css_selector('.about-contents > div > a')]:
        # コンテンツ一覧ページ
        if get_page(content_url): continue
        wait.until(EC.title_contains('manaba - page'))
        for page_url, page_text in [(l.get_attribute('href'), l.text) for l in
                                    driver.find_elements_by_css_selector('.GRIread > a')]:
            if get_page(page_url): continue
            wait.until(EC.title_contains('manaba - page'))
            Node(page_text, parent=course_top, url=driver.current_url,
                 content=driver.find_element_by_class_name('contentbody-left').text)

    # コースニュース一覧ページ
    if get_page(course_url + '_news'): continue
    wait.until(EC.title_contains('manaba - course'))
    if driver.find_elements_by_class_name('description') and \
            'ニュースはありません。' in driver.find_element_by_class_name('description').text:
        continue
    news_count = int(driver.find_element_by_css_selector(
        '.navigator > div:nth-child(2) > span:nth-child(1)').text.replace('全', '').replace('件', ''))

    for i in range(news_count // 10 + 1):
        # コンテンツページ
        if get_page(course_url + '_news' + f'?start={i * 10 + 1}&pagelen=10'): continue
        wait.until(EC.title_contains('manaba - course'))
        for news_url, news_text in [(l.get_attribute('href'), l.text) for l in
                                    driver.find_elements_by_css_selector('.newstext > a')]:
            if get_page(news_url): continue
            wait.until(EC.title_contains('manaba - course'))
            Node(news_text, parent=course_top, url=driver.current_url,
                 content=driver.find_element_by_class_name('msg-text').text)

tree = RenderTree(root)

with open(f'data/manaba_{int(time())}.pickle', 'wb') as f:
    pickle.dump(tree, f)

driver.quit()
driver.close()
