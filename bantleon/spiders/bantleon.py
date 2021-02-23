import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bantleon.items import Article


class BantleonSpider(scrapy.Spider):
    name = 'bantleon'
    start_urls = ['https://www.bantleon.com/newsroom/uebersicht']

    def parse(self, response):
        links = response.xpath('//a[@class="is-more"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

        next_pages = response.xpath('//ul[@class="pagination-list"]//a/@href').getall()
        yield from response.follow_all(next_pages, self.parse)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//div[@class="title is-2 "]//text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="column date"]//text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="ce-bodyinnertext"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)
        # item.add_value('author', author)
        # item.add_value('category', category)

        return item.load_item()
