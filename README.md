# 📜 MATA55 - Team Python: Trabalho final

## O que é

Projeto desenvolvido para a disciplina MATA55 com o Professor Gilberto Leite no semestre de 2024.2 utilizando a linguagem Python, o framework Django e seu Django REST Framework.

Consiste de 3 containeres com serviços distintos (banco de dados, administração deste e servidor web) para fornecer um exemplo teórico da implementação dos conceitos do paradigma de Programação Orientada a Objetos trabalhados na matéria, como abstração, encapsulamento, herança, polimorfismo e outros.

O painel de administração do banco de dado Postgres (acessível em https://localhost:5050 após orquestração dos containeres) facilita a visualização das operações de interação com o sistema.

## Entidades

Esta aplicação instrumentaliza uma API RESTful para manipular um banco de dados PostgreSQL consistente das seguintes entidades:

- Entidade legal
- Pessoa, podendo ser Física ou Jurídica
- Indivíduo (subclasse de Pessoa Física)
- Empresa (subclasse de Pessoa Jurídica)
- Contatos e endereços de entidades

## Como rodar este projeto localmente

1. Instale as dependências necessárias

| Dependência | Fonte |
|-------------|-------|
| git | https://git-scm.com/book/en/v2/Getting-Started-Installing-Git |
| Docker | https://www.docker.com |
| VSCode | https://code.visualstudio.com |
| Extensão Docker | https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker |

2. Clone o projeto e acesse o diretório criado

``` shell
git clone git@github.com:XlipeDCodder/testes.git && cd testes/
```

3. Copie o arquivo .env-example para um arquivo denominado .env

``` shell
cp .env-example .env
```

4. Construa e orquestre os containers

``` shell
docker compose up -d --build
```

5. Utilizando a extensão Docker no VSCode, clique com o botão direito no container testes-web e abra um terminal (Attach Shell ou Conectar Terminal)

6. No terminal do container testes-web, realize as migrações para popular o banco de dados

``` shell
python3 manage.py makemigrations && python3 manage.py migrate
```

7. Crie um superusuário na aplicação

``` shell
python3 manage.py createsuperuser
```

8. Visite http://localhost:8000/admin

Use suas credenciais criadas no passo 6 para manipular as entidades no banco de dados
