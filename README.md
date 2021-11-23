# final-project-python
## Title:
Final project. Summary from CoinGecko

## Installation

PyPI
```bash
pip install flask
pip install flask_SQLAlchemy
pip install request
pip install BeautifulSoup
pip install Transformers
pip install jwt
```
or from source
```bash
flask - https://flask.palletsprojects.com/en/2.0.x/
flask_SQLAlchemy - https://flask-sqlalchemy.palletsprojects.com/en/2.x/
request - https://pypi.org/project/requests/
BeautifulSoup - https://www.crummy.com/software/BeautifulSoup/bs4/doc/
Transformers - https://pypi.org/project/transformers/
jwt - https://pyjwt.readthedocs.io/en/stable/
```

## Usage
```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:erkeaiym2408@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
```

## Examples
Firstly, we create account and sing in with this account.
After, we can see search page. Here, for example we searched bitcoin.
![alt text](https://user-images.githubusercontent.com/77783049/143140520-25712d3c-b785-41bd-ad27-0ac37fb9ee59.png)
![alt text](https://user-images.githubusercontent.com/77783049/143140642-a1b3ce7c-e3f3-4d17-9b52-89c4f63c736a.png)
## License
[MIT](https://choosealicense.com/licenses/mit/)
