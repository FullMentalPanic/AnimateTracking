import scrapy
from scrapy.crawler import CrawlerProcess
from animatetracking.spiders.animatetracking_spider import animatetracking

if __name__ == "__main__":
  process = CrawlerProcess()
  process.crawl(animatetracking)
  process.start()