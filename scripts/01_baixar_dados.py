"""Etapa 1: baixa os arquivos do TSE e extrai apenas os CSVs do estado escolhido."""
import tempfile
import zipfile
from pathlib import Path

import requests

import config


def baixar(url: str, destino: Path) -> None:
    print(f"Baixando {url}")
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        lido = 0
        with open(destino, "wb") as f:
            for bloco in r.iter_content(chunk_size=1024 * 1024):
                f.write(bloco)
                lido += len(bloco)
                if total:
                    print(f"\r  {lido / total:.0%} de {total / 1e6:.0f} MB", end="")
    print()


def extrair_uf(zip_path: Path) -> None:
    sufixo = f"_{config.UF}.csv".lower()
    with zipfile.ZipFile(zip_path) as z:
        for membro in z.namelist():
            if membro.lower().endswith(sufixo):
                z.extract(membro, config.PASTA_BRUTOS)
                print(f"  extraído: {membro}")


def main() -> None:
    for nome, url in config.URLS.items():
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / f"{nome}.zip"
            try:
                baixar(url, destino)
            except requests.RequestException as erro:
                print(f"  ERRO ao baixar '{nome}': {erro}")
                print("  Confira o endereço no Portal de Dados Abertos do TSE e ajuste config.py,")
                print(f"  ou baixe o arquivo manualmente e coloque os CSVs em {config.PASTA_BRUTOS}/")
                continue
            extrair_uf(destino)
    print("Concluído. Arquivos em", config.PASTA_BRUTOS)


if __name__ == "__main__":
    main()
