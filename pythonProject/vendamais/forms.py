from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from vendamais.models import Usuario


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")


class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Nome de usuário', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(11)])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado, faça login para continuar.")

    def validate_cpf(self, cpf):
        usuario = Usuario.query.filter_by(cpf=cpf.data).first()
        if usuario:
            raise ValidationError("CPF já cadastrado, faça login para continuar.")


class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    botao_confirmacao = SubmitField("Enviar")


class FormProduto(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    preco = DecimalField('Preço', validators=[DataRequired(), NumberRange(min=0)], places=2)
    preco_minimo = DecimalField('Preço Mínimo', validators=[DataRequired(), NumberRange(min=0)], places=2)
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    imagem = FileField('Imagem', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Produto')

    def validate_precos(self):
        # Converter os valores para ponto
        if self.preco.data:
            self.preco.data = float(str(self.preco.data).replace(',', '.'))
        if self.preco_minimo.data:
            self.preco_minimo.data = float(str(self.preco_minimo.data).replace(',', '.'))

        # Verifica se o preço mínimo é menor que o preço
        if self.preco_minimo.data >= self.preco.data:
            raise ValidationError("O preço mínimo deve ser menor que o preço do produto.")


class SubscriptionForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()],
                       render_kw={"placeholder": "Digite seu nome"})
    email = StringField('E-mail', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Digite seu e-mail"})
    telefone = StringField('Telefone', validators=[DataRequired()],
                           render_kw={"placeholder": "Digite seu telefone"})
    mensagem = TextAreaField('Mensagem', validators=[DataRequired()],
                             render_kw={"placeholder": "Escreva sua mensagem aqui..."})
    submit = SubmitField('Inscrever-se')


class FormEndereco(FlaskForm):
    rua = StringField('Rua', validators=[DataRequired()])
    numero = StringField('Número', validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    cep = StringField('CEP', validators=[DataRequired()])
    submit = SubmitField('Salvar Alterações')

class FormUsuario(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=120)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Salvar Usuário')

class FormEndereco(FlaskForm):
    rua = StringField('Rua', validators=[DataRequired(), Length(max=100)])
    numero = StringField('Número', validators=[DataRequired(), Length(max=10)])
    bairro = StringField('Bairro', validators=[DataRequired(), Length(max=50)])
    cidade = StringField('Cidade', validators=[DataRequired(), Length(max=50)])
    estado = StringField('Estado', validators=[DataRequired(), Length(max=50)])
    cep = StringField('CEP', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Salvar Endereço')


class FormEditarEndereco(FlaskForm):
    rua = StringField('Rua', validators=[DataRequired()])
    numero = StringField('Número', validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired()])
    cidade = StringField('Cidade', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    cep = StringField('CEP', validators=[DataRequired()])
    submit = SubmitField('Salvar alterações')

