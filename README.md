Plataforma de Importação de Clientes

Sobre o projeto

Sistema desenvolvido em Python utilizando o Django e Django REST Framework para importação de clientes através de arquivos CSV.

O sistema realiza a validação dos dados antes da importação, evita registros duplicados utilizando o e-mail como identificador único, registra o histórico das importações e disponibiliza uma API REST completa para gerenciamento dos clientes.

---

Tecnologias:

- Python
- Django
- Django REST Framework
- SQLite
- HTML
- CSS
- Postman

---

Funcionalidades:

- Importação de arquivos CSV
- Validação de dados
- Evita clientes duplicados
- Registro das importações
- Painel administrativo do Django
- API REST
- CRUD completo
- Serialização de dados em JSON

---

  Endpoints

  Clientes

GET `/api/clientes/`

Lista todos os clientes.

GET `/api/clientes/{id}/`

Retorna um cliente específico.

POST `/api/clientes/`

Cadastra um novo cliente.

PUT `/api/clientes/{id}/`

Atualiza um cliente.

DELETE `/api/clientes/{id}/`

Remove um cliente.

---

## Como executar

Clone o projeto:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta:

```bash
cd PlataformaDados
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual.

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute as migrações:

```bash
python manage.py migrate
```

Inicie o servidor:

```bash
python manage.py runserver
```

---

Almir Filho