import scrapy


class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['web.archive.org']
    start_urls = ['http://web.archive.org/web/20200715000935/https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    def parse(self, response):
        movies = response.xpath("//div[@class='lister-list']/div")
        for movie in movies:
            name = movie.xpath(".//div[3]/h3/a/text()").get()
            link = movie.xpath(".//div[3]/h3/a/@href").get()

            yield response.follow(url=link, callback=self.parse_movie, meta = {"Movie": name})
           

        next_page = response.xpath("//a[@class='lister-page-next next-page']/@href").get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)
    

    def parse_movie(self, response):
        movie = response.request.meta["Movie"]
        year = response.xpath(".//span[@id='titleYear']/a/text()").get()
        duration = response.xpath("normalize-space(//time[@datetime='PT142M']/text())").get()
        genre = response.xpath("//div[@class='subtext']/a/text()").get()
        rating = response.xpath("//span[@itemprop='ratingValue']/text()").get()
        summary = response.xpath("normalize-space(//div[@class='summary_text']/text())").get()

        yield {
            "Movie": movie,
            "Rating": rating,
            "Genre": genre,
            "Summary": summary,
            "Duration": duration,
            "Year": year
            
        }
