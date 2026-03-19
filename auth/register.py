def register_user(conn, email, password):
    cursor = conn.cursor()
    
    try:
        # ✅ DEFAULT ROLE USER
        role = "user"

        # ✅ MAKE YOUR EMAIL ADMIN (CHANGE THIS EMAIL)
        if email == "rautarayakshay09@gmail.com":
            role = "admin"

        cursor.execute(
            "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
            (email, password, role)
        )

        conn.commit()
        return True

    except:
        return False