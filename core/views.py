import csv

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from .models import Arquivo, Cliente, Importacao

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ClienteSerializer
from .services.importacao_service import importar_csv
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

def home(request):
    return render(request, "core/home.html")


def upload(request):

    if request.method == "POST":

        arquivo = request.FILES.get("arquivo")

        if not arquivo:
            messages.error(request, "Selecione um arquivo.")
            return redirect("upload")

        if not arquivo.name.endswith(".csv"):
            messages.error(request, "Envie apenas arquivos CSV.")
            return redirect("upload")

        fs = FileSystemStorage()
        nome = fs.save(arquivo.name, arquivo)
        caminho = fs.path(nome)

        resultado = importar_csv(caminho)

        importados = resultado["importados"]

        Arquivo.objects.create(nome=nome)

        messages.success(
            request,
            f"Importação concluída! {importados} cliente(s) importado(s)."
        )

        return redirect("upload")

    return render(request, "core/upload.html")

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def lista_clientes(request):

    if request.method == "GET":
        nome = request.GET.get("nome")

        if nome:
            clientes = Cliente.objects.filter(nome__icontains=nome)
        else:
            clientes = Cliente.objects.all()

        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ClienteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def detalhe_cliente(request, id):

    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        return Response(
            {"erro": "Cliente não encontrado"},
            status=404
        )

    if request.method == "GET":
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ClienteSerializer(cliente, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
     
    elif request.method == "DELETE":

        cliente.delete()

        return Response(status=204)