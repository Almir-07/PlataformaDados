import csv

from core.models import Cliente, Importacao


def importar_csv(caminho):

    importados = 0
    ignorados = 0

    with open(caminho, newline="", encoding="utf-8") as csvfile:
        leitor = csv.reader(csvfile)

        next(leitor)

        for linha in leitor:

            if not linha[0].strip() or not linha[1].strip():
                ignorados += 1
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

            except ValueError:
                ignorados += 1

    Importacao.objects.create(
        arquivo=caminho.split("\\")[-1],
        importados=importados,
        ignorados=ignorados,
    )
    
    return {
        "importados": importados,
        "ignorados": ignorados,
    }