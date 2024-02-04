import scrapy


class SportResultSpider(scrapy.Spider):
    name = "sport_result"
    allowed_domains = ["sports.ru"]
    start_urls = ["https://www.sports.ru/football/tournament/rfpl/table/"]

    def parse(self, response):
        teams = response.xpath("//td/div/a")   
        for team in teams:
            name = team.xpath(".//text()").get().strip()
            link = team.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.parse_result, 
                                  meta={'team' : name})
 



    def parse_result(self, response):
        rows = response.xpath("//table[contains(@class, 'stat-table')]/tbody/tr")

        for row in rows:
            season = row.xpath(".//td/a/text()").get()
            rang = row.xpath(".//td[3]/text()").get()
            name = response.request.meta['team']

            if season is not None:

                yield {
                    'team' : name,
                    'season' : season,
                    'rang' : rang
                    }