import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

from devBG.utils import strip_string, replace_comma


class DevbgItem(scrapy.Item):
    position = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_string, replace_comma),
        output_processor=TakeFirst(),
    )
    company = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_string),
        output_processor=TakeFirst(),
    )
    location = scrapy.Field(
        input_processor=MapCompose(remove_tags, strip_string),
        output_processor=TakeFirst(),
    )
    date = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    link = scrapy.Field(
        output_processor=TakeFirst(),
    )
