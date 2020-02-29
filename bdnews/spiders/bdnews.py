import scrapy
import os
import errno
import json
import unicodedata
from urllib.parse import urlparse
import hashlib
import logging

logging.basicConfig(filename='scraphistory.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('logging important moments!')
monthDict = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06", "Jul":"07", "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}


class BdSpider(scrapy.Spider):
	name = 'bdnews'

	# scrapping bdnews website
	start_urls = ['https://bangla.bdnews24.com/']



	def parse(self, response):
		# get all the news link
		newsLinks = response.css('div.news-bn a::attr(href)').getall()
		for link in newsLinks:
			if link is not None:
				yield response.follow(link, callback=self.parseNews)
			


	def parseNews(self, response):
		# for individual news posts
		
		# get the date 
		date = response.css('p.dateline span::text').getall()[1]
		d = date[1:3]
		m = monthDict[date[4:7]]
		y = date[8:12]
		format_date = d+'-'+m+'-'+y
		fullDate = date[:21]


		# get title 
		title = response.css('h1::text').get()

		# get the body of the article
		body = response.css('div.custombody p::text').getall()

		body_text = ""
		for b in body:
			body_text+= b

		# dictionary to save as json
		entry = {
			"Title" : title,
			"Date" : fullDate,
			"Content" : body_text
		}


		# parsing the uri and getting the domain
		parsed_uri = urlparse(response.url)
		domain_name = '{uri.netloc}'.format(uri=parsed_uri).strip()
		uri = '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri).strip()
		# hashing the uri
		hs = hashlib.md5(uri.encode()).hexdigest().upper()
		# setting up directory and filename
		file = domain_name + '/' + format_date + '/' + hs + '.json'
		if not os.path.exists(os.path.dirname(file)):
			try:
				os.makedirs(os.path.dirname(file))
				logger.info('made directory: '+file)
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					logger.error('cannot make directory!')
					raise

		
		with open(file, 'w+', encoding='utf-8') as fp:    
			json.dump(entry, fp, ensure_ascii=False)
			logger.info('json dumped for: ' + title)

