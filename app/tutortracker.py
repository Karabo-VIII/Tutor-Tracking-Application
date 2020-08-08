from app import app, db
from app.models import User, Lecture, Tutor

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Lecture': Lecture, 'Tutor':Tutor}