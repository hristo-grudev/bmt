import scrapy

from scrapy.loader import ItemLoader

from ..items import BmtItem
from itemloaders.processors import TakeFirst


class BmtSpider(scrapy.Spider):
	name = 'bmt'
	start_urls = ['https://www.bmt.com/insights/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="wp-block-buttons"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="posted-on"]/text()').get()[3:]

		item = ItemLoader(item=BmtItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
