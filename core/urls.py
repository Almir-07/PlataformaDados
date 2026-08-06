from django.urls import path
from .views import (
    home,
    upload,
    clientes,
    lista_clientes,
    detalhe_cliente,
    exportar_excel,
)
from . import views

urlpatterns = [
    path("", home, name="home"),
    path("upload/", upload, name="upload"),
    path("clientes/", views.clientes, name="clientes"),
    path("clientes/exportar/", exportar_excel, name="exportar_excel"),
    path("clientes/novo/", views.novo_cliente, name="novo_cliente"),
    path("clientes/<int:id>/editar/", views.editar_cliente, name="editar_cliente"),

    path("api/clientes/", lista_clientes, name="lista_clientes"),
    path("api/clientes/<int:id>/", detalhe_cliente, name="detalhe_cliente"),
    path("clientes/<int:id>/excluir/", views.excluir_cliente, name="excluir_cliente"),
]

