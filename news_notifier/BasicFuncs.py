import os
import time
import pytz
import chromedriver_binary
from bs4 import BeautifulSoup
from datetime import datetime
from telegram_send import send
from selenium import webdriver
from urllib.parse import urljoin
from selenium.webdriver.chrome.options import Options


class BasicFuncs(object):
    """docstring for BasicFuncs."""

    def __init__(self):
        day_range_division = 5
        now = datetime.utcnow()
        tw_tz = pytz.timezone('Asia/Taipei')
        today = now.astimezone(tw_tz).today()

        pre_day_division_str = str(
            (today.day // day_range_division)-1
        ).zfill(2)

        day_division_str = str(today.day // day_range_division).zfill(2)

        pre_filename = f'{today.strftime("%Y%m")}{pre_day_division_str}'
        filename = f'{today.strftime("%Y%m")}{day_division_str}'

        self.is_debug_mode = False

        self.checkpoint_filepath = f'./checkpoint/{filename}.checkpoint'
        self.pre_checkpoint_filepath = \
            f'./checkpoint/{pre_filename}.checkpoint'

        self.islander_base_url = 'https://islander.cc'
        self.islander_event_url = f'{self.islander_base_url}/top30event'

        self.ptt_url = 'https://www.pttweb.cc'
        self.ptt_hot_news_url = f'{self.ptt_url}/hot/all/today'
        self.ptt_trend_threshold = 500

        self.mobile01_url = 'https://www.mobile01.com'
        self.mobile01_hot_news_url = f'{self.mobile01_url}/hottopics.php'
        self.mobile01_trend_threshold = 20

        self.dcard_url = 'https://www.dcard.tw'
        self.dcard_hot_news_url = f'{self.dcard_url}/f'
        self.dcard_trend_threshold = 5000

        self.youtube_url = 'https://www.youtube.com'
        self.youtube_trend_url = \
            f'{self.youtube_url}/channel/UCBcIWZhWqUwknlxikVHQoyA'

        self.get_web_waiting_time = 15
        self.chrome_options = Options()
        self.chrome_options.headless = True
        self.chrome_options.add_argument('--log-level=3')
        self.chrome_options.add_argument(
            'User-Agent={}'.format(
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/39.0.2171.95 '
                'Safari/537.36'
            )
        )

        self.telegram_send_interval = 5

    def get_islander_news(self):
        with webdriver.Chrome(options=self.chrome_options) as web:
            web.get(self.islander_event_url)
            time.sleep(self.get_web_waiting_time)
            islander_page_source = web.page_source

        islander_page_soup = BeautifulSoup(
            islander_page_source, 'html.parser'
        )

        self.all_news_list = []
        specific_type_news_list = islander_page_soup.find(
            'ul', class_='event-list'
        )

        if specific_type_news_list:
            self.all_news_list.extend(
                self.get_islander_news_content(
                    specific_type_news_list.find_all(
                        'li', class_='event-list-item'
                    )
                )
            )

        if self.is_debug_mode:
            self.debug_save_test_data(
                'tests/data/islander.html', islander_page_source
            )

        return self.all_news_list

    def get_islander_news_content(self, web_news_list):
        news_list = []
        saved_news = self.get_saved_news()

        for news in web_news_list:
            news_title = news.find('div', class_='event-title').text
            news_url = urljoin(self.islander_base_url, news.find('a')['href'])
            parsed_news = f'{news_title}\n{news_url}\n'

            is_not_duplicate_news = (
                news_url not in saved_news and
                parsed_news not in self.all_news_list
            )

            if is_not_duplicate_news:
                news_list.append(parsed_news)

        if self.is_debug_mode:
            self.debug_save_test_data(
                'tests/data/islander.txt', news_list
            )

        return news_list

    def create_telegram_send_conf(self):
        if not os.path.exists('telegram-send.conf'):
            telegram_token = os.getenv('TELEGRAM_TOKEN')
            telegram_to = os.getenv('TELEGRAM_TO')

            if not telegram_token or not telegram_to:
                raise Exception(
                    'The telegram-send related info are not in env variable'
                )

            with open('telegram-send.conf', 'w') as conf_file:
                conf_file.write(
                    '[telegram]\n'
                    f'token = {telegram_token}\n'
                    f'chat_id = {telegram_to}'
                )

    def send_notification(self, source, news_list):
        for news in news_list:
            if news:
                news = f'來源：{source}\n{news}'
                send(
                    messages=[news],
                    parse_mode='text',
                    conf='telegram-send.conf',
                )

            time.sleep(self.telegram_send_interval)

    def create_checkpoint(self, news_list):
        os.makedirs(
            os.path.dirname(self.checkpoint_filepath), exist_ok=True
        )

        # Add the change line in the EOL
        if news_list:
            news_list.append('')

        with open(self.checkpoint_filepath,
                  'a+',
                  encoding='utf-8') as check_point_file:
            check_point_file.write('\n'.join(news_list))

    def get_ptt_hot_news(self):
        with webdriver.Chrome(options=self.chrome_options) as web:
            ptt_page_source = ''
            scroll_limit = 3
            screen_height = web.execute_script("return window.screen.height;")
            web.get(self.ptt_hot_news_url)

            for scroll_time in range(1, scroll_limit):
                ptt_page_source += web.page_source
                time.sleep(self.get_web_waiting_time)
                web.execute_script(
                    f'window.scrollTo(0, {screen_height}*{scroll_time});'
                )

        if self.is_debug_mode:
            self.debug_save_test_data(
                'tests/data/ptt.html', ptt_page_source
            )

        ptt_page_soup = BeautifulSoup(ptt_page_source, 'html.parser')

        ptt_news = ptt_page_soup.find_all(
            lambda tag: tag.name == 'div' and
            tag.get('class') == ['e7-container']
        )

        saved_news = self.get_saved_news()
        ptt_news_list = []

        for news in ptt_news:
            try:
                news_url = urljoin(
                    self.ptt_url,
                    news.find('a', class_='e7-article-default')['href']
                )
                news_title = news.find('span', class_='e7-title').span.text
                news_trend = int(news.find('div', class_='e7-grey-text').text)
                parsed_news = f'{news_title}\n{news_url}\n'

                condition = (
                    news_url not in saved_news and
                    parsed_news not in ptt_news_list and
                    news_trend > self.ptt_trend_threshold
                )

                if condition:
                    ptt_news_list.append(parsed_news)
            except Exception as e:
                pass

        if self.is_debug_mode:
            self.debug_save_test_data(
                'tests/data/ptt.txt', ptt_news_list
            )

        return ptt_news_list

    def get_saved_news(self):
        try:
            saved_news = []

            if os.path.exists(self.pre_checkpoint_filepath):
                with open(self.pre_checkpoint_filepath,
                          'r+',
                          encoding='utf-8') as check_point_file:
                    saved_news_raw = check_point_file.read()
                    saved_news.extend(''.join(saved_news_raw).split('\n'))

            with open(self.checkpoint_filepath,
                      'r+',
                      encoding='utf-8') as check_point_file:
                saved_news_raw = check_point_file.read()
                saved_news.extend(''.join(saved_news_raw).split('\n'))

            return saved_news
        except Exception:
            return ''

    def debug_save_test_data(self, filename, content):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(content))

    def get_mobile01_hot_news(self):
        with webdriver.Chrome(options=self.chrome_options) as web:
            web.get(self.mobile01_hot_news_url)
            mobile01_page_source = web.page_source
            time.sleep(self.get_web_waiting_time)

        if self.is_debug_mode:
            self.debug_save_test_data(
                'tests/data/mobile01.html', mobile01_page_source
            )

        mobile01_page_soup = BeautifulSoup(mobile01_page_source, 'html.parser')

        mobile01_news_list = []
        mobile01_news = mobile01_page_soup.find_all(
            'div', class_='l-listTable__tr'
        )

        saved_news = self.get_saved_news()

        for news in mobile01_news:
            if 'data-id' in news.attrs:
                news_link = news.find('a', class_='c-link')
                news_url = urljoin(self.mobile01_url, news_link['href'])
                news_title = news_link.text
                news_trend = int(news.find('div', class_='o-fMini').text)
                news_category = \
                    news.find('ul', class_='l-jumpList').li.a.span.text
                parsed_news = f'[{news_category}] {news_title}\n{news_url}\n'

                condition = (
                    news_url not in saved_news and
                    parsed_news not in mobile01_news_list and
                    news_trend > self.mobile01_trend_threshold
                )

                if condition:
                    mobile01_news_list.append(parsed_news)

        if self.is_debug_mode:
            self.debug_save_test_data(
                'tests/data/mobile01.txt', mobile01_news_list
            )

        return mobile01_news_list

    def get_dcard_hot_news(self):
        with webdriver.Chrome(options=self.chrome_options) as web:
            web.get(self.dcard_hot_news_url)
            dcard_page_source = web.page_source
            time.sleep(self.get_web_waiting_time)

        if self.is_debug_mode:
            self.debug_save_test_data(
                'tests/data/dcard.html', dcard_page_source
            )

        dcard_page_soup = BeautifulSoup(dcard_page_source, 'html.parser')

        dcard_news_list = []
        dcard_news = \
            dcard_page_soup.find('div', class_='dhzTzT').find_all('div')
        saved_news = self.get_saved_news()

        for news in dcard_news:
            try:
                if 'data-index' in news.attrs:
                    news_category = news.find('div', class_='hclFXC').text
                    news_link = news.find('a', class_='iuyCWN')
                    news_url = urljoin(self.dcard_url, news_link['href'])
                    news_title = news_link.span.text
                    news_trend = int(news.find('div', class_='fkFjDX').text)
                    parsed_news = \
                        f'[{news_category}] {news_title}\n{news_url}\n'

                    condition = (
                        news_url not in saved_news and
                        parsed_news not in dcard_news_list and
                        news_trend > self.dcard_trend_threshold
                    )

                    if condition:
                        dcard_news_list.append(parsed_news)
            except Exception:
                pass

        if self.is_debug_mode:
            self.debug_save_test_data(
                'tests/data/dcard.txt', dcard_news_list
            )

        return dcard_news_list

    def get_youtube_trend(self):
        with webdriver.Chrome(options=self.chrome_options) as web:
            web.get(self.youtube_trend_url)
            web.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-shelf-renderer/div[1]/div[2]/yt-horizontal-list-renderer/div[3]/ytd-button-renderer/a/yt-icon-button/button').click()
            youtube_trend_page_source = web.page_source
            time.sleep(self.get_web_waiting_time)

        if self.is_debug_mode:
            self.debug_save_test_data(
                'tests/data/youtube.html', youtube_trend_page_source
            )

        youtube_page_soup = BeautifulSoup(
            youtube_trend_page_source, 'html.parser'
        )

        youtube_trend_list = []
        youtube_trend_videos = \
            youtube_page_soup.find(
                'div', id='scroll-container'
            ).find_all(
                'ytd-grid-video-renderer'
            )

        saved_news = self.get_saved_news()

        for video in youtube_trend_videos:
            try:
                video_a = video.find('a', id='video-title')
                video_url = urljoin(self.youtube_url, video_a['href'])
                video_title = video_a['aria-label']
                parsed_news = f'{video_title}\n{video_url}\n'

                condition = (
                    video_url not in saved_news and
                    parsed_news not in youtube_trend_list
                )

                if condition:
                    youtube_trend_list.append(parsed_news)

            except Exception as e:
                print(e)

        if self.is_debug_mode:
            self.debug_save_test_data(
                'tests/data/youtube.txt', youtube_trend_list
            )

        return youtube_trend_list
