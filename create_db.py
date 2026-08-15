from app import app, db
from models import User

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('1234')
        db.session.add(admin)
        db.session.commit()
    print("DB created & admin added")
