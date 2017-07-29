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
        fileObj = open('/home/movie2.txt', 'a')
        for (n,u) in [(name,url)]:
            movie_name = str(n)
            movie_url = str(u)
            #print('movie info:', movie_str)
            fileObj.write(movie_name+movie_url)
        fileObj.write('\n')
        fileObj.close()

class movie_spider2(scrapy.Spider):

    name = "movie_spider2"

    start_urls = ['http://blu-raydisc.tv/film/720p-1080p']

    allow_urls = ['blu-raydisc.tv']

    #def __init__(self, name, url, score, link):
    #    self.name = name
    #    self.url = url
    #    self.link = link

    def parse(self,response):
        for i in response.xpath("//h2[@class='pos-title']/a/@href").extract():
            yield scrapy.Request("http://blu-raydisc.tv"+i,callback=self.parse_movie)

        pages_link = response.xpath("//div[@class='pagination-bg']/a/@href").extract()
        full_page_link = "http://blu-raydisc.tv"+pages_link[-2]
        if full_page_link not in next_page_link:
            yield scrapy.Request(full_page_link,callback=self.parse)
        else:
            print 'I finished but I can continue'

    def parse_movie(self,response):
        item = MovieSpiderItem()
        item['movie_name'] = response.xpath("//div[@id='yoo-zoo']/div/div/h1/text()").extract()
        #item['movie_name'] = response.selector.xpath("//tile/text()").extract()
        item['movie_url'] = response.selector.xpath("//div/div/div/div/div/div/a/@href").extract()
        yield item

        for name in item['movie_name']:
            for url in item['movie_url']:
                saveInfo(name,url)
            #show(url)
            #print '0'

    # def show(url):
    #     print 'url'



    
