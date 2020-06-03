from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/student')
def new_student():
   return render_template('student.html')

@app.route('/addrecord',methods = ['POST', 'GET'])
def addrecord():
   if request.method == 'POST':
      msg = "Unknown Error"
      try:
         name = request.form['name']
         address = request.form['address']
         city = request.form['city']
         zipcode = request.form['zipcode']

         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,address,city,zipcode) VALUES(?,?,?,?)",(name,address,city,zipcode))
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "Error in insert operation"

      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("select * from students")

   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)
