import requests
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser


def scrapping():
	import requests
	from bs4 import BeautifulSoup
	import pandas as pd
	from splinter import Browser

	## (1) Scrape Latest Mars News 
	url = "https://mars.nasa.gov/news/"
	browser = Browser("chrome")
	browser.visit(url)
	html = browser.html
	soup = BeautifulSoup(html, "html.parser")
	news = soup.find("div", class_="list_text")
	title = news.find("div", class_="content_title")
	para = soup.find("div", class_="article_teaser_body")
	news.text
	news_title =title.text
	news_p = para.text

	## (2)Scrape Mars featured space image
	url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	response = requests.get (url)
	soup = BeautifulSoup(response.text, 'html.parser')

	# get a list of all images under tag 'li' and class 'slide'
	list_items = soup.find_all("li", class_="slide")
	#list_items[0]
	#get first element of the list, get tag 'a' and get attribute 'data-fancybox-href' which contains the full size image
	partial_url = list_items[0].a['data-fancybox-href']
	#print(partial_url)
	featured_image_url = "https://jpl.nasa.gov" + partial_url
	#print(f"full image url is {featured_image_url}")

	## (3) Colect Mars weather info 
	url = 'https://twitter.com/marswxreport?lang=en'
	response = requests.get (url)
	soup = BeautifulSoup(response.text, 'html.parser')

	result = soup.find('p', class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
	# check multiple type of outputs from result
	# result
	# result.text
	# result.contents
	# result.contents[0]
	#replace newline character \n with space
	result.contents[0].replace("\n", " ")
	#save above 
	mars_weather = result.contents[0].replace("\n", " ")

	## (4) Scrape table from space-facts directly to pandas
	url = "https://space-facts.com/mars/"

	table =pd.read_html(url)
	# table
	# table[0]
	df_table = table[0]
	df_table.columns = ['Mars_Particular', 'Values']
	df_table.set_index('Mars_Particular', inplace = True)
	# df_table
	html_table = df_table.to_html(header = False)
	# html_table

	# (5) Scrape Mars hemisphere images
	# url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	# response = requests.get(url).text
	# # get a list of items available
	# soup = BeautifulSoup(response, 'html.parser')
	# list_images = soup.find_all('div', class_="item")
	# # print(list_images[0].prettify())


	browser = Browser("chrome")

	url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(url)

	img_list=[]
	for i in range (4):

	    images = browser.find_by_tag('h3')
	    images[i].click()
	    html = browser.html
	    soup = BeautifulSoup(html, 'html.parser')
	    partial = soup.find("img", class_="wide-image")["src"]
	    img_title = soup.find("h2",class_="title").text.split('Enhanced')[0]
	    img_url = 'https://astrogeology.usgs.gov'+ partial
	    dict={"img_title":img_title,"img_url":img_url}
	    img_list.append(dict)
	    browser.back()

	# print(img_list)
	scrape = {'news_title':news_title, 'news_p':news_p, 'featured_image_url':featured_image_url, 'mars_weather': mars_weather, 'html_table': html_table, 'img_list':img_list}

	print("we have img_list(list of dict with hemis name and images")
	print("we have 'html_table' - html file with mars stats")
	print ("we have 'mars_weather' a string containing latest weather tweet")
	print ("we have 'featured_image_url' - string containing featured image url")
	print("we have 'news_title' and 'news_p' strings of latest news from Nasa mars page")
	print(scrape)
	return(scrape)

# import python mongo module
from pymongo import MongoClient
conn = "mongodb://localhost:27017"
client = MongoClient(conn)
db = client.mars_db
coll = db.mars_coll

#################################################
# Flask Setup
from flask import Flask, jsonify, render_template
app = Flask(__name__)
#################################################

# Flask Routes
#################################################

@app.route("/scrapper")
def scrapper():
	
	db.coll.remove()
	data = scrapping()
	print('scrapping done..')
	result = coll.insert_one(data)

	return render_template("index.html", my_scrape = data) 
#################################################

@app.route("/")
def index():

    my_search = coll.find_one()

    return render_template("index.html", my_scrape=my_search)


if __name__ == "__main__":
    app.run(debug=True)