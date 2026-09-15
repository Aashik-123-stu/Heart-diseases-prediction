import sqlite3
import bcrypt


DB_NAME = "users.db"


# -----------------------------
# Database Setup
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            result TEXT NOT NULL,
            probability REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Create Account
# -----------------------------
def create_user(username, email, password):

    conn = sqlite3.connect(DB_NAME)

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    try:
        conn.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password.decode("utf-8"))
        )

        conn.commit()
        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "Username or email already exists."

    finally:
        conn.close()


# -----------------------------
# Login
# -----------------------------
def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return False

    stored_password = user[0].encode("utf-8")

    return bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password
    )

# -------prediction history save function--------
def save_prediction(username, result, probability):

    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO prediction_history
        (username, result, probability)
        VALUES (?, ?, ?)
        """,
        (username, result, probability)
    )

    conn.commit()
    conn.close()

# logged-in user ki sirf uski own predictions fetch
def get_prediction_history(username):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.execute(
        """
        SELECT result, probability, created_at
        FROM prediction_history
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,)
    )

    history = cursor.fetchall()

    conn.close()

    return history

# ------ delete history
def delete_prediction_history(username):

    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        DELETE FROM prediction_history
        WHERE username = ?
        """,
        (username,)
    )

    conn.commit()
    conn.close()