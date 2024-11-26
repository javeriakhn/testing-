from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': '18.212.20.227',  # Replace with your MySQL endpoint
    'user': 'root',  # Replace with your MySQL username
    'password': 'admin123',  # Replace with your MySQL password
    'database': 'notepad_db'  # Replace with the database name you created
}

# Function to connect to MySQL
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Home route: Display all notes
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes ORDER BY created_at DESC')
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', notes=notes)

# Add note route
@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (title, content) VALUES (%s, %s)', (title, content))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_note.html')

# Edit note route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE id = %s', (id,))
    note = cursor.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute('UPDATE notes SET title = %s, content = %s WHERE id = %s', (title, content, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    cursor.close()
    conn.close()
    return render_template('edit_note.html', note=note)

# Delete note route
@app.route('/delete/<int:id>', methods=['GET'])
def delete_note(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
