from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)
DB = 'tasks.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending'
        )''')
        db.commit()

@app.route('/')
def index():
    db = get_db()
    tasks = db.execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        if title:
            db = get_db()
            db.execute('INSERT INTO tasks (title, description) VALUES (?, ?)', (title, description))
            db.commit()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id=?', (id,)).fetchone()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        db.execute('UPDATE tasks SET title=?, description=?, status=? WHERE id=?',
                   (title, description, status, id))
        db.commit()
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:id>')
def delete_task(id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id=?', (id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    db = get_db()
    tasks = db.execute("SELECT * FROM tasks WHERE title LIKE ?", (f'%{query}%',)).fetchall()
    return render_template('index.html', tasks=tasks, query=query)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)