import scrapy
from reviewscraper.items import ReviewItem

class ReviewSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['obchody.heureka.sk']
    start_urls = ['https://obchody.heureka.sk/?f=1']

    custom_settings = {
        # 'COOKIES_ENABLED': True,
        'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        # 'DOWNLOAD_DELAY': 3
    }

    def parse(self, response):
        stores = response.css('div > a.e-button.e-button--simple')
        for store in stores:
            link = store.attrib['href']
            # print(link.split('overene')[0] + '?f=1')
            yield response.follow(link.split('overene')[0] + '?f=1', self.parse_reviews_page)

        current_page_number = int(response.url.split('=')[-1])
        next_page_number = current_page_number + 1
        next_page_url = f"https://obchody.heureka.sk/?f={next_page_number}"

        if response.css('div > a.e-button.e-button--simple'):
            self.logger.info(f'Following to stores page {next_page_number}')
            yield response.follow(next_page_url, self.parse)
        else:
            self.logger.info('No more store pages to load.')

    def parse_reviews_page(self, response):
        for review in response.css('div.c-post__content.u-normal-spacing'):
            pros = review.css('div.c-post__attributes > ul.c-attributes-list.c-attributes-list--pros.c-attributes-list--circle.o-block-list.o-block-list--snug')
            for pro in pros:
                item = ReviewItem()
                review_text = pro.css('li::text').get()
                if review_text is not None:
                    item['review_text'] = review_text.strip()
                    item['sentiment'] = 1
                    yield item

            cons = review.css('div.c-post__attributes > ul.c-attributes-list.c-attributes-list--cons.c-attributes-list--circle.o-block-list.o-block-list--snug')
            for con in cons:
                item = ReviewItem()
                review_text = con.css('li::text').get()
                if review_text is not None:
                    item['review_text'] = review_text.strip()
                    item['sentiment'] = 0
                    yield item

            item = ReviewItem()
            review_text = review.css('div > p.c-post__summary::text').get()
            if review_text is not None:
                item['review_text'] = review_text.strip()
                item['sentiment'] = None
                yield item
        
        print(response.url)
        current_page_number = int(response.url.split('=')[-1])
        prefix = response.url.split('=')[0]
        next_page_number = current_page_number + 1
        next_page_url = f"{prefix}={next_page_number}"

        if response.css('div.c-post__content.u-normal-spacing'):
            self.logger.info(f'Following to reviews page {next_page_number}')
            yield response.follow(next_page_url, self.parse_reviews_page)
        else:
            self.logger.info('No more reviews pages to load.')