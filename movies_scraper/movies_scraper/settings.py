# -*- coding: utf-8 -*-

# Scrapy settings for movies_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import sys
import os
from django.core.wsgi import get_wsgi_application
import django

sys.path.append("/home/arehovski/PycharmProjects/movies_db")
os.environ['DJANGO_SETTINGS_MODULE'] = "movies_db.settings"
application = get_wsgi_application()
django.setup()

BOT_NAME = 'movies_scraper'

SPIDER_MODULES = ['movies_scraper.spiders']
NEWSPIDER_MODULE = 'movies_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'movies_scraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    'cache-control': "max-age=0",
    # 'cookie': "mda_exp_enabled=1; yandexuid=4857725561592033830; i=PbUFWD5+hVcxlVhnirLl6aTdFHoFUgfc/tWVFPyd3A6eiph/lzzSSBTSfnC7JNkKzUUIUpUa/pn82Mxj48s7hv+4uoA=; _ym_uid=1592037261681435889; mda=0; crookie=1apMJbSQLaoyBFKNcELNl9xWVW72c3F0QBZEHJDoC5gaZ6mbTDEB2ytAMhfqk3eMsOUZIe6ZSMF/5PiooVVcvnXPR6g=; cmtchd=MTU5MjAzNzI2MDg3MA==; location=1; mobile=no; yuidss=4857725561592033830; my_perpages=%5B%5D; users_info[check_sh_bool]=none; _ym_wasSynced=%7B%22time%22%3A1592414477252%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; yp=1592500877.yu.4857725561592033830; ymex=1595006477.oyu.4857725561592033830; tc=182; ya_sess_id=noauth:1592484250; ys=c_chck.54300311; mda2_beacon=1592484250713; sso_status=sso.passport.yandex.ru:synchronized; gdpr=0; user-geo-region-id=157; user-geo-country-id=69; desktop_session_key=b7c2763b512031e7a6f3f018f79d13bbc1fb5da50594d62ba223c8576c9d70476145fd54de1fe4d2b49e87fb2812128db69af7333d57bfe3ceb37f6df97de520a99706fadc69645c80076e5bec76060c2026060957e26918e0c8e87362ddc68f; desktop_session_key.sig=QjszfgYYN-V_QqVc6aPaWTJdkzg; _ym_visorc_22663942=b; _ym_visorc_52332406=b; _ym_visorc_56177992=b; adblock-warning-toast-hide=1; PHPSESSID=lobkrqtf9s3n3nucradkgagre7; user_country=by; yandex_gid=157; _csrf_csrf_token=P451GDCNICSkMyLI0E9lN1h9yEWtJUzme4cfm-dZY84; _ym_visorc_26812653=b; _ym_isad=1; yandex_plus_metrika_cookie=true; _ym_d=1592489988",
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/83.0.4103.106 Chrome/83.0.4103.106 Safari/537.36"
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'movies_scraper.middlewares.MoviesScraperSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'movies_scraper.middlewares.MoviesScraperDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'movies_scraper.pipelines.MoviesScraperPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FEED_EXPORT_ENCODING = 'utf-8'
