# Instruções de Instalação

Siga os passos abaixo para configurar o projeto VendaMaisAgro em seu ambiente local.

## Pré-requisitos

- Node.js v14 ou superior
- MongoDB
- Conta na AWS (opcional, para hospedagem)

## Passo a Passo

1. Clone o repositório:

   ```sh
   git clone https://github.com/LeandroOliveirataz/VendaMaisAgro.git
   cd VendaMaisAgro
   ```

2. Instale as dependências do projeto:

   ```sh
   npm install
   ```

3. Configure as variáveis de ambiente:

   Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

   ```env
   MONGODB_URI=mongodb://localhost:27017/vendamaisagro
   JWT_SECRET=sua_chave_secreta
   AWS_ACCESS_KEY_ID=sua_chave_de_acesso_aws
   AWS_SECRET_ACCESS_KEY=sua_chave_secreta_aws
   ```

4. Inicie o servidor de desenvolvimento:

   ```sh
   npm run dev
   ```

5. Acesse a aplicação no navegador:

   ```
   http://localhost:3000
   ```

Pronto! O projeto VendaMaisAgro está configurado em seu ambiente local.
