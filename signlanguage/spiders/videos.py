# -*- coding: utf-8 -*-
import scrapy


class VideosSpider(scrapy.Spider):
    name = 'videos'
    allowed_domains = ['dai.cs.rutgers.edu']
    #start_urls = ['http://http://dai.cs.rutgers.edu/dai/s/signbank?fbclid=IwAR1afEAMDXprb-LCKS8GoXg0asoeNzse9C3ihXeXnfVpQOOYwfXgXW1Wq8/']
    def start_requests(self):
        yield scrapy.Request(url='http://dai.cs.rutgers.edu/dai/s/signbank?fbclid=IwAR1afEAMDXprb-LCKS8GoXg0asoeNzse9C3ihXeXnfVpQOOYwfXgXW1Wq8c',callback=self.parse,headers={
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36'
        })
    def parse(self, response):
        links = response.xpath('//select/option[@style="color: green"]')
        for link in links:
            class_name = link.xpath('.//preceding::option[@class="optionGroup"][1]/text()').get()
            link = link.xpath('.//@ondblclick').get()
            link = link.replace("return popup('", "")
            link = link.replace("', 'dh_end')", "")

            url = "http://dai.cs.rutgers.edu/dai/s/"+link

            #yield{
            #    "class":class_name,
            #    "link":link,
            #    "url" :url
            #}

            yield scrapy.Request(url,callback=self.parse_signs,meta={
                "class":class_name,
                "link":link,
                "url" :url
            },headers={
            'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36'
        })

    def parse_signs(self,response):
        title = response.xpath('//td[@colspan="2"]/center/b/text()').get()
        title=title.replace('Occurrences for Sign Variant:  ',"")
        class_name=response.request.meta["class"]
        videos = response.xpath('.//input[(@id="videoview" or @id = "compositevideoview") and (@value!="Play Utterance Video") and (@value!="Play Composite Video")]/@onclick')
        for video in videos:
            link = video.get()
            link = link.replace("return popupvideo('", "")
            link = link.replace("')", "")
            url = "http://dai.cs.rutgers.edu/dai/s/" + link
            #yield {
            #    "titre":title,
            #    "class_name":class_name,
            #    "url":url
            #}

            yield scrapy.Request(url, callback=self.parse_videos, meta={
                "title":title,
                "class_name":class_name
            }, headers={
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36'
            })
    def parse_videos(self,response):
        video_url = response.xpath('.//video/source/@src').get()
        if not(video_url):
            video_url = response.xpath('.//embed/@src').get()
        title = response.request.meta["title"]
        class_name = response.request.meta["class_name"]

        yield {
            "video_url" : video_url,
            "class" : class_name,
            "sous_class":title
        }
