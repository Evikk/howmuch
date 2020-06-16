from selenium import webdriver
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def show_home():
    return render_template('index.html')

@app.route("/results", methods=['GET', 'POST'])
def show_results():
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    browser = webdriver.Chrome(chrome_options=options, executable_path='/usr/local/bin/chromedriver')

    choice = request.form.get("choice")
    limit = int(request.form.get("limit"))
    check = False
    if request.method == 'POST':
        check = request.form.getlist('search')
    amazon_section = ''
    ali_section = ''
    zap_section = ''
    zap_section2 = ''
    zap_template = ''
    zap_results = ''

    if "1" in check:
        url = 'https://www.amazon.com/s?k='
        browser.get(url+choice)
        content = browser.page_source
        soup = BeautifulSoup(content, 'html.parser')
        amazon_section = soup.findAll('div', class_='s-latency-cf-section')

    if "2" in check:
        url = 'https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20200606095835&SearchText='
        # view = '&g=n'
        browser.get(url+choice)
        content = browser.page_source
        soup = BeautifulSoup(content, 'html.parser')
        ali_section = soup.findAll('li', class_='list-item')

    if "3" in check:
        url = 'https://www.zap.co.il/search.aspx?keyword='
        page = requests.get(url+choice)
        soup = BeautifulSoup(page.content, 'html.parser')
        zap_results = soup.find('div', class_='NoResults')
        zap_section = soup.findAll('div', class_='ProductBox')
        zap_section2 = soup.findAll('div', class_='CompareModel')
        zap_template = 1
        for i in zap_section:
            if i.find('div',class_='ProdInfoTitle') != None:
                zap_template = 1
        for i in zap_section2:
            if i.find('div',class_='ProdName') != None:
                zap_template = 2
        
    return render_template('results.html', choice=choice, amazon_section = amazon_section, ali_section = ali_section, zap_results = zap_results, zap_section = zap_section, zap_section2 = zap_section2, zap_template = zap_template, limit = limit+1)


if __name__ == '__main__':
    app.run(debug=True)