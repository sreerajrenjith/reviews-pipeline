#scrapy runspider amazon_review.py -o reviews.csv
from selenium import webdriver
import scrapy
#from final_amazon import product_name
chromedriver_location="/home/sreeraj/Desktop/voice_assistant/chromedriver"
urllist=[]
driver = webdriver.Chrome(chromedriver_location)
driver.get("https://www.amazon.in/")
product_name="IE Irodov"
prod=product_name
searchbar='//*[@id="twotabsearchtextbox"]'
search='//*[@id="nav-search-submit-button"]'
driver.find_element_by_xpath(searchbar).send_keys(prod)
driver.find_element_by_xpath(search).click()

for i in range (2,7):
 try:
    item=f'//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[{i}]/div/div/div/div/div/div[2]/div/div/div[1]/h2/a'
    url=driver.find_element_by_xpath(item).get_attribute('href')
    urllist.append(url)
 except: continue

review_urls=[]
for url in urllist:
    review_url = url.partition("dp/")[0]
    prodid = url.partition("dp/")[2]
    prodid = prodid.partition("/")[0]
    review_url = review_url + "product-reviews/" + prodid + "/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    review_urls.append(review_url)

class AmazonReviewSpider(scrapy.Spider):
    name = 'amazon_review'
    allowed_domains = ['amazon.in']
    start_urls=review_urls
    #print(start_urls,'\n\n\n\n\n\n\n\n')
    # Creating list of urls to be scraped by appending page number a the end of base url
    # for i in range(1,121):
    #     start_urls.append(myBaseUrl+str(i))


    # Defining a Scrapy parser
    def parse(self, response):
            data = response.css('#cm_cr-review_list')

            # Collecting product star ratings
            star_rating = data.css('.review-rating')

            # Collecting user reviews
            comments = data.css('.review-text')
            count = 0

            # Combining the results
            for review in star_rating:
                yield{'stars': ''.join(review.xpath('.//text()').extract()),
                      'comment': ''.join(comments[count].xpath(".//text()").extract())
                     }
                count=count+1

