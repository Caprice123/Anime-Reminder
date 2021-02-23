from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

class Scraping:
    """
    This is scraping function that is used to extract anime and episodes from gogoanime.sh and extract it to a dataframe
    How does it work?
        1. Connect to gogoanime.sh
        2. Extract all the htmls from the website
        3. Find the anime title and episode by using the class of the p tag in htmls
        4. Put the anime title and episode into dataframe

    """

    ###########################################################################################################
    # Main Scraping Function
    def __init__(self, link):
        names, episodes = self.get_html_website(link)
        self.df = self.make_df(names,episodes)

    ###########################################################################################################


    ###########################################################################################################
    # 1. Connect to gogoanime.sh
    def get_html_website(self, link):
        # connected to the link
        try:
            return self.parsing(requests.get(link))
        except requests.exceptions.ConnectionError:
            return self.get_html_website(link)
    ###########################################################################################################



    def parsing(self,content):
        ###########################################################################################################
        # 2. Extract all htmls from the website
        htmls = BeautifulSoup(content.text,'lxml')
        ###########################################################################################################


        ###########################################################################################################
        # 3. Find the anime title and episode by using the class of the p tag in htmls.
        return htmls.find_all('p', class_ = "name"),htmls.find_all('p', class_ = "episode")
        ###########################################################################################################


    ###########################################################################################################
    # 4. Put the anime title and episode into dataframe
    def make_df(self, names,episodes):
        # make dataframe based on the data from the website
        all_anime = []
        anime_episodes = []

        for name, episode in zip(names, episodes):
            all_anime.append(name.a.text.lower())
            anime_episodes.append(episode.text.replace('Episode', ''))
        lists = list(zip(all_anime, anime_episodes))
        df = pd.DataFrame(lists, columns=["Anime_Title", "Episodes"])
        return df
    ###########################################################################################################






