from tkinter import *
from tkinter import messagebox

import sqlite3

class GUI:
    """
    This is GUI main program in anime reminder system

    """

    ###########################################################################################################
    # Main Configuration
    def __init__(self):
        # initial setting root
        self.root = Tk()
        self.root.geometry("635x410+890+385")
        self.root.title("Waiting List Anime")

        # initial images collection
        photo = PhotoImage(file ='images/waiting list.png')
        self.watched_button = PhotoImage(file='images/watched2.png').subsample(4, 4)
        self.watched = PhotoImage(file ='images/done.png')
        self.add_icon = PhotoImage(file='images/add.png').subsample(3, 3)
        self.photo_delete = PhotoImage(file="images/delete.png").subsample(5, 5)
        self.back_icon = PhotoImage(file ='images/back.png').subsample(13, 13)
        self.save_icon = PhotoImage(file ='images/save.png')
        self.new_added_anime_icon = PhotoImage(file='images/added new anime.png')

        # initial font
        self.font = ("Jokerman", 11)
        self.font2 = ("Bookman Old Style", 10)

        # initial other variable
        self.quit = 0
        self.cnt = 0
        self.database = 'anime.db'

        # icon for windows
        self.root.iconphoto(False, photo)

        self.main()

        # asking for confirmation of quit
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    ###########################################################################################################


    ###########################################################################################################
    # Confirmation of closing GUI
    def on_closing(self):
        # asking confirmation and destroy windows
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.quit = 1
    ###########################################################################################################


    ###########################################################################################################
    # Scrollbar configuration for main table anime
    def configure_scroll_for_canvas(self, event):
        # configuration for scrollbar in main table
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox('all'))
    ###########################################################################################################


    ###########################################################################################################
    # Adding new anime to the database
    def save_new_anime(self,event = None):
        # checking whether empty input and connect to database
        if (self.added_anime_title.get() != ''):
            conn = sqlite3.connect(self.database)
            c = conn.cursor()
            c.execute("SELECT * FROM anime")
            lists_anime = c.fetchall()

            # checking database empty
            if len(lists_anime) > 0:

                # checking for duplicate title
                titles = [i[1].lower() for i in lists_anime]
                statuses = [i[-1] for i in lists_anime]
                lists_anime = [i[0].lower() for i in lists_anime]

                found = 0
                for anime, stats,title in zip(lists_anime, statuses, titles):
                    if (self.added_anime_title.get() in anime and self.added_anime_title.get() == title):
                        if(stats == 1):
                            found = 1
                            break
                if (found == 0):
                    # saving to database if no duplicate title or duplicate title with status not on going
                    c.execute("INSERT INTO anime VALUES (?,?,?,?,?,?)",
                              (self.added_anime_title.get(),self.added_anime_title.get(),'0', '-',0, 1))
                    conn.commit()
                    conn.close()
                    self.new_window.destroy()
                    self.main()

                else:
                    # show error and asking for re input another anime title
                    self.new_window.destroy()
                    messagebox.showwarning("Duplicate Anime", "You have already input that anime title before, please check in the history. Try re-input anime title")
                    self.add_anime()

            else:
                # no anime in database and save the first anime title
                c.execute("INSERT INTO anime VALUES (?,?,?,?,?,?)",
                          (self.added_anime_title.get(), self.added_anime_title.get(), '0', '-', 0, 1))
                conn.commit()
                conn.close()
                self.new_window.destroy()
                self.see_waiting_list()
    ###########################################################################################################


    ###########################################################################################################
    # Adding anime title that wants to be in waiting list GUI
    def add_anime(self):
        # making new windows for adding anime
        self.new_window = Toplevel(bg = "#E5D7F7")
        self.new_window.geometry("635x100+890+300")
        self.new_window.title("Adding New Anime")
        self.new_window.iconphoto(False,self.new_added_anime_icon)

        # command for adding new anime title
        blank = Label(self.new_window, text = " ", width = 10, bg = "#E5D7F7")
        blank.grid(row = 0, column = 0)
        commands = Label(self.new_window, text = "New Anime Title : ", font = self.font, bg = "#E5D7F7")
        commands.grid (row = 0, column = 1)

        # entry box for new anime title
        self.added_anime_title = Entry(self.new_window, width = 50, font = self.font2)
        self.added_anime_title.focus_set()
        self.added_anime_title.bind('<Return>', self.save_new_anime)
        self.added_anime_title.grid(row = 0, column = 2, columnspan = 3)

        # saving button
        button = Button(self.new_window, image = self.save_icon,text = "Save",compound = LEFT, bg = "#E5D7F7",
                        relief = FLAT, font = self.font,command = self.save_new_anime)
        button.grid (row = 1, column = 2)
    ###########################################################################################################


    ###########################################################################################################
    # Scrollbar configuration of watched list table
    def configure_scroll_for_canvas_watched(self, event):
        # scrollbar configuration for watched anime
        self.canvas_table.configure(scrollregion=self.canvas_table.bbox('all'))
    ###########################################################################################################

    ###########################################################################################################
    # Extracting all anime title in database
    def display_watched_anime(self):
        # connect to database and get all data from database
        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        c.execute("SELECT * FROM anime")

        animes = c.fetchall()
        rows = 0

        # show content of all anime in database
        # print(len(all_waiting_list))
        for full_name, anime_title, episod, update,days,  status in sorted(animes, key = lambda x : x [3], reverse = True):
            #print(full_name)
            if (rows + 1) % 2 == 0:
                warna = "#75D4DF"
            else:
                warna = "#5BB3BD"
            frame_no = Frame(self.frame_table, width = 50, highlightbackground = "#2582A8", highlightthickness = 2)
            frame_no.grid(row = rows, column = 0)
            no = Label(frame_no, text=str(rows + 1) + ".", width=3, font=self.font2, bg=warna)
            no.pack()

            frame_anime = Frame(self.frame_table, width = 50, highlightbackground = "#2582A8", highlightthickness = 2)
            frame_anime.grid(row = rows, column = 1)
            anime_title = Label(frame_anime, text=full_name, width=51, font=self.font2, bg=warna)
            anime_title.pack()
            rows += 1
    ###########################################################################################################


    ###########################################################################################################
    # Configuration of new window that show the watched anime list
    def see_watched_anime(self):
        # making new windows for watched anime
        new_window = Toplevel()
        new_window.geometry("475x190+975+200")
        new_window.title("Watched Anime")
        new_window.iconphoto(False, self.watched)

        frame_title = Frame(new_window, width = 400, height = 25)
        frame_title.place(x = 0, y = 0)

        # title bar for watched anime windows
        frame_no = Frame(frame_title, width = 50, highlightbackground = "#2582A8", highlightthickness = 2)
        frame_no.grid(row = 0, column = 0)
        watch_no = Label (frame_no, text = "No.", width = 3, font = self.font, bg = "#4BDEC0")
        watch_no.pack()

        frame_anime = Frame(frame_title, width = 50, highlightbackground = "#2582A8", highlightthickness = 2)
        frame_anime.grid(row = 0, column = 1)
        watch_anime = Label (frame_anime, text = "Watched Anime", width = 49, font = self.font, bg = "#4BDEC0")
        watch_anime.pack()

        frame_table = Frame(new_window, width = 475, height = 150, bg = "#9CE5A3")
        frame_table.place (x = 0, y = 33)

        # configuration for watched anime title
        self.canvas_table = Canvas(frame_table)
        self.canvas_table.place (relx = 0, rely = 0, relheight =  1, relwidth = 1)

        self.frame_table = Frame(self.canvas_table, bg = "#D7D6D6")
        self.frame_table.bind('<Configure>', self.configure_scroll_for_canvas_watched)
        self.canvas_table.create_window(0, 0, window=self.frame_table)

        scrolly = Scrollbar(frame_table, command=self.canvas_table.yview,takefocus = 0)
        scrolly.place(relx=1, rely=0, relheight=1, anchor='ne')

        self.canvas_table.configure(yscrollcommand=scrolly.set)

        self.display_watched_anime()
    ###########################################################################################################


    ###########################################################################################################
    # Extracting all data in database and show if the anime is still updating within 31 days
    def see_waiting_list(self):
        # connect to database and get alk information from database
        self.cnt = 0
        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        c.execute("SELECT * FROM anime")

        all_waiting_list = c.fetchall()
        rows = 0
        #print(len(all_waiting_list))
        # display all anime title and information
        for full_name, anime_title, episod, update,days,  status in sorted(all_waiting_list, key = lambda x : x [3], reverse = True):
            if (rows + 1) % 2 == 0:
                warna = "#75D4DF"
            else:
                warna = "#5BB3BD"
            if (status == 1 and days < 101):
                frame_no = Frame(self.table, width = 5,highlightbackground = "#2582A8", highlightthickness = 2)
                frame_no.grid(row = rows, column = 0)
                no = Label(frame_no, text = str(rows + 1) + ".", width = 5, font = self.font2, bg = warna)
                no.pack()

                frame_title = Frame(self.table, width = 5,highlightbackground = "#2582A8", highlightthickness = 2)
                frame_title.grid(row = rows, column = 1)
                anime_title = Label (frame_title, text = full_name, width = 49,font = self.font2, bg = warna)
                anime_title.pack()

                frame_episode = Frame(self.table, width=5, highlightbackground="#2582A8", highlightthickness=2)
                frame_episode.grid(row=rows, column=2)
                if (episod == 0):
                    text = "-"
                else :
                    text = str(episod)
                episode = Label (frame_episode, text = text, width = 8, font = self.font2, bg = warna)
                episode.grid(row = 0, column = 0)


                frame_update = Frame(self.table, width=5, highlightbackground="#2582A8", highlightthickness=2)
                frame_update.grid(row=rows, column=3)
                last_update = Label(frame_update, text = update, width = 13, font = self.font2, bg = warna)
                last_update.pack()
                rows += 1
        self.buttons()
    ###########################################################################################################


    ###########################################################################################################
    # Configuration for waiting list
    def main_table_canvas(self):
        # configuration for main table anime
        self.main_frame = Frame(self.frame, width=635, height=325, bg="#3B9B20")
        self.main_frame.place(x=0, y=32)

        self.main_canvas = Canvas(self.main_frame, bg = "#E5D7F7")
        self.main_canvas.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.table = Frame(self.main_canvas, bg="#D7D6D6")
        self.table.bind('<Configure>', self.configure_scroll_for_canvas)
        self.main_canvas.create_window(0, 0, window=self.table)

        self.scrolly = Scrollbar(self.main_frame, command=self.main_canvas.yview)
        self.scrolly.place(relx=1, rely=0, relheight=1, anchor='ne')

        self.main_canvas.configure(yscrollcommand=self.scrolly.set)
    ###########################################################################################################


    ###########################################################################################################
    # Deleting the anime in database based on the button in waiting list
    def delete(self, index):
        # delete anime based on number in main table
        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        c.execute("SELECT * FROM anime")

        all_waiting_list = c.fetchall()
        all_waiting_list = sorted(all_waiting_list, key=lambda x: x[3],reverse=True)
        #print(all_waiting_list[index])

        c.execute(f"DELETE from anime WHERE full_name LIKE '{all_waiting_list[index][0]}'")
        conn.commit()
        conn.close()

        self.main()
    ###########################################################################################################


    ###########################################################################################################
    # Making all number in waiting list anime to button
    def prepare_delete(self):
        # make button for deletion
        self.cnt += 1
        if (self.cnt % 2 == 1):
            conn = sqlite3.connect(self.database)
            c = conn.cursor()

            c.execute("SELECT * FROM anime")

            all_waiting_list = c.fetchall()
            conn.close()
            rows = 0
            # print(len(all_waiting_list))
            for full_name, anime_title, episod, update, days, status in sorted(all_waiting_list, key=lambda x: x[3],
                                                                               reverse=True):
                if (rows + 1) % 2 == 0:
                    warna = "#75D4DF"
                else:
                    warna = "#5BB3BD"
                if (status == 1 and days < 101):
                    no = Button(self.table, text=str(rows + 1) + ".", width=5, font=("Bookman Old Style", 8),
                                                     bg=warna, command = lambda rows=rows : self.delete(rows))
                    no.grid(row = rows, column = 0)


                    rows += 1
            self.buttons()
        else:
            self.see_waiting_list()
    ###########################################################################################################

    ###########################################################################################################
    # Configuration for all button
    def buttons(self):
        # button primary see watched anime, delete and add button
        self.bottom_frame = Frame(self.frame, width=635, height=53, bg="#E5D7F7")
        self.bottom_frame.place(x=0, y=355)


        add_button = Button(self.bottom_frame, text = "Add", font = self.font, relief=FLAT, image=self.add_icon, bg="#E5D7F7",
                            compound = LEFT, command=self.add_anime)
        add_button.place(x=500, y=0)

        if (self.cnt % 2 == 0):
            delete_button = Button(self.bottom_frame, text = "Delete",font = self.font, relief = FLAT, image = self.photo_delete, bg = "#E5D7F7",
                                   compound = LEFT, command = self.prepare_delete)
            delete_button.place(x = 275, y = 0)
        else:
            back_button = Button(self.bottom_frame, text = "Back",font = self.font, relief = FLAT, image = self.back_icon, bg = "#E5D7F7",
                                   compound = LEFT, command = self.see_waiting_list)
            back_button.place(x = 275, y = 0)

        see_watched = Button(self.bottom_frame, relief=FLAT, image=self.watched_button, text = "See Watched\nAnime",
                             font = self.font, bg="#E5D7F7", compound = LEFT,command=self.see_watched_anime)
        see_watched.place(x=0, y=0)
    ###########################################################################################################


    ###########################################################################################################
    # Configuration for title bar of waiting list anime
    def title_bar(self):
        # configuration for title bar of main windows
        self.title_frame = Frame(self.frame, width=620, height=30)
        self.title_frame.place(x=0, y=0)

        frame_number = Frame(self.title_frame, width = 50,height = 30,highlightbackground = "#2582A8", highlightthickness = 2)
        frame_number.grid(row = 0, column = 0)
        number = Label(frame_number, text="No.", width=4, font=self.font, bg = "#4BDEC0")
        number.pack()

        frame_title = Frame(self.title_frame, width = 50,height = 30,highlightbackground = "#2582A8", highlightthickness = 2)
        frame_title.grid(row = 0, column = 1)
        anime_title = Label(frame_title, text="Anime Title", width=43, font=self.font, bg = "#4BDEC0")
        anime_title.pack()

        frame_episode = Frame(self.title_frame, width=50, height=30, highlightbackground="#2582A8", highlightthickness=2)
        frame_episode.grid(row=0, column=2)
        last_episode = Label(frame_episode, text="Episode", width=7, font = self.font, bg = "#4BDEC0")
        last_episode.pack()

        frame_update = Frame(self.title_frame, width=50, height=30, highlightbackground="#2582A8", highlightthickness=2)
        frame_update.grid(row=0, column=3)
        update = Label(frame_update, text = "Updated", width = 14, font = self.font, bg = "#4BDEC0")
        update.pack()
    ###########################################################################################################


    ###########################################################################################################
    # Main Function
    def main(self):

        self.frame = Frame(self.root, width = 630, height = 410, bg = "#3B9B20")
        self.frame.place(x = 0, y = 0)
        self.title_bar()

        self.main_table_canvas()

        self.see_waiting_list()
        self.root.minsize()

        self.root.after(1000 * 60 * 15, lambda: self.root.destroy())
    ###########################################################################################################


if __name__ == '__main__':
    GUI()