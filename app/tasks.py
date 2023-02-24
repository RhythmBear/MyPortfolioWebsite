from app import db
from werkzeug.security import generate_password_hash
from app.models import User

# Function
def add_new_user(username, password):
    hashed_password = generate_password_hash(password=password,
                                             method='pbkdf2:sha256',
                                             salt_length=8)

    new_user = User(username=username,
                    password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
