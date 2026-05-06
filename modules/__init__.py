# criar admin automaticamente
c.execute("SELECT * FROM users WHERE username='admin'")
if not c.fetchone():
    c.execute("""
    INSERT INTO users (username, password, role)
    VALUES ('admin', 'admin123', 'admin')
    """)
