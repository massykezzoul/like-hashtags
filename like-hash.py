from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException

import time

class TwitterBot:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()
    
    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/')
        bot.maximize_window()
        print("Connection en cours...")
        time.sleep(2) # TODO in future try this : https://selenium-python.readthedocs.io/waits.html
        try:
            #email = bot.find_element_by_css_selector('input.email-input')
            email = bot.find_element_by_name('session[username_or_email]')
            pwd = bot.find_element_by_name('session[password]')
            email.clear() # clear element if it has some text
            pwd.clear()
        except NoSuchElementException:
            print('Unable to locate element')
            bot.quit()
            exit()
        email.send_keys(self.username)
        pwd.send_keys(self.password)
        pwd.send_keys(Keys.RETURN)
        time.sleep(1)

    def like_tweet(self,hashtag):
        bot = self.bot
        bot.get('https://twitter.com/search?q=%23'+hashtag)
        print("Chargement des tweets...")
        time.sleep(1)
        nb = 0
        impossible = 0
        pas = 600 # TODO trouver la bonne taille pour scroller
        scroll = 0
        for i in range(1,20): # scroll for loading tweets
            #tweets = bot.find_elements_by_css_selector('article.css-1dbjc4n.r-1loqt21.r-1udh08x.r-o7ynqc.r-1j63xyz')
            tweets = bot.find_elements_by_css_selector('article div[data-testid=like] svg')
            for tweet in tweets:
                try:
                    tweet.click()
                    time.sleep(5)
                except Exception:
                    impossible += 1

            bot.execute_script('window.scrollTo('+str(scroll)+ ','+ str(scroll+pas) +')')
            scroll += pas
            time.sleep(5)
            nb += len(tweets)
        print(str(nb) + " tweets au total.")
        print(str(nb-impossible) + " tweet liker au total.")
        print(str(impossible)+ " tweets non liker.")
        bot.quit()


mail = 'likehash@yahoo.com'
password = 'motdepasse00'

bot = TwitterBot(mail,password)
bot.login()
bot.like_tweet('hashtag')