from vendamais import database
from pythonProject.vendamais import app

with app.app_context():
    database.create_all() # Isso criará as tabelas no banco de dados
