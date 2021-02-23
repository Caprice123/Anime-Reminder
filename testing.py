'''import pywhatkit
import datetime

now = datetime.datetime.now()

pywhatkit.sendwhatmsg("+628971740268","This is a message",now.hour,now.minute+1)
print("send succesfully")'''
anime = ["owari no seraph", "mushoku"]
for a in anime:
    if ("owari" in a):
        print('break')
        break
print("owari" in anime)