from flask import Flask,render_template,url_for,request,redirect,session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)

picfolder = os.path.join('static','pic')
picfolder2 =os.path.join('static','pic')

app.config['UPLOAD_FOLDER'] = picfolder
app.config['UPLOAD_FOLDER'] = picfolder2



conn=mysql.connector.connect(host='remotemysql.com',user="ETjUizaEAg",password="a6sB5UPYpW",database="ETjUizaEAg")
cursor=conn.cursor()

@app.route('/')
def login():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'sih.jpeg')
    logo1 = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template('login.html',user_image = pic1,logo_image=logo1)

@app.route('/register')
def about():
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'], 'sih.jpeg')
    logo2 = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template('register.html',user_image = pic2,logo_image2 = logo2)


@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html',)
    else:
        return redirect('/')

@app.route('/login_validation',methods=['GET','POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')


    cursor.execute("""SELECT * FROM `user` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(email,password))
    user=cursor.fetchall()
    if len(user)>0:
        session['user_id']=user[0][0]
        email1 = request.form['email']
        return render_template('home.html',email=email1)
    else:
        return redirect('/')

@app.route('/add_user',methods=['GET','POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    cursor.execute("""INSERT INTO `user` (`name`,`email`,`password`) VALUES
    ('{}','{}','{}')""".format(name,email,password))
    conn.commit()
    return redirect('/')

@app.route('/upload',methods=['GET','POST'])
def upload():
    file = request.form.get('inputfile')

    cursor.execute("""INSERT INTO `photo` (`file`) VALUES
    ('{}')""".format(file))
    conn.commit()
    return "<h3>File Upload Done<h3>"

@app.route('/dropsession')
def dropsession():
    session.pop('user_id',None)
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)
