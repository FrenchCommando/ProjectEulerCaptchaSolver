import json
from os import remove
from time import sleep
from bs4 import BeautifulSoup
from mechanize import Browser
from captcha_solver import resolve


class ProjectEulerInterface:

    browser = Browser()
    temp_png = 'temp.png'

    @staticmethod
    def display_msg(resp):
        soup = BeautifulSoup(resp, features="html5lib")
        message = soup.find(id='message') or soup.select('#content p')
        return message

    @staticmethod
    def login():
        # login info in a config file
        config_file = "project_euler_config.json"
        with open(config_file) as json_file:
            config = json.load(json_file)
        url = 'https://projecteuler.net/sign_in'

        connected = False
        while not connected:
            resp = ProjectEulerInterface.browser.open(url)
            ProjectEulerInterface.browser.select_form(nr=0)
            soup = BeautifulSoup(resp, features="html5lib")
            msg = soup.find(id='captcha_image')
            print(msg['src'])
            ProjectEulerInterface.browser.retrieve('https://projecteuler.net/' + msg['src'], ProjectEulerInterface.temp_png)
            captcha_answer = resolve(ProjectEulerInterface.temp_png)
            print(captcha_answer)
            remove(ProjectEulerInterface.temp_png)
            ProjectEulerInterface.browser.form['captcha'] = captcha_answer
            ProjectEulerInterface.browser.form['username'] = config["USERNAME"]
            ProjectEulerInterface.browser.form['password'] = config["PASSWORD"]
            resp = ProjectEulerInterface.browser.submit()
            msg = ProjectEulerInterface.display_msg(resp)
            print(msg)
            if "successful" in msg.text:
                print("Sign In successful")
                connected = True
            if "failed" in msg.text:
                raise ValueError("Username or password must be wrong")

    @staticmethod
    def submit(d):
        for problem_num, answer in d.items():
            print('Problem', problem_num, ':')

            url = 'https://projecteuler.net/problem=' + problem_num
            resp = ProjectEulerInterface.browser.open(url)
            soup = BeautifulSoup(resp, features="html5lib")
            signin_msg = soup.find(title='Sign In')
            print(signin_msg)
            if signin_msg is not None:
                print("Need to Log In First")
                ProjectEulerInterface.login()

            resp = ProjectEulerInterface.browser.open(url)
            soup = BeautifulSoup(resp, features="html5lib")
            signout_msg = soup.find(title='Sign Out')
            print("Sign out found - Meaning you are connected", signout_msg)
            if not soup.find(id='captcha_image'):
                # Assume that if you don't see a captcha then this problem was already solved
                print('No captcha found - The Problem is Solved')
                continue

            submitted = False
            while not submitted:
                print()
                print("Attempt to submit solution")
                resp = ProjectEulerInterface.browser.open(url)
                ProjectEulerInterface.browser.select_form(nr=0)
                soup = BeautifulSoup(resp, features="html5lib")
                msg = soup.find(id='captcha_image')
                print(msg)
                print(msg['src'])
                url_path = 'https://projecteuler.net/' + msg['src']
                url_path = 'https://projecteuler.net/' + "captcha/show_captcha.php"
                print(url_path)
                ProjectEulerInterface.browser.retrieve(url_path,
                                                       ProjectEulerInterface.temp_png)
                captcha_answer = resolve(ProjectEulerInterface.temp_png)
                print(captcha_answer)
                remove(ProjectEulerInterface.temp_png)
                ProjectEulerInterface.browser.form['captcha'] = captcha_answer
                ProjectEulerInterface.browser.form['guess_' + str(problem_num)] = answer
                resp = ProjectEulerInterface.browser.submit()
                msg = ProjectEulerInterface.display_msg(resp)
                print(msg)
                if isinstance(msg, list):
                    if "incorrect" in msg[0].text:
                        #   [
                        #   <p> Sorry, but the answer you gave appears to be incorrect. < / p >,
                        #   < p > Go back to < a href = "problem=20" > Problem 20 < / a >.< / p >
                        #   ]
                        print("Answer submitted but incorrect")
                        break
                    if "Congratulations" in msg[0].text:
                        # [<p>Congratulations, the answer you gave to problem 11 is correct.</p>, 
                        # <p>You are the 215573rd person to have solved this problem.</p>, 
                        # <p>This problem had a difficulty rating of 5%. 
                        # The highest difficulty rating you have solved remains at 5%. 
                        # <span class="info"><img src="images/icon_info.png" style="width:15px;vertical-align:top;"/>
                        # <span style="width:200px;left:0;">Problem ID: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10</span></span></p>, 
                        # <p>Return to <a href="problems">Problems</a> page.</p>, 
                        # <p>We hope that you enjoyed solving this problem. 
                        # Please do not deprive others of going through the same process 
                        # by publishing your solution outside of Project Euler; 
                        # for example, on other websites, forums, blogs, 
                        # or any public repositories (e.g. GitHub), et cetera. 
                        # Members found to be spoiling problems will have their accounts locked. 
                        # If you are keen to share your insights and/or see how other members have solved the problem, 
                        # then please visit <a href="thread=11">thread 11</a> in our private discussion forum.</p>]
                        print("Submitted ! Answer is correct !")
                        break
                if "successful" in msg.text:
                    submitted = True

            # Wait 30 seconds
            if submitted:
                sleep(30)  # according to fta2012 there is a limit


if __name__ == "__main__":
    # ProjectEulerInterface.login()
    filename = "..\\output.txt"
    with open(filename, 'r') as res_file:
        res = res_file.readlines()
        d = {}
        k = ''
        for l in res:
            if k == '':
                k = l.split(" ")[-1].strip()
            else:
                v = l.strip()
                d[k] = v
                k = ''
    print(d)
    ProjectEulerInterface.submit(d)
