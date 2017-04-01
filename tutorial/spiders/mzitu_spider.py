#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys, os, urllib
reload(sys)

sys.setdefaultencoding('utf-8')

import scrapy

from tutorial.items import MeizituSpiderItem

next_page_link = []

def download(url):
	file_name = url[-20:]
	path = '/home/mzitutu'
	name = path+file_name.replace('/','_')
	if not os.path.exists(name):
		data = urllib.urlretrieve(url,name)
	else:
		print 'this pic exists'
		pass


class meizitu_spider(scrapy.Spider):
	"""docstring for meizitu_spider"scrapy.Spiderf __init__(self, arg):"""
	
	name = "mzitu_spider"

	start_urls = ['http://www.meizitu.com/a/list_1_1.html']

	allow_urls = ['meizitu.com']

	def parse(self,response):
		for i in response.xpath("//ul[@class='wp-list clearfix']/li/div/div/a/@href").extract():
			yield scrapy.Request(i,callback=self.parse_picture)

		pages_link = response.xpath("//div[@id='wp_page_numbers']/ul/li/a/@href").extract()
		full_page_link = "http://www.meizitu.com/a/"+pages_link[-2]
		if full_page_link not in next_page_link:
			yield scrapy.Request(full_page_link,callback=self.parse)
		else:
			print 'I finished but I can continue'

	def parse_picture(self,response):
		item = MeizituSpiderItem()
		item['pic_name'] = response.selector.xpath("//tile/text()").extract()
		item['pic_url'] = response.selector.xpath("//div/p/img/@src").extract()
		yield item

		for url in item['pic_url']:
			download(url)






