from  flask import Flask, render_template, request, redirect
from  flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




db = SQLAlchemy(app)

class Item (db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    text = db.Column(db.Text, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    isActive = db.Column(db.Boolean, default=True)
    count = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return  self.title

@app.route('/buy/<int:id>')
def buy(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": int(item.price)*100
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/about')
def about():
    return render_template('about.html')





@app.route('/sales')
def sales():
    items = Item.query.all()
    return render_template('sales.html', data = items)

@app.route('/create', methods = ['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']
        count = request.form['count']
        item = Item(title = title, price = price, text = text, count = count)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return render_template('home.html')
        pass
    else:
        return render_template('create.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug = True)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
