from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector  # type: ignore

app = Flask(__name__)
app.secret_key = "supersecretkey"  
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="blog"
    )

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articulos")
    articulos = cursor.fetchall()
    conn.close()
    return render_template('index.html', articulos=articulos)

@app.route('/add', methods=['POST'])
def add():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO articulos (titulo, introduccion, anio, autores) VALUES (%s, %s, %s, %s)",
                       (request.form['titulo'], request.form['introduccion'], request.form['anio'], request.form['autores']))
        conn.commit()

        conn.close()
        return redirect('/')
    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return redirect('/')

@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articulos WHERE id = %s", (id,))
    articulo = cursor.fetchone()
    conn.close()
    return render_template('edit.html', articulo=articulo)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE articulos SET titulo=%s, introduccion=%s, anio=%s, autores=%s WHERE id=%s",
                       (request.form['titulo'], request.form['introduccion'], request.form['anio'], request.form['autores'], id))
        conn.commit()

        conn.close()
        return redirect('/')
    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        
        cursor.execute("DELETE FROM articulos WHERE id = %s", (id,))
        conn.commit()

        conn.close()
        return redirect('/')
    except Exception as e:
        flash(f"Error: {str(e)}", 'error')
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
