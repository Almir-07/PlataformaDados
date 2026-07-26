import csv

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from .models import Arquivo, Cliente, Importacao

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ClienteSerializer

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

        if arquivo:
            fs = FileSystemStorage()
            nome = fs.save(arquivo.name, arquivo)
            caminho = fs.path(nome)

            with open(caminho, newline="", encoding="utf-8") as csvfile:
                leitor = csv.reader(csvfile)

                next(leitor)
                
                importados=0
                ignorados = 0
                
                for linha in leitor:
                    
                    if not linha[0].strip() or not linha[1].strip():
                        ignorados += 1
                        print(f"Linha ignorada: campos obrigatórios vazios -> {linha}")
                        continue
                    
                    if len(linha) != 3:
                        ignorados += 1
                        continue

                    try:
                        idade = int(linha[2])

                        cliente, criado = Cliente.objects.get_or_create(
                            email=linha[1],
                            defaults={
                                "nome": linha[0],
                                "idade": idade,
                            }
                        )

                        if criado:
                            importados += 1
                        
                        print(f"Cliente importado: {linha[0]}")

                    except ValueError:
                        ignorados += 1
                        print(f"Idade inválida: {linha}")

                    print(linha)

            Arquivo.objects.create(nome=nome)

            print(f"Arquivo salvo: {nome}")
            
            Importacao.objects.create(
                arquivo=nome,
                importados=importados,
                ignorados=ignorados,
            )

            messages.success(
                request,
                f"Importação concluída! {importados} cliente(s) importado(s)."
            )

            return redirect("upload")

    return render(request, "core/upload.html")

@api_view(["GET", "POST"])
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