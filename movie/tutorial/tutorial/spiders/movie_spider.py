#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys, os, urllib
reload(sys)

sys.setdefaultencoding('utf-8')

#import requests

import scrapy

from tutorial.items import MovieSpiderItem

# site = 'http://www.yinfans.com'
lineNo = 1

next_page_link = []


def saveInfo(name,url):
        fileObj = open('/home/movie.txt', 'a')
        for (n,u) in [(name,url)]:
            movie_name = str(n)          
            movie_url = str(u)
            #print('movie info:', movie_str)
            fileObj.write(movie_name+movie_url)
        fileObj.write('\n')      
        fileObj.close()


class movie_spider(scrapy.Spider):

    name = "movie_spider"

    start_urls = ['http://www.yinfans.com']

    allow_urls = ['yinfans.com']

    #def __init__(self, name, url, score, link):
    #    self.name = name
    #    self.url = url
    #    self.link = link

    def parse(self,response):
        for i in response.xpath("//div[@class='article']/h2/a/@href").extract():
            yield scrapy.Request(i,callback=self.parse_movie)

        pages_link = response.xpath("//div[@class='pagination']/a/@href").extract()
        full_page_link = pages_link[-2]
        if full_page_link not in next_page_link:
            yield scrapy.Request(full_page_link,callback=self.parse)
        else:
            print 'I finished but I can continue'

    def parse_movie(self,response):
        item = MovieSpiderItem()
        item['movie_name'] = response.xpath("//div[@id='content']/div/h1/text()").extract()
        #item['movie_name'] = response.selector.xpath("//tile/text()").extract()
        item['movie_url'] = response.selector.xpath("//div/p/strong/a/@href").extract()
        yield item

        #for (name,url) in [(item['movie_name'],item['movie_url'])]:
        for name in item['movie_name']:
            #print name
            for url in item['movie_url']:
                saveInfo(name,url)
            #show(url)
            #print '0'

    # def show(url):
    #     print 'url'



    
