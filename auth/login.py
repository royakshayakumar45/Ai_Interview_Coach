def login(conn, email, password):
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )
    
    user = cursor.fetchone()

    if user:
        return {
            "email": user[1],
            "role": "user"
        }
    else:
        return None