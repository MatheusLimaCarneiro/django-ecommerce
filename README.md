# 🛒 Django E-commerce API(em desenvolvimento)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/Django%20REST%20Framework-red?style=for-the-badge)
![status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![tests](https://img.shields.io/badge/tests-pytest-blue)



## 📌 Descrição

Este projeto é uma **API de e-commerce desenvolvida em Django Rest Framework**.  
Ela foi construída com o objetivo de **estudar python, Django Rest Framework, arquitetura de APIs, testes automatizados e boas práticas de desenvolvimento backend**, simulando funcionalidades reais de um sistema de compras online.

Atualmente a aplicação conta (ou contará) com módulos como:

- Cadastro de usuários e perfis de cliente
- Gerenciamento de produtos e categorias
- Carrinho de compras
- Itens do carrinho
- Pedidos e fluxo de compra
- Autenticação

---

## 📚 Tecnologias Utilizadas
- Python 3.12
- Django 5.x
- Django Rest Framework
- pytest (testes)
- factory_boy (fixtures)
- Faker (dados falsos)

## ✅ Pré-requisitos

Antes de instalar o projeto, você precisará ter:

- **Python 3.11+** (ou a versão que você estiver usando)
- **Git**
- **Conda** (ou outro gerenciador de ambientes virtuais)
- **pip**

**Opcional** (para testar a API):

- Insomnia / Postman
- Navegador para acessar o Django Admin

---

## 🛠️ Instalação e Configuração

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/MatheusLimaCarneiro/django-ecommerce
cd django-ecommerce
```

### 2️⃣ Criar e ativar o ambiente Conda

```bash
conda create -n django-ecommerce python=3.12
conda activate django-ecommerce
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Rodar migrações
```bash
python manage.py migrate
```

### 5️⃣ Criar usuário admin(recomendado)
```bash
python manage.py createsuperuser
```

### 6️⃣ Executar o servidor
```bash
python manage.py runserver
```

## ▶️ Como Usar a Aplicação

Esta é uma API REST, então você pode usar:

- Insomnia
- Postman
- Thunder Client
- curl
- Navegador (para endpoints GET públicos)

Fluxo básico de uso:

- Criar usuário
- Cadastrar produtos
- Criar carrinho
- Adicionar itens ao carrinho
- Criar pedido

    ⚠️ Nota: Como o projeto ainda está em desenvolvimento, as rotas podem mudar. Assim que todas as funcionalidades forem fechadas, adicionarei aqui a documentação completa de endpoints.

---

## 🧪 Testes Automatizados

O projeto utiliza:

- `pytest`
- `pytest-django`
- `factory_boy` (fábricas de objetos)
- `Faker` (geração de dados fictícios)

### ✔️ Executando os testes

No ambiente virtual já ativado, execute:

```bash
pytest
```

Para executar apenas uma pasta específica:
```bash
pytest apps/nome_do_app/tests/
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um **fork** do projeto

2. Crie uma branch para sua feature:

```bash
git checkout -b feature/nome-da-feature
```

3. Implemente sua alteração

4. Faça o commit seguindo o padrão de mensagens:
```bash
git commit -m "feat: descrição clara da mudança"
```

5. Envie para o seu repositório:
```bash
git push origin feature/nome-da-feature
```

6. Abra um Pull Request descrevendo:

- o que foi alterado
- o motivo da alteração
- qualquer contexto adicional relevante


Dica: sempre descreva claramente o que foi alterado e o motivo.

---

## 🌿 Git Flow Adotado
- `main` → versão estável
- `development` → desenvolvimento ativo

### Padrão de Commits:
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `test:` testes
- `docs:` documentação
- `refactor:` melhoria interna de código

---

## 📜 Licença
Este projeto foi desenvolvido para fins de **estudo**.
Você pode reutilizar o código livremente.