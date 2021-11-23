from flask import render_template, url_for, flash, redirect, request
from datetime import datetime, timedelta
from flaskweb import db, bcrypt, app
from flaskweb.forms import RegistrationForm, LoginForm, CheckForm
from flaskweb.models import User, Articles, SummarizedArticle
from flask_login import login_user, current_user, logout_user
import jwt
from bs4 import BeautifulSoup
import requests
from transformers import pipeline
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashes_psw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        token = jwt.encode({'user': form.email.data, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        user = User(username=form.username.data, email=form.email.data, password=hashes_psw, token=token)
        db.session.add(user)
        db.session.commit()
        flash(f'You have account, please just login!', 'successLog')
        return redirect(url_for('index'))
    return render_template('reg.html', title='Register', form=form)


@app.route('/log', methods=['GET', 'POST'])
def log():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            token = jwt.encode({'user': form.email.data, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                               app.config['SECRET_KEY'])
            user.token = token
            db.session.add(user)
            db.session.commit()
            flash(f' successfulLog. Hello, {user.username}', 'successLog')
            return redirect(url_for('index'))
        else:
            flash('FailLog, check email and password', 'unsafe')
    return render_template('log.html', title="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/protected')
def protected():
    token = request.args.get('token')
    user = User.query.filter_by(token=token).first()
    if user:
        return '<h1>The token has been verified {}</h1>'.format(token)
    return '<h1>Could not verify your token</h1>'


@app.route('/coin', methods=['GET', 'POST'])
def coin():
    summarizer = pipeline("summarization")
    form = CheckForm()
    textArr = []
    summText = []
    titleArr = []

    if form.validate_on_submit():
        # Scrapper

        cryptoName = (str(form.coin_name.data)).lower()

        url = 'https://coinmarketcap.com/currencies/' + cryptoName + '/news/'
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(url)

        page = driver.page_source
        page_soup = BeautifulSoup(page, 'html.parser')
        news = page_soup.find("div", {"class": "wav26n-1", "class": "gWmJSZ"})

        exists = check(cryptoName)

        for a in news.find_all('a', href=True):
            if a["href"][0:8] == 'https://':
                r = requests.get(a['href'])
                soup = BeautifulSoup(r.text, 'html.parser')
                results = soup.find_all(['h1', 'h3', 'h4', 'h6', 'p'])
                text = [result.text for result in results]
                title = soup.find("title").text.strip()

                ARTICLE = ' '.join(text)
                ARTICLE = ARTICLE.replace('.', '.<eos>')
                ARTICLE = ARTICLE.replace('?', '?<eos>')
                ARTICLE = ARTICLE.replace('!', '!<eos>')
                max_chunk = 500
                sentences = ARTICLE.split('<eos>')
                current_chunk = 0
                chunks = []
                for sentence in sentences:
                    if len(chunks) == current_chunk + 1:
                        if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                            chunks[current_chunk].extend(sentence.split(' '))
                        else:
                            current_chunk += 1
                            chunks.append(sentence.split(' '))
                    else:
                        print(current_chunk)
                        chunks.append(sentence.split(' '))

                for chunk_id in range(len(chunks)):
                    chunks[chunk_id] = ' '.join(chunks[chunk_id])

                res = summarizer(chunks, max_length=130, min_length=10, do_sample=False)
                summarized_text = ' '.join([summ['summary_text'] for summ in res])
                if not exists and len(text) > 0 and len(title) > 0:
                    new_article = Articles(f'{cryptoName}', f'{text}', f'{title}')
                    new_summarized_article = SummarizedArticle(f'{cryptoName}', f'{summarized_text}', f'{title}')
                    db.session.add(new_article)
                    db.session.add(new_summarized_article)
                    db.session.commit()
            else:
                pass



        for row in db.session.query(Articles).filter_by(coin_name=cryptoName):
            textArr.append(row.text)
            titleArr.append(row.title)

        for row in db.session.query(SummarizedArticle).filter_by(coin_name=cryptoName):
            summText.append(row.summarized_text)

        if len(titleArr) != 0:
            flash(f'Successfully pulled {form.coin_name.data}!', 'success')
        else:
            flash(f'Couldn\'t find {form.coin_name.data}!', 'warning')

    return render_template('coin.html', title='Check', form=form, textArr=textArr, titleArr=titleArr, summText=summText)


def check(cryptoName):
    for row in db.session.query(Articles).filter_by(coin_name=cryptoName):
        if row.coin_name == cryptoName:
            return True
    return False
