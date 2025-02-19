from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect

# Inicializar a aplicação Flask
app = Flask(__name__)

# Configurações do aplicativo
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "123456"  # chave secreta para o Flask
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"  # pasta para upload de imagens

# Inicializar as extensões com o app
database = SQLAlchemy(app)  # Banco de dados
bcrypt = Bcrypt(app)  # Criptografia
login_manager = LoginManager(app)  # Gerenciamento de login
csrf = CSRFProtect(app)  # Proteção CSRF

# Configuração da view de login padrão
login_manager.login_view = "homepage"

# Carregamento de usuário para o login_manager
@login_manager.user_loader
def load_usuario(id_usuario):
    from vendamais.models import Usuario  # Importação local para evitar referências circulares
    return Usuario.query.get(int(id_usuario))


# Importar rotas e modelos (deve vir depois da inicialização do db para evitar importação circular)
from vendamais import routes, models