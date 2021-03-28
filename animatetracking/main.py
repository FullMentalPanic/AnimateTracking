import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from animatetracking import settings as my_settings
from animatetracking.spiders.animatetracking_spider import animatetracking

if __name__ == "__main__":
  crawler_settings = Settings()
  crawler_settings.setmodule(my_settings)
  process = CrawlerProcess(settings=crawler_settings)
  process.crawl(animatetracking)
  process.start()