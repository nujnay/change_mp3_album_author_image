from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
# address = "F:\mygithub\change_mp3\data/first.mp3"
# address = "F:\mygithub\change_mp3\data/pick_bila_waktu_telah_berakhir.mp3"
# address = "F:\mygithub\change_mp3\data/pick_taubat.mp3"
address = "F:\mygithub\change_mp3\data/sholawat_nabi_maulidu_ahmad.mp3"

audio = MP3(address, ID3=ID3)

try:
    audio.add_tags()
except error:
    pass

audio.tags.add(
    APIC(
        encoding=3,  # 3 is for utf-8
        mime='image/jpg',  # image/jpeg or image/png
        type=3,  # 3 is for the cover image
        desc=u'Cover',
        data=open('F:\mygithub\change_mp3\icon\icon_1.jpg', "rb").read()
    )
)

audio.save()
audio = EasyID3(address)
audio['artist'] = "artist"
audio['title'] = "title"
audio['tracknumber'] = "tracknumber"
audio['album'] = "album"
audio.save()
