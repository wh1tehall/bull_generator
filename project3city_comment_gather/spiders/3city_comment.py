import scrapy


class QuotesSpider(scrapy.Spider):
    name = "3city_quotes"

    def start_requests(self):
        urls = [
            'https://trojmiasto.pl',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        new_links = response.css('div.news-first').re("https://.*html")
        for n in new_links:
            yield response.follow(n,callback=self.parse)
        for q in response.css('div.opinion-wrap div.content::text').extract():
            yield {'quote' : q}
