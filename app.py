from flask import Flask, request, render_template_string
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# Create table if not exists
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            note TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO notes (timestamp, note) VALUES (%s, %s)", 
                       (datetime.now(), note))
            conn.commit()
            cur.close()
            conn.close()

    # Fetch recent notes
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT timestamp, note FROM notes ORDER BY timestamp DESC LIMIT 10")
    entries = cur.fetchall()
    cur.close()
    conn.close()

    html = '''
    <h1>🍺 Benedictine Brewery - Daily Check-in </h1>
    <form method="post">
        <textarea name="note" rows="4" cols="50" placeholder="How are you today? Energy, mood, gratitude..."></textarea><br><br>
        <input type="submit" value="Save Entry">
    </form>
    <hr>
    <h2>Recent Entries</h2>
    <ul>
    {% for ts, note in entries %}
        <li><strong>{{ ts }}</strong><br>{{ note }}</li>
    {% endfor %}
    </ul>
    '''
    return render_template_string(html, entries=entries)

@app.route('/monk')
def monk_secret():
    password = request.args.get('pass')
    if password == "ora et labora":
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT timestamp, note FROM notes ORDER BY timestamp DESC")
        all_entries = cur.fetchall()
        cur.close()
        conn.close()
        
        html = "<h1>🙏 Secret Monk Archive</h1><ul>"
        for ts, note in all_entries:
            html += f"<li><strong>{ts}</strong><br>{note}</li>"
        html += "</ul>"
        return html
    else:
        return "<h1>Access Denied. Only true monks may enter.</h1>", 403

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5050, debug=False)