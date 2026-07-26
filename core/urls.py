from django.urls import path
from .views import home, upload, lista_clientes, detalhe_cliente

urlpatterns = [
    path("", home, name="home"),
    path("upload/", upload, name="upload"),

    path("api/clientes/", lista_clientes, name="lista_clientes"),
    path("api/clientes/<int:id>/", detalhe_cliente, name="detalhe_cliente"),
]

