// script.js
document.addEventListener("DOMContentLoaded", function() {
    const cepModal = document.getElementById("cep-modal");
    const closeButton = document.querySelector(".close-button");
    const submitButton = document.getElementById("submit-cep");

    // Função para abrir o modal
    function openModal() {
        cepModal.style.display = "block";
    }

    // Função para fechar o modal
    function closeModal() {
        cepModal.style.display = "none";
    }

    // Adiciona eventos para abrir e fechar o modal
    const openCepModalButton = document.getElementById("open-cep-modal");
    if (openCepModalButton) {
        openCepModalButton.addEventListener("click", openModal);
    }

    closeButton.addEventListener("click", closeModal);

    window.addEventListener("click", function(event) {
        if (event.target === cepModal) {
            closeModal();
        }
    });

    submitButton.addEventListener("click", function() {
        const cepValue = document.getElementById("cep-input").value;
        console.log("CEP enviado:", cepValue); // Aqui você pode adicionar a lógica para usar o CEP
        closeModal(); // Fecha o modal após o envio
    });
});

// script.js

document.addEventListener("DOMContentLoaded", function () {
    const addToCartButtons = document.querySelectorAll(".add-to-cart");
    const buyNowButtons = document.querySelectorAll(".buy-now");
    const popup = document.getElementById("product-popup");
    const closeButton = document.querySelector(".close-button");

    addToCartButtons.forEach(button => {
        button.addEventListener("click", function() {
            const productId = button.getAttribute("data-id");
            // Chame uma função para adicionar ao carrinho
            adicionarAoCarrinho(productId);
        });
    });

    buyNowButtons.forEach(button => {
        button.addEventListener("click", function() {
            const productId = button.getAttribute("data-id");
            // Redirecione para a página de compra
            window.location.href = `/comprar/${productId}`; // Substitua com a URL de compra correta
        });
    });

    closeButton.addEventListener("click", function() {
        popup.style.display = "none";
    });

    // Função para adicionar ao carrinho
    function adicionarAoCarrinho(productId) {
        // Implementar lógica para adicionar ao carrinho
        // Exibir um popup com informações do produto
        const product = produtos.find(prod => prod.id === productId);
        if (product) {
            document.getElementById("popup-title").innerText = product.titulo;
            document.getElementById("popup-image").src = product.imagem;
            document.getElementById("popup-description").innerText = product.descricao;
            document.getElementById("popup-price").innerText = product.preco;
            popup.style.display = "block";
        }
    }
});


$(document).ready(function() {
    $('#editarEnderecoModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Botão que acionou o modal
        var usuario = button.data('usuario') // Obtém os dados do usuário do botão (se aplicável)

        // Preencher o formulário com os dados do usuário
        $('#formEditarEndereco input[name="rua"]').val(usuario.rua);
        $('#formEditarEndereco input[name="numero"]').val(usuario.numero);
        $('#formEditarEndereco input[name="bairro"]').val(usuario.bairro);
        $('#formEditarEndereco input[name="cidade"]').val(usuario.cidade);
        $('#formEditarEndereco input[name="estado"]').val(usuario.estado);
        $('#formEditarEndereco input[name="cep"]').val(usuario.cep);
    });
});
