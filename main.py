from app import app, db
import os

if __name__ == "__main__":
    db.create_all()
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, port=port)
