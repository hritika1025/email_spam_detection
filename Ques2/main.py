from flask import Flask ,render_template, session, url_for, request
import sqlite3 as sql
from flask_mysqldb import MySQL
import MySQLdb.cursors
from collections import Counter
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score

app = Flask(__name__, template_folder = 'template', static_folder = 'static')


app.secret_key='#the#secret#key#'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mitika@03'
app.config['MYSQL_DB'] = 'spam_test'

mysql = MySQL(app)
print(mysql)
@app.route("/", methods = ['GET', 'POST'])
def home():
    msg = ''
    if request.method == 'POST' :
        mail = request.form['mail']
        if len(mail) > 0:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO email VALUES (NULL, % s)',(mail,))
            mysql.connection.commit()
            cursor.close()
            session['mail'] = mail
        df = pd.read_csv('SMSSpamCollection', delimiter='\t',header=None)

        X_train_raw, X_test_raw, y_train, y_test = train_test_split(df[1],df[0])

        vectorizer = TfidfVectorizer()
        X_train = vectorizer.fit_transform(X_train_raw)
        classifier = LogisticRegression()
        classifier.fit(X_train, y_train)

        X_test = vectorizer.transform( [mail] )
        prediction = classifier.predict(X_test)
        msg = "This message is " + prediction



    return render_template('home.html', msg = msg)

app.run(debug=True)