import scrapy
from scrapy.crawler import CrawlerProcess
import json

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ['http://books.toscrape.com/']

    # Inicializamos uma lista para acumular os dados de todos os livros de todas as páginas
    books_list = []

    def parse(self, response):

        for book in response.css('article.product_pod'):
            
            #CLASS DO CSS (ex: "star-rating ****")
            estrelas = book.css('p.star-rating::attr(class)').get()
            if estrelas and ('Four' in estrelas or 'Five' in estrelas):

                book_data = {
                    'title': book.css('h3 a::attr(title)').get(),
                    'price': book.css('p.price_color::text').get(),
                    'availability': book.css('p.instock.availability::text').re_first(r'(\S+\s\S+)'),
                    
                    #SALVAR NO JSON
                    'rating': estrelas.replace('star-rating ', '') 
                }
                self.books_list.append(book_data)

       
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            
            yield response.follow(next_page, self.parse)
        else:
            
            with open('books.json', 'w', encoding='utf-8') as f:
                json.dump(self.books_list, f, ensure_ascii=False, indent=4)

# Executa o spider
# process = CrawlerProcess()
# process.crawl(BooksSpider)
# process.start()