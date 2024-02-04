import scrapy


class SearchDataSpider(scrapy.Spider):
    name = "search_data"
    allowed_domains = ["tradingeconomics.com"]
    start_urls = ["https://tradingeconomics.com/country-list/interest-rate?continent=world"]

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get().strip()
            link = country.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.parse_country, 
                                  meta={'country_name' : name})


    def parse_country(self, response):
        rows = response.xpath("//tr[contains(@class, 'datatable-row')]")

        for row in rows:
            related = row.xpath(".//td/a/text()").get().strip()
            last = float(row.xpath(".//td[2]/text()").get())
            previous = float(row.xpath(".//td[3]/text()").get())
            name = response.request.meta['country_name']

            yield {
                'country_name' : name,
                'related' : related,
                'last' : last,
                'previous' : previous
                }