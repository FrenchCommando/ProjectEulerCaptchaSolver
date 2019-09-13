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
                print('Solved')
                break

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
                    #   [
                    #   <p> Sorry, but the answer you gave appears to be incorrect. < / p >,
                    #   < p > Go back to < a href = "problem=20" > Problem 20 < / a >.< / p >
                    #   ]
                    if "incorrect" in msg[0].text:
                        print("Answer submitted but incorrect")
                        break
                    print("Submitted I guess ...")
                if "successful" in msg.text:
                    submitted = True

            # Wait 30 seconds
            if submitted:
                sleep(30)  # according to fta2012 there is a limit


if __name__ == "__main__":
    # ProjectEulerInterface.login()
    ProjectEulerInterface.submit({'20': '151515', '66': '69'})
