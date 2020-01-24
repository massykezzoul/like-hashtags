from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time

class TwitterBot:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()
        self.likeDelay = 5
    
    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/')
        bot.maximize_window()
        print("Connection en cours...")
        time.sleep(4) # TODO in future find a more efficient wait method
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
        time.sleep(4)
        # TODO check connection done
        print("Connection done.")
    
    def like_tweet(self,hashtag,toLike = 10):
        bot = self.bot
        bot.get('https://twitter.com/search?q=%23'+hashtag)
        print("Entrain de liker des tweets...")
        time.sleep(3)
        nb = 0
        liked = 0
        impossible = 0
        pas = 300 # TODO trouver la bonne taille pour scroller
        scroll = 0
        while liked <= toLike: # scroll for loading tweets
            #tweets = bot.find_elements_by_css_selector('article.css-1dbjc4n.r-1loqt21.r-1udh08x.r-o7ynqc.r-1j63xyz')
            tweets = bot.find_elements_by_css_selector('article div[data-testid=like] svg, div.HeartAnimation') # like button
            nb += len(tweets)
            for tweet in tweets:
                try:
                    tweet.click()
                    liked += 1
                    time.sleep(self.likeDelay)
                except Exception:
                    impossible += 1

            scroll += pas
            bot.execute_script('window.scrollTo(0,'+ str(scroll) +')')
            time.sleep(2) # waiting for element to load after a scroll
        print(str(nb) + " tweets au total.")
        print(str(liked) + " tweets liker au total.")
        print(str(impossible)+ " tweets non liker.")
        
        
    def quit(self):
        self.bot.quit()


mail = 'likehash@yahoo.com'
password = 'motdepasse00'

bot = TwitterBot(mail,password)
hashtags = ['github','developer','dev','botTwitter','bot','TwitterBot']
for hashtag in hashtags:
    bot.login()
    print("liking #"+hashtag+"...")
    bot.like_tweet(hashtag,30)
bot.quit()