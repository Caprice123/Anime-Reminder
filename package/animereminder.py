from win10toast import ToastNotifier
import sqlite3
from datetime import date
from .GUI_anime import GUI
from .scraping import Scraping
import pickle
import multiprocessing
from .whatsapp import Whatsapp

class AnimeReminder:
    """
    This is main package anime reminder system where scraping, whatsapp and GUI system run
    How does it work?
        1. Check the date based on the pickle data
        2. Scrape gogoanime.sh from scraping.py
        3. Check the animes in database based on the scraping data
        4. Make notification on PC using ToastNotifier and Whatsapp using whatsapp.py by multiprocessing module
        5. Update the GUI

    """

    ###########################################################################################################
    # Configuration for the anime reminder class
    def __init__(self):
        self.apps = Whatsapp()
    ###########################################################################################################


    ###########################################################################################################
    # 1. Check the date based on the pickle data
    # Extract the data from the pickle file
    def unpickling_date(self, pickle_file):
        pickle_out = open(pickle_file, 'rb')
        date = pickle.load(pickle_out)
        pickle_out.close()
        return date

    # Update the data in pickle file
    def pickling_date(self, pickle_file, date):
        pickle_in = open(pickle_file, 'wb')
        pickle.dump(date, pickle_in)
        pickle_in.close()

    # Checking the data in pickle and today's date
    def check_date(self, date):
        date_saved = self.unpickling_date("package/date.pickle")
        if (date_saved != date):
            self.pickling_date("package/date.pickle", date)
            return 1
        return 0
    ###########################################################################################################

    ###########################################################################################################
    # 2. Scrape gogoanime from scraping.py
    def scrape_website(self):
        #print(Scraping("https://gogoanime.sh/").df)
        return Scraping("https://gogoanime.sh/").df
    ###########################################################################################################


    ###########################################################################################################
    # 3. Check the animes in database based on the scraping data
    def update_database(self, database, table, date, change):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table}")
        waiting_list = c.fetchall()

        df = self.scrape_website()
        found_anime = []

        for full_name, anime, episode, last, days, status in waiting_list:
            updated = 0

            search_anime = df['Anime_Title'].str.contains(anime)

            if (search_anime.sum() > 0) and (full_name == anime or (last != date and days > 1)):
                #print(df[search_anime].values)
                full_name, epi = df[search_anime].values[0]

                print(anime)
                c.execute(f"""UPDATE anime SET full_name = '{full_name.title()}',
                                               episodes = '{epi}',
                                               updated_time = '{date}',
                                               days = 0,
                                               status = 1
                                               WHERE anime_title LIKE '{anime}' AND full_name LIKE '%{anime.title()}%'""")
                updated = 1
                found_anime.append(full_name)
            if (change == 1):
                if(last < date and updated == 0):
                    c.execute(f"UPDATE anime SET days = {days + 1} WHERE anime_title LIKE '%{anime}%'")
            elif (days > 31):
                # make anime that hasn't updated on 31 days become history
                c.execute(f"UPDATE anime SET status = 0 WHERE anime_title LIKE '%{anime}%'")
        conn.commit()
        conn.close()
        ###########################################################################################################


        ###########################################################################################################
        # 4. Make notification in PC using ToastNotifier and in Whatsapp using whatsapp.py by multiprocessing module
        if len(found_anime) > 0:
            self.threading(found_anime)

    def threading(self, animes):
        d1 = multiprocessing.Process(target=self.makenotif, args=(animes,))
        d2 = multiprocessing.Process(target=self.apps.send_message, args=("\n".join(animes), "Kelvin",))

        d1.start()
        d2.start()
        d1.join()
        d2.join()

    def makenotif(self, animes, duration=10):
        """
        :param found_anime: all anime that is released that day
        :param duration: duration for windows notifier:
        """
        # print(len(found_anime))
        notif_ = ToastNotifier()
        string = "Released Anime :\n"
        for anime in animes:
            string += anime + "\n"
        notif_.show_toast("Anime Found", string, duration=duration, threaded=True)
    ###########################################################################################################

    ###########################################################################################################
    # 5. Update the GUI
    def run(self):
        database = "anime.db"
        table = "anime"
        while True:
            today_date = date.today().isoformat()
            change = self.check_date(today_date)
            self.update_database(database, table, today_date, change)
            print("Scraping Finished and Saved")

            if GUI().quit == 1:
                break
    ###########################################################################################################


if __name__ == '__main__':
    apps = AnimeReminder()
    apps.run()