from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
import os


app = Flask(__name__)
app.secret_key = 'SecretKey'
fa = FontAwesome(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/joycebiju'
app.config['UPLOAD_FOLDER'] = 'static/upload/'
db = SQLAlchemy(app)

class product(db.Model):
    prod_id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(100), nullable=False)
    prod_description = db.Column(db.String(500))
    prod_collection = db.Column(db.Integer)
    prod_section = db.Column(db.Integer)
    prod_price = db.Column(db.Float, nullable=False)

class highlight(db.Model):
    highlight_id = db.Column(db.Integer, primary_key=True)
    highlight_name = db.Column(db.String(100), nullable=False)
    highlight_description = db.Column(db.String(500))

class collection(db.Model):
    collection_id = db.Column(db.Integer, primary_key=True)
    collection_name = db.Column(db.String(50), nullable=False)

class section(db.Model):
    section_id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(50), nullable=False)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}


@app.route('/')
def home():
    # get list of products
    products = product.query.all()
    highlights = highlight.query.all()

    return render_template('home.html', products=products, highlights=highlights)

@app.route('/brincos')
def brinco():
    # get list of products
    products = product.query.filter(product.prod_section == 1).all()

    return render_template('brincos.html', products=products)

@app.route('/pulseiras')
def pulseira():
    # get list of products
    products = product.query.filter(product.prod_section == 2).all()

    return render_template('pulseiras.html', products=products)

@app.route('/aneis')
def anel():
    # get list of products
    products = product.query.filter(product.prod_section == 3).all()

    return render_template('aneis.html', products=products)

@app.route('/colares')
def colar():
    
    products = product.query.filter(product.prod_section == 4).all()

    return render_template('colares.html', products=products)

@app.route('/destaques')
def dest():
    
    products = product.query.filter(product.prod_section == 5).all()

    return render_template('dest.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' in session and session['username'] == 'admin':
        return redirect(url_for('admin'))
    else:
        if request.method == 'POST':
            if request.form['username'] == 'admin' and request.form['password'] == 'admin':
                session['username'] = request.form['username']
                return redirect(url_for('admin'))
        return render_template('add.html')
       

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' in session and session['username'] == 'admin':
        if request.method == 'POST':
            if request.form.get('prod_add') == 'TRUE':
                # get data from form
                name = request.form['name']
                price = float(request.form['price'])
                description = request.form['description']
                collections = request.form['collection']
                sections = request.form['section']

                # create new product and add to database
                products = product(prod_name=name, prod_price=price, prod_description=description, prod_collection=collections, prod_section=sections)
                db.session.add(products)
                db.session.commit()
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = (f"prod_{products.prod_id}.jpg")
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                return redirect(url_for('admin'))
            
            elif  request.form.get('high_add') == 'TRUE':
                name = request.form['name_high']
                description = request.form['description_high']

                # create new highlight and add to database

                highlights = highlight(highlight_name=name, highlight_description=description)
                db.session.add(highlights)
                db.session.commit()
                file = request.files['image_high']
                if file and allowed_file(file.filename):
                    filename = (f"highlight_{highlights.highlight_id}.jpg")
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('admin'))
            
        # get list of all products
        sections = section.query.all()
        collections = collection.query.all()
        products = product.query.all()
        highlights = highlight.query.all()

        return render_template('admin.html', products=products, collections=collections, sections=sections, highlights=highlights)
    else:
        return redirect(url_for('add'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/product/<int:produto>')
def produto(produto):
    produto = product.query.filter(product.prod_id == produto).all()
    products = product.query.all()
    return render_template('produto.html', products = products, product = produto[0])


app.run(debug=True)