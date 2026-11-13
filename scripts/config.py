"""Configurações do projeto. Mude aqui o recorte da análise."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent   # pasta principal do projeto

ANO = 2022                      # ano da eleição
UF = "PE"                       # estado
CARGO = "DEPUTADO ESTADUAL"     # como aparece na coluna DS_CARGO, em maiúsculas

PASTA_BRUTOS = RAIZ / "dados" / "brutos"
PASTA_TRATADOS = RAIZ / "dados" / "tratados"
PASTA_RESULTADOS = RAIZ / "resultados"

# Endereços dos arquivos no repositório do TSE (padrão conferido nas páginas do Portal de Dados Abertos).
# Se algum download falhar, confira o endereço em dadosabertos.tse.jus.br.
BASE_URL = "https://cdn.tse.jus.br/estatistica/sead/odsele"
URLS = {
    "candidatos": f"{BASE_URL}/consulta_cand/consulta_cand_{ANO}.zip",
    "votacao": f"{BASE_URL}/votacao_candidato_munzona/votacao_candidato_munzona_{ANO}.zip",
    "contas": f"{BASE_URL}/prestacao_contas/prestacao_de_contas_eleitorais_candidatos_{ANO}.zip",
}

# Padrão dos CSVs do TSE
SEP = ";"
ENCODING = "latin-1"

for _p in (PASTA_BRUTOS, PASTA_TRATADOS, PASTA_RESULTADOS):
    _p.mkdir(parents=True, exist_ok=True)
