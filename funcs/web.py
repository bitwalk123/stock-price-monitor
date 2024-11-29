from PySide6.QtTest import QTest

from selenium import webdriver
from selenium.common import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from funcs.config import get_login_info
from structs.web_info import WebInfoRakuten


def do_alert_dialog_check(driver: webdriver.Firefox):
    """アラートダイアログが表示されていれば OK ボタンをクリック

    :param driver:
    :return:
    """
    try:
        wait = WebDriverWait(driver, timeout=2)
        alert = wait.until(lambda d: d.switch_to.alert)
        alert.accept()
    except Exception:
        return False
    else:
        return True


def do_autologout(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    """自動ログアウトの切り替え

    :param driver:
    :param info:
    :return:
    """
    label_autologout = driver.find_element(
        By.CLASS_NAME,
        info.classname['auto-logout-button'],
    )
    label_autologout.click()
    # Alert
    return (do_alert_dialog_check(driver))


def do_credit(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    """国内株式のページ

    :param driver:
    :param info:
    :return:
    """
    li_credit = driver.find_element(
        By.ID,
        info.id['credit'],
    )
    li_credit.click()

    """
    if load_url_class(driver, info.classname['domestic-stock-search-box']):
        return True
    else:
        return False
    """
    return True


def do_domestic(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    """国内株式のページ

    :param driver:
    :param info:
    :return:
    """
    li_domestic = driver.find_element(
        By.ID,
        info.id['domestic'],
    )
    li_domestic.click()
    return True

    # if load_url_class(driver, info.classname['domestic-stock-search-box']):
    #    return True
    # else:
    #    return False


def do_login(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    """ログイン処理

    :param driver:
    :param info:
    :return:
    """
    obj_login = get_login_info()
    # login account
    entry_login = driver.find_element(
        By.ID,
        info.id['login']
    )
    entry_login.clear()
    entry_login.send_keys(obj_login.getLoginID())
    # login password
    entry_passwd = driver.find_element(
        By.ID,
        info.id['passwd']
    )
    entry_passwd.clear()
    entry_passwd.send_keys(obj_login.getPassword())

    # login button
    button_login = driver.find_element(
        By.ID,
        info.id['login-button']
    )
    button_login.submit()

    # check page title
    wait_page_title(driver, info.title['home'])

    # check if specified class exists
    if not load_url_class(driver, info.classname['logout-button']):
        return False
    else:
        return True


def do_login_site(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    """ログイン画面へ移動

    :param driver:
    :param info:
    :return:
    """
    if site_login(driver, info):
        return True
    else:
        return False


def do_logout(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    """ログアウト処理

    :param driver:
    :param info:
    :return:
    """
    button_logout = driver.find_element(
        By.CLASS_NAME,
        info.classname['logout-button']
    )
    button_logout.send_keys(Keys.ENTER)
    # Alert
    if do_alert_dialog_check(driver):
        return True
    else:
        return False


def do_long(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    # 売買 - 買建
    input_buy = driver.find_element(
        By.ID,
        info.id['buy']
    )
    input_buy.click()

    # 信用区分（期限）- 一般（1日）
    input_period = driver.find_element(
        By.ID,
        info.id['general_1d']
    )
    input_period.click()

    # 数量 株/口（入力欄）
    input_shares = driver.find_element(
        By.ID,
        info.id['shares']
    )
    input_shares.clear()
    input_shares.send_keys(info.num_shares)

    # 指値（入力欄）
    input_price = driver.find_element(
        By.ID,
        info.id['order-price']
    )
    input_price.clear()

    # 価格 成行で執行
    input_market_order = driver.find_element(
        By.ID,
        info.id['market-order']
    )
    input_market_order.click()

    return True


def do_short(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    # 売買 - 売建
    input_sell = driver.find_element(
        By.ID,
        info.id['sell']
    )
    input_sell.click()

    # 信用区分（期限）- 一般（1日）
    input_period = driver.find_element(
        By.ID,
        info.id['general_1d']
    )
    input_period.click()

    # 数量 株/口
    input_shares = driver.find_element(
        By.ID,
        info.id['shares']
    )
    input_shares.clear()
    input_shares.send_keys(info.num_shares)

    # 指値（入力欄）
    input_price = driver.find_element(
        By.ID,
        info.id['order-price']
    )
    input_price.clear()

    # 価格 成行で執行
    input_market_order = driver.find_element(
        By.ID,
        info.id['market-order']
    )
    input_market_order.click()

    return True


def do_search(driver: webdriver.Firefox, info: WebInfoRakuten, ticker: str) -> bool:
    """Search ticker

    :param driver:
    :param info:
    :param ticker:
    :return:
    """
    try:
        table_search = driver.find_element(
            By.CLASS_NAME,
            info.classname['domestic-stock-search-box']
        )
    except NoSuchElementException as e:
        print(e)
        return False
    else:
        input_search = table_search.find_element(
            By.ID,
            info.id['domestic-stock-input-box']
        )
        input_search.clear()
        input_search.send_keys(ticker)

        button_search = table_search.find_element(
            By.CLASS_NAME,
            info.classname['domestic-stock-btn-box']
        )
        button_search.click()
        return True

        # check if specified class exists
        # if load_url_class(driver, info.classname['table-stock-price']):
        #    return True
        # else:
        #    return False


def do_update(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    """Update auto-update

    :param driver:
    :param info:
    :return:
    """
    p_auto_update_panel_off = driver.find_element(
        By.ID,
        info.id['auto-update-off-status'],
    )
    p_auto_update_panel_off.click()
    return True


def do_update_button_auto(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    """自動更新 ON ボタン

    :param driver:
    :param info:
    :return:
    """
    try:
        a_update_button_auto = driver.find_element(
            By.ID,
            info.id['auto-update-on-button'],
        )
        a_update_button_auto.click()
    except ElementNotInteractableException as e:
        print(e)
    finally:
        return True


def do_update_button_manual(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    """自動更新 OFF / 手動ボタン

    :param driver:
    :param info:
    :return:
    """
    a_update_button_manual = driver.find_element(
        By.ID,
        info.id['auto-update-off-button'],
    )
    a_update_button_manual.click()
    return True


def get_autologout_checked_status(driver: webdriver.Firefox, info: WebInfoRakuten) -> str:
    """自動ログアウトの状態を取得

    :param driver:
    :param info:
    :return:
    """
    input_autologout = driver.find_element(
        By.ID,
        info.id['auto-logout']
    )
    return input_autologout.get_attribute('checked')


def get_auto_update_status(driver: webdriver.Firefox, info: WebInfoRakuten) -> dict:
    """自動更新の状態取得

    :param driver:
    :param info:
    :return:
    """
    dict_result = dict()
    update_off_select = driver.find_element(
        By.ID,
        info.id['auto-update-off-select']
    )
    dict_result['auto-update-off-select'] = update_off_select.get_attribute('style')

    update_on_select = driver.find_element(
        By.ID,
        info.id['auto-update-on-select']
    )
    dict_result['auto-update-on-select'] = update_on_select.get_attribute('style')

    update_off_status = driver.find_element(
        By.ID,
        info.id['auto-update-off-status']
    )
    dict_result['auto-update-off-status'] = update_off_status.get_attribute('style')

    update_on_status = driver.find_element(
        By.ID,
        info.id['auto-update-on-status']
    )
    dict_result['auto-update-on-status'] = update_on_status.get_attribute('style')

    return dict_result


def get_stock_price(driver: webdriver.Firefox, info: WebInfoRakuten) -> tuple[str, str]:
    """株価情報の取得

    :param driver:
    :param info:
    :return:
    """
    tbl_stock_price = driver.find_element(
        By.CLASS_NAME,
        info.classname['table-stock-price']
    )
    element_stock_price_value = tbl_stock_price.find_element(
        By.CLASS_NAME,
        info.classname['table-stock-price-value']
    )
    price_str = element_stock_price_value.text
    element_stock_price_time = tbl_stock_price.find_element(
        By.CLASS_NAME,
        info.classname['table-stock-price-time']
    )
    time_str = element_stock_price_time.text
    return price_str, time_str


def get_update_status(driver: webdriver.Firefox, info: WebInfoRakuten, ticker: str):
    pass


def load_url_id(driver: webdriver.Firefox, name_id: str) -> bool:
    """Load URL, finished if specified id exists

    :param driver:
    :param name_id:
    :return:
    """
    delay = 5  # seconds
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.ID, name_id))
        )
        return True
    except TimeoutException:
        print('Loading took too much time!')
        return False


def load_url_class(driver: webdriver.Firefox, name_class: str) -> bool:
    """
    Load URL, finished if specified class exists

    :param driver:
    :param name_class:
    :return:
    """
    delay = 5  # seconds
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, name_class))
        )
        return True
    except TimeoutException:
        print('Loading took too much time!')
        return False


def site_login(driver: webdriver.Firefox, info: WebInfoRakuten) -> bool:
    """Login site

    :param driver:
    :param info:
    :return:
    """
    driver.get(info.url_login)
    return load_url_id(driver, info.id['passwd'])


def wait_page_title(driver: webdriver.Firefox, page_title: str):
    """Wait till title of current page becomes specified title

    :param driver:
    :param page_title:
    :return:
    """
    max = 100
    count = 0
    while (driver.title != page_title) & (count < max):
        count += 1
        QTest.qWait(100)
