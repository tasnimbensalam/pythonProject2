from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__ , template_folder= 'template')

app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost:3306/crud'
app.config['SQLALCHEMY_TRUCK_MODIFICATIONS']= False

db = SQLAlchemy(app)

class Dataclassroom(db.Model):
    __tablename__ = 'data2'
    id = db.Column(db.Integer, primary_key = True)
    classroom = db.Column(db.String(100))


    def __init__(self,classroom):
        self.classroom= classroom

with app.app_context():
    db.create_all()


class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone= db.Column(db.String(100))
    absenties= db.Column(db.Integer)

    def __init__(self,name,email,phone,absenties):
        self.name= name
        self.email= email
        self.phone = phone
        self.absenties= absenties


with app.app_context():
    db.create_all()

def calculate_absenties(numb_abs) :
    numb=numb_abs+1
    return numb


@app.route('/')
def Index():
    all_data= Data.query.all()
    return render_template("index.html",students= all_data)

@app.route('/insert',methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        absenties = request.form['absenties']


    my_data = Data(name,email,phone,absenties)
    db.session.add(my_data)
    db.session.commit()

    return redirect(url_for('Index'))\

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.absenties = request.form['absenties']
        db.session.commit()
        return redirect(url_for('Index'))\



@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('Index'))

@app.route('/absent/<id>/', methods=['GET', 'POST'])
def absent(id):
    num = Data.query.get(id)
    numb_abs= num.absenties
    num.absenties=calculate_absenties(numb_abs)
    db.session.commit()
    return redirect(url_for('Index'))

@app.route('/list', methods=['GET', 'POST'])
def list():
    all_data = Dataclassroom.query.all()
    return render_template('list.html' , classrooms = all_data)

@app.route('/insert_class',methods = ['POST'])
def insert_class():
    if request.method == 'POST':
        classrooms = request.form['classroom']


    my_data = Dataclassroom(classrooms)
    db.session.add(my_data)
    db.session.commit()

    return redirect(url_for('list'))\

@app.route('/update_class', methods=['GET', 'POST'])
def update_class():
    if request.method == 'POST':
        my_data = Dataclassroom.query.get(request.form.get('id'))
        my_data.classroom = request.form['classroom']
        db.session.commit()
        return redirect(url_for('list'))\

@app.route('/delete_class/<id>/', methods=['GET', 'POST'])
def delete_class(id):
    my_data = Dataclassroom.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    return redirect(url_for('list'))
if __name__=="__main__":
    app.run(debug=True)

#--------------------------------------------------------------------------------------------------------
