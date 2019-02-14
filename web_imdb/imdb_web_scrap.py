import pandas as pd
import requests
from bs4 import BeautifulSoup
import os


def scrap_IMDB_page(url):
	""" Web scapping for Movies in IMDB"""
	page = requests.get(url)
	soup = BeautifulSoup(page.content, "html.parser")
	name_tags = soup.select(".lister-item .lister-item-header")
	movie_names = [i.a.get_text() for i in name_tags]
	links = [i.get('href') for i in soup.select(".lister-item-header > a:nth-of-type(1)")]
	links = ["https://www.imdb.com" + s for s in links]
	img_links = []
	for i in soup.find_all('img'):
			img_links.append(i.get('loadlate',''))

	img_links.remove('')
	img_links.remove('')

	imdb_df = pd.DataFrame({
			"names": movie_names,
			"links": links,
			"image_links": img_links
		})
	if os.path.isfile('./imdb1.csv'):
		os.remove("imdb1.csv")
	if os.path.isfile('./imdb1.json'):
    		os.remove("imdb1.json")		
	imdb_df.to_csv('imdb1.csv')
	imdb_df.to_json('imdb1.json')



