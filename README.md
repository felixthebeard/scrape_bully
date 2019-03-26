# scrape_bully

This is a short python script for the "ANTENNE BAYERN – VW Bullis geschenkt!"-Lottery.
It scrapes the winning songs from the Antenne Bayern Website
and automatically notify your phone if the songs are played in the correct order.

## The two main parts:
- update_winning_songs: scrapes the winning song names from the website
- scrape_and_check: Listen to the webradio and get the current song names from the steam.
  Reloads the radio stream every 2s to minimize delay.
  
Requirements:
- BeautifulSoup4
- Selenium
- ChromeDriver

Instructions:
- install python requirements with pip
- download chromdriver executable and update path in the script
- setup ifttt and autoremote on your phone and update the keys in the script
- start script with "python scrape_bully.py"
