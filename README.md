# Plataforma de Importação de Clientes

# Sobre o projeto

Sistema desenvolvido em **Python + Django** para importação, gerenciamento e visualização de clientes através de arquivos CSV.

O sistema realiza a validação dos dados antes da importação, evita registros duplicados utilizando o e-mail como identificador único, registra o histórico das importações e disponibiliza uma API REST completa para gerenciamento dos clientes.

---

# Tecnologias:

- Python
- Django
- Django REST Framework
- Bootstrap 5
- Chart.js
- SQLite
- OpenPyXL
- HTML5
- CSS3

---

# Funcionalidades:

- Dashboard com indicadores
- Upload de arquivos CSV
- Cadastro, edição e exclusão de clientes
- Pesquisa por nome
- Paginação de resultados
- Exportação para Excel
- API REST completa
- Dashboard com gráficos (Chart.js)
- Validação de dados e prevenção de duplicidade

---

# Endpoints

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

## Estrutura do Projeto

PlataformaDados/
│
├── config/
├── core/
├── media/
├── static/
├── templates/
├── manage.py
├── requirements.txt
└── README.md

---

# Como executar

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

# Desenvolvedor

**Almir Filho**

Projeto desenvolvido para estudos de Python, Django e Desenvolvimento Web.

GitHub:
https://github.com/Almir-07