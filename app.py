from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
app.secret_key = "Cairocoders-Ednalan"

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'crud'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def Index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('SELECT * FROM students')
    data = cur.fetchall()

    cur.close()
    return render_template('index.html', students=data)


@app.route('/add_contact', methods=['POST'])
def add_students():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        due_amount = request.form['due_amount']
        cur.execute("INSERT INTO students (student_id, first_name, last_name, dob, due_amount) VALUES (%s,%s,%s,%s,%s)", (student_id, first_name, last_name, dob, due_amount))
        conn.commit()
        flash('Student Added successfully')
        return redirect(url_for('Index'))


@app.route('/edit/<student_id>', methods=['POST', 'GET'])
def get_students(student_id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('SELECT * FROM students WHERE student_id = %s', student_id)
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', students=data[0])


@app.route('/update/<student_id>', methods=['POST'])
def update_students(student_id):
    if request.method == 'POST':
        s_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        due_amount = request.form['due_amount']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""UPDATE students SET student_id = %s, 
        first_name = %s, 
        last_name = %s, 
        dob = %s, due_amount = %s 
        WHERE student_id = %s""", (s_id, first_name, last_name, dob, due_amount, student_id))
        flash('Student Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:student_id>', methods=['POST', 'GET'])
def delete_students(student_id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('DELETE FROM students WHERE student_id = {0}'.format(student_id))
    conn.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('Index'))


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
