#import necessary dependencies
from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors, os

application = Flask(__name__)

conn = cursor = None

#open connection to db
def openDB():
    global conn, cursor
    conn = pymysql.connect(
        str(os.environ.get("DB_HOST")), #connect to db witn env
        str(os.environ.get("DB_USERNAME")),
        str(os.environ.get("DB_PASSWORD")),
        str(os.environ.get("DB_NAME"))
    )
    cursor = conn.cursor()
    
#close connection to db
def closeDB():
    global conn, cursor
    cursor.close()
    conn.close()

#home, get all data
@application.route('/') #by default, flask app is live on port 5000
def index():
    openDB()
    container = []
    sql = "SELECT * FROM barang"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDB()
    return render_template('index.html', container=container)

#insert new data
@application.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama_barang = request.form['nama_barang'] 
        harga = request.form['harga']
        stok = request.form['stok']
        openDB()
        sql = "INSERT INTO barang (nama_barang, harga, stok) VALUES (%s, %s, %s)"
        value = (nama_barang, harga, stok)
        cursor.execute(sql, value)
        conn.commit()
        closeDB()
        return redirect(url_for('index'))
    else:
        return render_template('tambah.html')
    
#edit data
@application.route('/edit/<id_barang>', methods=['GET', 'POST'])
def edit(id_barang):
    openDB()
    cursor.execute('SELECT * FROM barang WHERE id_barang = %s', (id_barang))
    data = cursor.fetchone()
    if request.method == 'POST':
        id_barang = request.form['id_barang']
        nama_barang = request.form['nama_barang']
        harga = request.form['harga']
        stok = request.form['stok']
        sql = "UPDATE barang SET nama_barang = %s, harga = %s, stok = %s WHERE id_barang = %s"
        value = (nama_barang, harga, stok, id_barang)
        cursor.execute(sql, value)
        conn.commit()
        closeDB()
        return redirect(url_for('index'))
    else:
        closeDB()
        return render_template('edit.html', data=data)

    
#delete data
@application.route('/hapus/<id_barang>', methods=['GET', 'POST'])
def hapus(id_barang):
    openDB()
    cursor.execute("DELETE FROM barang WHERE id_barang=%s", (id_barang))
    conn.commit()
    closeDB()
    return redirect(url_for('index'))

if __name__ == '__main__':
    application.run(debug=True)