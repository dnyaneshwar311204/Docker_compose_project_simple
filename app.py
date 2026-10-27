import os
from flask import Flask
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"]
    )

@app.route("/")
def home():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return f"""
        <html>
        <body style="background:#e0f2fe;text-align:center;
                     font-family:Arial;padding:60px">
            <h1 style="color:#2563eb">My Docker Application</h1>
            <h2 style="color:green">Application is running!</h2>
            <p>Database connection successful.</p>
            <p>MySQL version: {version}</p>
        </body>
        </html>
        """
    except Exception as error:
        app.logger.exception("Database connection failed")
        return "Database connection failed. Check application logs.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
