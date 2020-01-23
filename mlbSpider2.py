#scrapy runspider mlbSpider2.py -o rockies.json
import logging
logging.getLogger('scrapy').setLevel(logging.WARNING)

from lxml import html

import scrapy

class mlbSpider2(scrapy.Spider):
	name = 'Boxscore'
	start_urls = ['https://www.baseball-reference.com/teams/tgl.cgi?team=WSN&t=b&year=2009']
	
	
	def parse(self, response):
		year = ''.join(response.css('div#meta>div>h1>span')[0].css('::text').extract())
		g = {year : [] }
		x = ""
		for d in response.css('div#meta>div>p'):
			if 'Ballpark:' == ''.join(d.css('strong::text').extract()) or 'Ballparks:' == ''.join(d.css('strong::text').extract()):
				x = ''.join(d.css('::text').extract()).strip()
		temp = x.split(' ', 1)
		#print(temp[1])
		for e in response.css('div#div_team_batting_gamelogs>table>tbody>tr'):
			gm = "GM" + ''.join(e.css('td[data-stat=team_game_num]::text').extract()).strip()
			BA = ''.join(e.css('td[data-stat=batting_avg]::text').extract()).strip()
			opp = ''.join(e.css('td[data-stat=opp_ID]>a::text').extract()).strip()
			if "@" != ''.join(e.css('td[data-stat=team_homeORaway]::text').extract()).strip():
				field = temp[1]
			else:
				field = ""
			g[year].append({
				'game': gm,
				'BA' : BA,
				'opp': opp,
				'field': field})
		yield g
		
		next_year = response.xpath('.//div[@class="prevnext"]/a[@class="button2 next"]/@href').extract()
		if next_year:
			next_href = next_year[0]
			url = 'https://www.baseball-reference.com' + next_href
			yield scrapy.Request(url, self.parse)