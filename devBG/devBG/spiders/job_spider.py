from devBG.mail_sender import send_email
import scrapy

from devBG.items import DevbgItem
from scrapy.loader import ItemLoader


class RemotePythonJobSpider(scrapy.Spider):
    name = 'job'

    def start_requests(self):
        url = 'https://dev.bg/company/jobs/python/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        jobs = response.css('div.job-list-item')
        for job in jobs:
            link = job.css('a.overlay-link::attr(href)').get()
            request = scrapy.Request(url=link, callback=self.parse_details)
            yield request

        next_page_url = response.xpath(
            '//a[@class="next page-numbers"]/@href').get()

        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse,)

    def parse_details(self, response, **kwargs):
        job = response.css('div.content-container.left-side')

        ldr = ItemLoader(
            item=DevbgItem(),
            selector=job
        )

        ldr.add_css('position', 'h6.job-title')
        ldr.add_css('company', 'span.company-name')
        ldr.add_css('location', 'span.badge')
        ldr.add_css('date', 'li.date-posted time::attr(datetime)')
        ldr.add_value('link', response.url)

        yield ldr.load_item()

    @staticmethod
    def close(spider, reason):
        send_email()
        return super().close(spider, reason)
