from urllib.parse import quote
from scrapyscript import Job, Processor
from scrapy.spiders import Spider
from scrapy import Request
import re
import praw
import os

REPLY_TEMPLATE = "[{} - {}](https://www.yankeecandle.com/{})"
READ_COMMENT_IDS = "comment_ids.txt"

comment_ids = []

if os.path.exists(READ_COMMENT_IDS):
    with open(READ_COMMENT_IDS, 'r') as filehandle:
        for line in filehandle:
            comment_ids.append(line[:-1])

class CandleSpider(Spider):
    name = "candles"

    def start_requests(self):
        yield Request(self.url)

    def parse(self, response):
        if len(response.css('.product_details')) == 0:
            return
        price = response.css('.product_details .sales_price .actual_value::text')[0].get()
        link = response.css('.product_details h2 a')[0].attrib['href']
        name = response.css('.product_details h2 a::text')[0].get()
        return {
            'price': price,
            'link': link,
            'name': name
        }

def main():
    reddit = praw.Reddit(
        user_agent="Candlebot (by /u/smartfuse)",
        client_id="<Reddit app client ID here>",
        client_secret="<Reddit app client secret here>",
        username="<Reddit username>",
        password="<Reddit password>",
    )

    subreddit = reddit.subreddit("NYYankees")
    pid = os.fork()
    if pid:
        for comment in subreddit.stream.comments():
            process_entity(comment, comment.body)
    else:
        for submission in subreddit.stream.submissions():
            process_entity(submission, submission.title + " " + submission.selftext)

def process_entity(entity, text):
    if str(entity.id) in comment_ids:
        return
    with open(READ_COMMENT_IDS, 'a') as filehandle:
        filehandle.write(str(entity.id) + "\n")
    comment_ids.append(entity.id)
    pattern = r"🕯️\(([-_ a-zA-Z0-9]+)\)"
    results = re.findall(pattern, text)
    for result in results:
        product_info = get_product_info(result)
        if product_info:
            try:
                entity.reply(REPLY_TEMPLATE.format(product_info['name'], product_info['price'], product_info['link']))
            except:
                print("Rate limited")

def get_product_info(term):
    candleJob = Job(CandleSpider, url = "https://www.yankeecandle.com/search?Ntt=" + quote(term))
    processor = Processor(settings = None)
    results = processor.run([candleJob])
    if len(results) == 0:
        return None
    else:
        return results[0]

main()

