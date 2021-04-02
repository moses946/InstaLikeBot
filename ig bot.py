#usr/bin/env/python
from selenium import webdriver,common
from selenium.webdriver.common.keys import Keys
import time, re
import getpass


class Instabot():
    def __init__(self, username, password, login_link):
        # initialize variables and instance of firefox to be used in the class
        self.username = username
        self.password = password
        self.login_link = login_link
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        login_url = self.login_link
        #bot.set_window_position(2000,2000)  #sets firefox to a part outside the display window
        bot.get(login_url)
        login_checker = 1
        while login_checker == 1:
            try:
                # find the boxes for login input
                usern = bot.find_element_by_name('username')
                passd = bot.find_element_by_name('password')
                # clear them just to be safe
                usern.clear()
                passd.clear()
                usern.send_keys(self.username)
                passd.send_keys(self.password)
                time.sleep(2)
                passd.send_keys(Keys.RETURN)
                if bool(usern) == True:
                    login_checker = 0
            except common.exceptions.NoSuchElementException or common.exceptions.WebDriverException:
                pass
        postlogin_checker = 1
        while postlogin_checker == 1:
            try:
                # way past saving password to the browser
                save_button = bot.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/section/div/button')
                notnow_button = bot.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button')
                if bool(save_button) == True:
                    postlogin_checker = 0
            except common.exceptions.NoSuchElementException or common.exceptions.WebDriverException:
                pass
        ans_test = 1
        while ans_test == 1:
            # the actual hackaround but getting users consent if desired
            qn = r'Do you want to save login credentials? Y\N: '
            quiz = input(qn)
            q_ans = re.search('[YyNy]', quiz)
            if  bool(q_ans) == True:
                ans_test = 0
                if quiz == 'Y'or"y":
                    time.sleep(1)
                    save_button.send_keys(Keys.RETURN)
                    time.sleep(3)
                elif quiz == 'N'or"n":
                    time.sleep(1)
                    notnow_button.send_keys(Keys.RETURN)
                    time.sleep(3)
            else:
                print("please answer with Y or N")
        notif_alert_check = 1
        while notif_alert_check == 1:
            try:
                notif_off = bot.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
                if bool(notif_off) == True:
                    notif_alert_check = 0
                notif_off.send_keys(Keys.RETURN)
            except common.exceptions.NoSuchElementException:
                pass
    def start_liking(self):
        bot = self.bot
        search_bar = bot.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input')
        search_bar.clear()
        time.sleep(3)
        # get hashtag and add the hash if absent
        hashtag = input("please enter hashtag to search: ")
        if bool("#" in hashtag) == True:
            pass
        else:
            hashtag = "#"+hashtag
        search_bar.send_keys(hashtag)
        time.sleep(2)
        for i in range(1,3): #pressing enter repeatedly because it doesn't always work when pressed once  
            search_bar.send_keys(Keys.RETURN)
        time.sleep(2)
        #check if explore page has loaded
        page_load_c = 1
        while page_load_c == 1:
            try:
                main_cont = bot.find_element_by_css_selector('.SCxLW')
                if bool(main_cont) == True:
                    page_load_c = 0
                    jscript = "window.scrollTo(0, document.body.scrollHeight)"
                    # scroll down the page for more links to load using javascript
                    for i in range(1,4):
                        bot.execute_script(jscript)
                        time.sleep(3)
                    time.sleep(7)
                    a_tags = bot.find_elements_by_xpath("//a[@href]") #gets all the links in the page 
                    all_links = []
                    #pattern to ensure we only get posts' links
                    regex = r"^(https://www.instagram.com)[/][p][/]\w*[&\/]$" 
                    for tag in a_tags:
                        link = tag.get_attribute('href')
                        # filter the links to get the posts' links
                        if bool(re.search(regex, link)) == True:
                            all_links.append(link)
                        else:
                            pass
                    counter = 0 #define it before for loop
                    # will stop looping if page has loaded
                    for link in all_links:
                        bot.get(link)
                        # check if page has loaded
                        link_load_checker = 1
                        while link_load_checker == 1: #check if link loads
                            link_check = bot.find_element_by_css_selector('.wmtNn > div:nth-child(1) > div:nth-child(1) > button:nth-child(1) > div:nth-child(1) > svg:nth-child(1)')
                            if bool(link_check) == True:
                                link_load_checker = 0
                            try:
                                # using 1st try because if like == 1 or none no_oflikes will return an error
                                # gets no of likes
                                no_oflikes = bot.find_element_by_css_selector('button.sqdOP:nth-child(1) > span:nth-child(1)').text 
                                try:
                                    # get the like button 
                                    like_button = bot.find_element_by_css_selector('.fr66n > button:nth-child(1) > div:nth-child(1) > span:nth-child(1) > svg:nth-child(1)') 
                                    label = like_button.get_attribute('aria-label') #gets condition of the post either liked or unliked
                                    if label == 'Like':
                                        # convert no_oflikes to an interger to use for comparison 
                                        try:
                                            no_oflikes = int(no_oflikes)  
                                        except ValueError:
                                            no_oflikes = int(no_oflikes.replace(',',''))
                                        # counter checks no of posts liked
                                        
                                        # only likes posts with more than 150 likes
                                        if no_oflikes > 150:
                                            like_button.click()
                                        else:
                                            pass
                                    elif label == 'Unlike':
                                        # posts that user might have liked before
                                        pass
                                except Exception as exc:
                                    print(exc)       
                            except common.exceptions.NoSuchElementException:
                                pass
                    bot.quit()
            except common.exceptions.NoSuchElementException:
                    pass
if __name__=="__main__":
    # wrapping all actions to be run in a function 
    def last_func():
        try:
            users = input('Enter your username : ')
            time.sleep(1)
            passw = getpass.getpass('Enter your password : ')
            time.sleep(2)
            verif_password = getpass.getpass('Re-enter your password to continue : ')
            n = 1
            while n ==1:
                if passw == verif_password:
                    username = users
                    password = passw  
                    n = 0
                    time.sleep(1)
                    login_url = 'https://www.instagram.com/accounts/login'
                    wakeup = Instabot(username, password, login_url)
                    # run the actual bot
                    wakeup.login()
                    wakeup.start_liking()
                # excecuted if passwords didn't match
                else:
                    print('please try that again')
                    password = getpass.getpass('Enter your password : ')
                    time.sleep(1)
                    verif_password = getpass.getpass('Re-enter your password to continue : ')
        except Exception as error:
            print(error)
    func_runner = 1
    while func_runner == 1:
        last_func()
        time.sleep(2)
          # re-runs the whole file dependig on the users input 
        query = input('Do you want to run the bot again (Y/N) ? ')
        if query == 'Y':
            func_runner= 1
        else:
            func_runner = 0

  
