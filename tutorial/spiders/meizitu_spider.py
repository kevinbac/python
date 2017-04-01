#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys, os, urllib
reload(sys)

sys.setdefaultencoding('utf-8')

import scrapy

from tutorial.items import MeizituSpiderItem

next_page_link = []

def download(url):
	file_name = url[-17:]
	path = '/home/xx/Pictures/meizi'
	name = path+file_name.replace('/','_')
	if not os.path.exists(name):
		data = urllib.urlretrieve(url,name)
	else:
		print 'this pic exists'
		pass


class meizitu_spider(scrapy.Spider):
	"""docstring for meizitu_spider"scrapy.Spiderf __init__(self, arg):"""
	
	name = "meizitu_spider"

	start_urls = ['http://www.mzitu.com/']

	allow_urls = ['mzitu.com']

	def parse(self,response):
		for i in response.xpath("//ul[@id='pins']/li/a/@href").extract():
			yield scrapy.Request(i,callback=self.parse_picture)

		pages_link = response.xpath("//div[@class='nav-links']/a/@href").extract()
		full_page_link = pages_link[-1]
		if full_page_link not in next_page_link:
			yield scrapy.Request(full_page_link,callback=self.parse)
		else:
			print 'I finished but I can continue'

	def parse_picture(self,response):
		item = MeizituSpiderItem()
		item['pic_name'] = response.selector.xpath("//tile/text()").extract()
		item['pic_url'] = response.selector.xpath("//div/p/a/img/@src").extract()
		yield item

		for url in item['pic_url']:
			download(url)






