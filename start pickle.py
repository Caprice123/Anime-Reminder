import pickle

from datetime import date

pickle_in = open("static/date.pickle", 'wb')
pickle.dump('2020-02-04', pickle_in)
pickle_in.close()