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
from .models import Cliente, Importacao
from django.core.paginator import Paginator
from django.http import HttpResponse
from openpyxl import Workbook

def home(request):

    total_clientes = Cliente.objects.count()
    total_importacoes = Importacao.objects.count()
    ultimas_importacoes = Importacao.objects.order_by("-data")[:5]
    ultima_importacao = Importacao.objects.order_by("-data").first()
    
    grafico_labels = []
    grafico_dados = []

    for item in ultimas_importacoes:
        grafico_labels.append(item.arquivo)
        grafico_dados.append(item.importados)

    context = {
        "total_clientes": total_clientes,
        "total_importacoes": total_importacoes,
        "ultimas_importacoes": ultimas_importacoes,
        "grafico_labels": grafico_labels,
        "grafico_dados": grafico_dados,
        "ultima_importacao": ultima_importacao,
    }

    return render(request, "core/home.html", context)

def exportar_excel(request):

    wb = Workbook()
    ws = wb.active
    ws.title = "Clientes"

    ws.append(["Nome", "Email", "Idade"])

    clientes = Cliente.objects.all().order_by("nome")

    for cliente in clientes:
        ws.append([
            cliente.nome,
            cliente.email,
            cliente.idade
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="clientes.xlsx"'

    wb.save(response)

    return response

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

    ultimas_importacoes = Importacao.objects.order_by("-data")[:5]

    return render(
        request,
        "core/upload.html",
        {
            "ultimas_importacoes": ultimas_importacoes
        }
    )
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

def clientes(request):

    nome = request.GET.get("nome")

    if nome:
        clientes = Cliente.objects.filter(nome__icontains=nome)
    else:
        clientes = Cliente.objects.all().order_by("nome")

    paginator = Paginator(clientes, 10)

    page_number = request.GET.get("page")

    clientes = paginator.get_page(page_number)

    return render(
        request,
        "core/clientes.html",
        {"clientes": clientes}
    )

def novo_cliente(request):

    if request.method == "POST":

        Cliente.objects.create(
            nome=request.POST["nome"],
            email=request.POST["email"],
            idade=request.POST["idade"],
        )

        return redirect("clientes")

    return render(request, "core/novo_cliente.html")    

def editar_cliente(request, id):

    cliente = Cliente.objects.get(id=id)

    if request.method == "POST":

        cliente.nome = request.POST["nome"]
        cliente.email = request.POST["email"]
        cliente.idade = request.POST["idade"]

        cliente.save()

        messages.success(request, "Cliente atualizado com sucesso!")

        return redirect("clientes")

    return render(
        request,
        "core/editar_cliente.html",
        {"cliente": cliente}
    )
    
def excluir_cliente(request, id):

    cliente = Cliente.objects.get(id=id)

    if request.method == "POST":
 
        cliente.delete()

        messages.success(request, "Cliente excluído com sucesso!")

        return redirect("clientes")

    return render(
        request,
        "core/excluir_cliente.html",
        {"cliente": cliente}
    )