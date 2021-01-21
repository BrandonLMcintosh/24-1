from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """connects to the db"""
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    
    __tablename__ = "pets"

    def __repr(self):
        p = self
        return f'''
            id: {p.id}
            name: {p.name}
            species: {p.species}
            photo_url: {p.photo_url}
            age: {p.age}
            notes: {p.notes}
            available: {p.available}
        '''

    id = db.Column(db.Integer, nullable=False, primary_key=True, auto_increment=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text, default="https://i1.wp.com/cullmanfumc.com/wp-content/uploads/2017/09/animal-paw-vector-icon-animals-icons-icons-download-0.png?ssl=1")
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)

    def adopt(self):

        self.available = False
        db.session.add(self)
        db.session.commit()
    