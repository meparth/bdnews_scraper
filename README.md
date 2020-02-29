# bdnews_scraper
This is a simple scraper made with the python module scrapy to scrape bengali news articles from the website *https://bangla.bdnews24.com/*

## Use
To use this, the files need to be downloaded into a **python** and **scrapy** installed machine. The opening the terminal, the following should be entered:

> scrapy crawl bdnews

That is all needed to get the news items downloaded into the machine. 

## Followed Strategy
The scraped json file names are set as the md5 hashed value of the url of that news item. The directory for the items are set as: *bangla.bdnews24.com/date/*




