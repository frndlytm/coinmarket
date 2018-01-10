# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector

from coinmarketcap.items import CoinItem


class CoinmarketSpider(Spider):
    """
    CoinMarketCap spider for scraping the table from the index.
    """
    name = 'coinall'
    allowed_domains = ['https://coinmarketcap.com']
    start_urls = ['https://coinmarketcap.com/all/views/all']

    def parse(self, response):
        """
        Follow links to the coin-specific url, and extract the data from there.
        """
        hxs = Selector(response)
        for coin in hxs.xpath('//table[@id="currencies-all"]/tbody/tr'):
            item = CoinItem()
            item['name'] = (
                coin
                .xpath('td/a[@class="currency-name-container"]/text()')
                .extract_first()
            )
            item['symbol'] = (
                coin
                .css('td.col-symbol')
                .xpath('text()')
                .extract_first()
            )
            item['market'] = (
                coin
                .css('.market-cap')
                .xpath('text()')
                .extract_first()
                .strip('\n ')
            )
            item['price'] = (
                coin
                .xpath('td/a[@class="price"]/text()')
                .extract_first()
            )
            item['supply'] = (
                coin
                .css('.circulating-supply')
                .xpath('a/@data-supply')
                .extract_first()
            )
            item['volume'] = (
                coin
                .css('a.volume')
                .xpath('text()')
                .extract_first()
            )
            yield item



class HistoricalSpider(Spider):
    """
    A Spider that crawls the 'root/historical' url
    by iterating through the date links and extracting
    all data to JSON.
    """
    name = 'historical'
    allowed_domains = ['coinmarketcap.com']
    start_urls = ['https://coinmarketcap.com/historical/']

    def parse(self, response):
        """
        Get all date links from historical,
        follow them.
        """
        links = (
            response
            .css('div.row')
            .css('ul.list-unstyled li a::attr(href)')
        )
        for link in links:
            yield response.follow(link, callback=self.parse_table)

    def parse_table(self, response):
        day = response.url.split('/')[-2]
        table = response.css('table#currencies-all')
        for coin in table.xpath('//tbody/tr'):
            item = CoinItem()
            item['histdate'] = day
            item['name'] = (
                coin
                .xpath('td/a[@class="currency-name-container"]/text()')
                .extract_first()
            )
            item['symbol'] = (
                coin
                .css('td.col-symbol')
                .xpath('text()')
                .extract_first()
            )
            item['market'] = (
                coin
                .css('.market-cap')
                .xpath('text()')
                .extract_first()
                .strip('\n ')
            )
            item['price'] = (
                coin
                .xpath('td/a[@class="price"]/text()')
                .extract_first()
            )
            item['supply'] = (
                coin
                .css('.circulating-supply')
                .xpath('a/@data-supply')
                .extract_first()
            )
            item['volume'] = (
                coin
                .css('a.volume')
                .xpath('text()')
                .extract_first()
            )
            yield item
