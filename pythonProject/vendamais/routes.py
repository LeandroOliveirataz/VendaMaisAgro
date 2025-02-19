from flask import render_template, url_for, redirect, flash, request, Blueprint
from vendamais import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from vendamais.forms import FormLogin, FormCriarConta, FormFoto, SubscriptionForm, FormProduto, FormEditarEndereco
from vendamais.models import Usuario, Foto, Subscription, Newsletter, Produto, Carrinho
import os
from werkzeug.utils import secure_filename
from decimal import Decimal
import uuid

# Função para salvar imagens
def salvar_imagem(imagem):
    if imagem:
        if not imagem.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            flash('Tipo de arquivo não suportado. Apenas JPG e PNG são permitidos.', 'danger')
            return None

        nome_imagem = str(uuid.uuid4()) + os.path.splitext(imagem.filename)[1]
        caminho_imagem = os.path.join(app.root_path, 'static/fotos_posts', nome_imagem)

        diretorio = os.path.dirname(caminho_imagem)
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        try:
            imagem.save(caminho_imagem)
            return nome_imagem
        except Exception as e:
            flash(f'Erro ao salvar a imagem: {e}', 'danger')
            return None
    return None

###############    HOMEPAGE    ################################
@app.route("/")
def homepage():
    # Buscar os últimos produtos adicionados
    produtos_ultimos = Produto.query.order_by(Produto.data_criacao.desc()).limit(5).all()
    return render_template("homepage.html", produtos=produtos_ultimos)

###############    LOGIN    ################################
@app.route("/login", methods=["GET", "POST"])
def login():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("perfil", id_usuario=usuario.id))
        else:
            flash("Email ou senha incorretos. Tente novamente.", "danger")
    return render_template("login.html", form=formlogin)

###############    CRIAR CONTA   ##############################
@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()

    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(
            username=form_criarconta.username.data,
            cpf=form_criarconta.cpf.data,
            email=form_criarconta.email.data,
            senha=senha
        )

        try:
            database.session.add(usuario)
            database.session.commit()
            flash("Conta criada com sucesso!", "success")
            login_user(usuario, remember=True)
            return redirect(url_for("perfil", id_usuario=usuario.id))
        except Exception as e:
            database.session.rollback()
            flash(f"Erro ao criar a conta: {e}", "danger")

    return render_template("criarconta.html", form=form_criarconta)

###############    USUARIO   ##################################
@app.route('/perfil/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    form = FormProduto()  # Formulário para adicionar produtos
    form_endereco = FormEditarEndereco()  # Formulário para editar endereço

    if form.validate_on_submit():
        # Converte preço e preço mínimo de vírgula para ponto
        preco = Decimal(str(form.preco.data).replace(',', '.'))
        preco_minimo = Decimal(str(form.preco_minimo.data).replace(',', '.'))

        # Verifique se a imagem foi recebida
        if form.imagem.data:
            imagem_path = salvar_imagem(form.imagem.data)
        else:
            imagem_path = None  # Mensagem caso nenhuma imagem seja enviada

        try:
            novo_produto = Produto(
                titulo=form.titulo.data,
                descricao=form.descricao.data,
                preco=preco,
                preco_minimo=preco_minimo,
                quantidade=form.quantidade.data,
                imagem=imagem_path,
                id_usuario=usuario.id
            )

            database.session.add(novo_produto)
            database.session.commit()
            flash('Produto cadastrado com sucesso!', 'success')
        except Exception as e:
            database.session.rollback()
            flash(f'Erro ao cadastrar produto: {e}', 'danger')

    if form_endereco.validate_on_submit():
        usuario.endereco = form_endereco.endereco.data  # Supondo que a classe Usuario tenha um campo endereco
        database.session.commit()
        flash('Endereço atualizado com sucesso!', 'success')

    return render_template('perfil.html', usuario=usuario, form=form, form_endereco=form_endereco)

###############    LOGOUT   ###################################
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

###############    SOBRE   ####################################
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

###############    FALE CONOSCO   #############################
@app.route('/fale_conosco', methods=['GET', 'POST'])
def fale_conosco():
    form = SubscriptionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            nome = form.nome.data
            email = form.email.data
            telefone = form.telefone.data
            mensagem = form.mensagem.data
            flash('Inscrição realizada com sucesso!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Erro ao se inscrever. Tente novamente.', 'error')

    return render_template('fale_conosco.html', form=form)

###############    PRODUTOS   #################################
@app.route("/produtos/<int:id_usuario>", methods=["GET", "POST"])
@login_required
def produtos(id_usuario):
    form_produto = FormProduto()

    if form_produto.validate_on_submit():
        try:
            # Salve a imagem usando a função definida
            imagem_path = salvar_imagem(form_produto.imagem.data)

            # Converte preço e preço mínimo de vírgula para ponto
            preco = Decimal(str(form_produto.preco.data).replace(',', '.'))
            preco_minimo = Decimal(str(form_produto.preco_minimo.data).replace(',', '.'))

            produto = Produto(
                titulo=form_produto.titulo.data,
                descricao=form_produto.descricao.data,
                preco=preco,
                preco_minimo=preco_minimo,
                quantidade=form_produto.quantidade.data,
                imagem=imagem_path,
                id_usuario=current_user.id
            )
            database.session.add(produto)
            database.session.commit()
            flash("Produto postado com sucesso!", "success")
        except Exception as e:
            database.session.rollback()
            flash(f'Erro ao cadastrar produto: {e}', 'danger')

    return render_template("produtos.html", usuario=current_user, form=form_produto)

@app.route("/produto/<int:id_produto>")
def produto_detalhes(id_produto):
    produto = Produto.query.get_or_404(id_produto)
    return render_template("produto_detalhes.html", produto=produto)

###############    FEED   #####################################
@app.route("/feed")
def feed():
    produtos = Produto.query.order_by(Produto.data_criacao.desc()).all()[:20]
    return render_template("feed.html", produtos=produtos)

###############    CARRINHO   #################################
@app.route('/carrinho')
@login_required
def carrinho():
    itens_carrinho = Carrinho.query.filter_by(id_usuario=current_user.id).all()
    return render_template('carrinho.html', itens_carrinho=itens_carrinho)

@app.route('/adicionar_ao_carrinho/<int:id_produto>', methods=['POST'])
@login_required
def adicionar_ao_carrinho(id_produto):
    produto = Produto.query.get(id_produto)
    if produto:
        item_carrinho = Carrinho.query.filter_by(id_usuario=current_user.id, id_produto=id_produto).first()
        if item_carrinho:
            item_carrinho.quantidade += 1  # Aumenta a quantidade se já existir
        else:
            item_carrinho = Carrinho(id_usuario=current_user.id, id_produto=id_produto)
            database.session.add(item_carrinho)
        database.session.commit()
        flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('homepage'))

@app.route("/remover_do_carrinho/<int:id_produto>", methods=["POST"])
@login_required
def remover_do_carrinho(id_produto):
    item_carrinho = Carrinho.query.filter_by(id_usuario=current_user.id, id_produto=id_produto).first()
    if item_carrinho:
        database.session.delete(item_carrinho)
        database.session.commit()
        flash("Produto removido do carrinho!", "success")
    else:
        flash("Produto não encontrado no carrinho.", "warning")

    return redirect(url_for("carrinho"))


# Rota para finalizar a compra
@app.route('/finalizar_compra', methods=['GET', 'POST'])
@login_required
def finalizar_compra():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        endereco = request.form.get('endereco')
        pagamento = request.form.get('pagamento')

        # Processar o pedido e limpar o carrinho
        # Exemplo de como você pode adicionar a lógica de compra
        carrinho = session.get('carrinho', [])
        if not carrinho:
            flash('Seu carrinho está vazio. Adicione produtos para comprar.', 'danger')
            return redirect(url_for('produtos'))  # Redireciona para a página de produtos

        # Aqui você pode armazenar os dados do pedido no banco de dados, criar transações, etc.
        # Exemplo:
        pedido = Pedido(nome=nome, email=email, endereco=endereco, pagamento=pagamento)
        database.session.add(pedido)

        for item in carrinho:
            produto = Produto.query.get(item['produto_id'])
            # Adicionar lógica para associar os itens ao pedido (caso você tenha uma relação no banco de dados)
            pedido_itens = PedidoItem(pedido_id=pedido.id, produto_id=produto.id, quantidade=item['quantidade'])
            database.session.add(pedido_itens)

        database.session.commit()

        # Limpar o carrinho após a compra
        session.pop('carrinho', None)

        flash('Compra finalizada com sucesso!', 'success')
        return redirect(url_for('homepage'))  # Redireciona para a homepage após a compra

    return render_template('finalizar_compra.html')


###############    CARTEIRA   #################################
@app.route('/carteira/<int:id_usuario>', methods=['GET'])
@login_required
def carteira(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    # Lógica para obter dados da carteira do usuário
    # Exemplo de como você pode buscar o saldo e transações
    saldo = usuario.saldo
    transacoes = Transacao.query.filter_by(usuario_id=id_usuario).all()
    return render_template('carteira.html', usuario=usuario, saldo=saldo, transacoes=transacoes)


###############    Minhas Compras   #################################
@app.route('/compras/<int:id_usuario>')
@login_required
def compras(id_usuario):
    # Aqui você pode adicionar a lógica para exibir as compras do usuário.
    # Exemplo de como buscar as compras
    compras = Pedido.query.filter_by(usuario_id=id_usuario).all()
    return render_template('compras.html', compras=compras, id_usuario=id_usuario)


###############    Minhas Vendas   #################################
@app.route('/vendas/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def vendas(id_usuario):
    # Lógica para exibir as vendas do usuário
    vendas = Produto.query.filter_by(id_usuario=id_usuario).all()
    return render_template("vendas.html", vendas=vendas, id_usuario=id_usuario)


###############    Endereco  #################################
@app.route('/editar_endereco/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def editar_endereco(id_usuario):
    # Verificar se o usuário está logado e se é o mesmo id
    if current_user.id != id_usuario:
        return redirect(url_for('index'))  # ou outra página de redirecionamento

    usuario = Usuario.query.get(id_usuario)

    # Verificar se o usuário tem pelo menos um endereço
    if not usuario.enderecos:
        return redirect(url_for('perfil'))  # Se não houver endereços, redireciona para o perfil

    # Acessar o primeiro endereço
    endereco = usuario.enderecos[0]

    # Criar o formulário de edição de endereço e preencher com os dados do primeiro endereço
    form = FormEditarEndereco(obj=endereco)

    # Verificar se o formulário foi enviado e é válido
    if form.validate_on_submit():
        endereco.rua = form.rua.data
        endereco.numero = form.numero.data
        endereco.bairro = form.bairro.data
        endereco.cidade = form.cidade.data
        endereco.estado = form.estado.data
        endereco.cep = form.cep.data

        # Salvar as alterações no banco de dados
        database.session.commit()
        flash('Endereço atualizado com sucesso!', 'success')
        return redirect(url_for('perfil', id_usuario=id_usuario))  # Redireciona para o perfil após salvar

    return render_template('perfil.html', form_endereco=form)


###############    Contrato   #################################
@app.route('/contrato', methods=['GET', 'POST'])
def contrato():
    # Sua lógica aqui
    return render_template('contrato.html')


###############    Newsletter   #################################
@app.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    # Sua lógica para lidar com o formulário da newsletter
    return render_template('newsletter.html')


###############    Editar Produto   #################################
@app.route('/editar_produto/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    form = FormProduto(obj=produto)

    if form.validate_on_submit():
        produto.titulo = form.titulo.data
        produto.preco = form.preco.data
        produto.descricao = form.descricao.data
        produto.quantidade = form.quantidade.data
        produto.imagem = form.imagem.data

        database.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('vendas', id_usuario=current_user.id))  # Redireciona para as vendas do usuário

    return render_template('editar_produto.html', form=form, produto=produto)


################################################
if __name__ == "__main__":
    app.run(debug=True)
