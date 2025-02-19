from vendamais import database, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

@login_manager.user_loader  # Carregar usuário a partir do BD
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    cpf = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True)



class Endereco(database.Model):
    id = database.Column(database.Integer, primary_key=True) # Adicionando a coluna de ID como chave primária
    rua = database.Column(database.String(100), nullable=False)
    numero = database.Column(database.String(10), nullable=False)
    bairro = database.Column(database.String(50), nullable=False)
    cidade = database.Column(database.String(50), nullable=False)
    estado = database.Column(database.String(2), nullable=False)
    cep = database.Column(database.String(8), nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False) # Relacionamento com o usuário
    usuario = database.relationship('Usuario', backref='enderecos') # Relação inversa com Usuario


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)


class Produto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String(100), nullable=False)
    preco = database.Column(database.Float, nullable=False)
    preco_minimo = database.Column(database.Float, nullable=False)
    quantidade = database.Column(database.Integer, nullable=False)
    imagem = database.Column(database.String(100), nullable=False, default="default.png") # Caminho da imagem
    descricao = database.Column(database.String(200), nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    usuario = database.relationship('Usuario', backref='produtos')

class Newsletter(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(120), unique=True, nullable=False)

class NewsletterForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Inscrever-se')


class Subscription(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Subscription {self.email}>'


class SubscriptionForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Inscrever-se')


class Carrinho(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'))
    id_produto = database.Column(database.Integer, database.ForeignKey('produto.id'))
    quantidade = database.Column(database.Integer, default=1)

    usuario = database.relationship('Usuario', backref='carrinhos')
    produto = database.relationship('Produto', backref='carrinhos')