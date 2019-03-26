import sys, signal
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


from bs4 import BeautifulSoup
import requests
from datetime import datetime, time
import time as now_time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

url = 'https://www.antenne.de/programm/aktionen/vw-bullis-geschenkt/los-gehts'
url_live_stream = 'https://www.webradio.de/antenne-bayern/live'

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

browser = webdriver.Chrome(executable_path='./chromedriver',
                           chrome_options=option)

first_song_found = False
second_song_found = False

current_song = ''
song_history = ['',]


# notify first song
def found_first_song():
    """
    Trigger ifttt if first song is found to be ready. This will only run during daytime.
    """
    now = datetime.now()
    if time(8, 00) <= now.time() <= time(23, 00):
        requests.get("https://maker.ifttt.com/trigger/first_song_found/{my_key}")    

# notify both songs found
def found_both_songs():
    """
    Trigger autoremote app to start dialing automatically. This will also run during the night.
    """
    requests.get(
        'https://autoremotejoaomgcd.appspot.com/sendmessage?key={my_key}')

def update_winning_songs():
    # Scrape winning songs                                                                                                                                                                                                                            
    try:
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        main = soup.find('main')

        for i, child in enumerate(main.children):
            if i == 3:
                child_3 = child

        images = child_3.find_all('img')

        song_1 = images[0]['srcset'].split(' ')[0].split('.')[-3].split('songs_fuer_bulli_')[-1].split('_')
        artist_1 = ' '.join(song_1)

        song_2 = images[2]['srcset'].split(' ')[0].split('.')[-3].split('songs_fuer_bulli_')[-1].split('_')
        artist_2 = ' '.join(song_2)
        print("Song 1: {}".format(artist_1))
        print("Song 2: {}".format(artist_2))
        return artist_1, artist_2
    except:
        return "first song not found", "second song not found"
    
def scrape_and_check(song_1, song_2):
    global song_history
    global browser

    first_song_found = False
    second_song_found = False

    try:
        browser.get(url_live_stream)
    
        now_time.sleep(2)

        song_element = browser.find_element_by_css_selector("li.slick-current")
        current_artist = song_element.get_attribute("data-artist").lower()
        current_title = song_element.get_attribute("data-title").lower()

        current_song = "{}_{}".format(current_artist, current_title)
        
        if current_song != ('_') and current_song != song_history[-1]:
            song_history.append(current_song)
            print(current_song)

            if song_history[-1].find(song_1) != -1:
                print("Found first song")
                found_first_song()

            if song_history[-1].find(song_2) != -1:
                print("Found second song")

                if song_history[-2].find(song_1) != -1:
                    print("Found first song")
                    found_both_songs()
        pass
    except:
        print("Exception!")
        pass


start_time = now_time.time()
#artist_1, artist_2 = update_winning_songs()

song_1 = 'luis fonsi_despacito'
song_2 = 'robbie williams_angel'

print("Song 1: {}".format(song_1))
print("Song 2: {}".format(song_2))
       
print("Sucessfull Loaded, Stating while loop")


while True:
    scrape_and_check(song_1, song_2)
