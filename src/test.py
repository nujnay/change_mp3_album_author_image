from src.change_mp3 import MP3



MP3 = MP3("F:\mygithub\change_mp3\data/first.mp3")
print(MP3.getInfo())
data = {u'Artist': "1",
        u'Title': "2",
        u'Album': "3"
        }
MP3.addImage("F:\mygithub\change_mp3\icon\icon_1.jpg", data)
