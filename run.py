from app import app, db
from app.models import User, Item, Cart

@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Item': Item, 'Cart': Cart}