# ProjectEulerCaptchaSolver

Tool to submit solution to Project Euler Problem solutions without the web browser.

https://projecteuler.net/

I see this project as an excuse to use machine learning and web scraping libraries.

## Config and Directions
- username and password required for logging in as to be placed in 'project_euler_config.json' (you can naturally use another file and replace the path to the json file)
- The file to run is 'euler_project.py'
- The format to submit solutions is to run 'ProjectEulerInterface.submit' with a python dictionary {'problem number' -> 'problem solution'} as argument.
- The first run will build and calibrate the keras model for digit recognition and create a file 'model.h5'.

## Criticism of the Design of Project Euler Website
- If you used the account recovery procedure: until recently (early sept 2019), passwords seems to be stored in clear. Now it seems to be fixed (Sept 13th 2019)
- This code attempts to solve captcha's with a very bad rate of success, nevertheless it seems that we can resubmit new trials any number of time until it works. There could be some submission request number limit.

## Criticism of my code
- The algorithm to solve captcha's is clearly not optimal
  - It assumes that the captcha is a sequence of numbers with all different colors - the separation is done by separating pixels by colors
  - The digit recognition is based on MNIST database, it is just the introduction from an article on medium
 
 https://towardsdatascience.com/image-classification-in-10-minutes-with-mnist-dataset-54c35b77a38d
 
 https://machinelearningmastery.com/save-load-keras-deep-learning-models/ 

- I am using a lot of print statements. I don't want to bring heavy mechinery for such a small script
- tensorflow warnings when running the script - I don't know how to get rid of it.

## Dependencies

All in requirements.txt - you can use
```shell script
pip install -r requirements.txt
```

- MNIST dataset with tensorflow and keras to solve captcha's.
```shell script
pip install tensorflow
pip install keras
```
- mechanize and beautifulsoup to access the website
```shell script
pip install beautifulsoup4
pip install mechanize
```
- Pillow for image processing
```shell script
pip install Pillow
```
## Acknowledgement

Inspired by
https://github.com/fta2012/ProjectEulerCaptchaSolver
which no longer works.

Please contact me for any comments or suggestions.