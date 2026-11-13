"""Etapa 2: limpa as bases (candidatos, votação, receitas, despesas) e junta em uma tabela só."""
import pandas as pd

import config


def achar_csv(prefixo: str):
    achados = sorted(config.PASTA_BRUTOS.glob(f"{prefixo}*_{config.UF}.csv"))
    if not achados:
        raise FileNotFoundError(f"Nenhum CSV '{prefixo}*_{config.UF}.csv' em {config.PASTA_BRUTOS}")
    return achados[0]


def ler(prefixo: str, colunas: list[str]) -> pd.DataFrame:
    caminho = achar_csv(prefixo)
    df = pd.read_csv(
        caminho, sep=config.SEP, encoding=config.ENCODING, dtype=str,
        usecols=lambda c: c in colunas, low_memory=False,
    )
    faltando = [c for c in colunas if c not in df.columns]
    if faltando:
        raise ValueError(f"{caminho.name}: colunas não encontradas {faltando}. Veja df.columns e ajuste.")
    print(f"{caminho.name}: {len(df):,} linhas lidas")
    return df


def para_numero(serie: pd.Series) -> pd.Series:
    """Converte textos como '1234,56' em número."""
    return pd.to_numeric(serie.str.replace(".", "", regex=False).str.replace(",", ".", regex=False), errors="coerce")


def somar_por_candidato(df: pd.DataFrame, coluna: str, novo_nome: str) -> pd.DataFrame:
    df[coluna] = para_numero(df[coluna]).fillna(0)
    return df.groupby("SQ_CANDIDATO", as_index=False)[coluna].sum().rename(columns={coluna: novo_nome})


def main() -> None:
    # Candidatos
    cand = ler("consulta_cand", ["SQ_CANDIDATO", "NM_URNA_CANDIDATO", "SG_PARTIDO", "DS_CARGO", "DS_SIT_TOT_TURNO"])
    cand = cand.dropna(subset=["SQ_CANDIDATO"]).drop_duplicates("SQ_CANDIDATO")
    for c in ["NM_URNA_CANDIDATO", "SG_PARTIDO", "DS_CARGO", "DS_SIT_TOT_TURNO"]:
        cand[c] = cand[c].str.strip().str.upper()
    cand = cand[cand["DS_CARGO"] == config.CARGO]
    cand["eleito"] = cand["DS_SIT_TOT_TURNO"].str.startswith("ELEITO", na=False)
    print(f"Candidatos a {config.CARGO}: {len(cand):,}")

    # Votos
    vot = ler("votacao_candidato_munzona", ["SQ_CANDIDATO", "QT_VOTOS_NOMINAIS"])
    vot["QT_VOTOS_NOMINAIS"] = pd.to_numeric(vot["QT_VOTOS_NOMINAIS"], errors="coerce").fillna(0)
    votos = vot.groupby("SQ_CANDIDATO", as_index=False)["QT_VOTOS_NOMINAIS"].sum().rename(
        columns={"QT_VOTOS_NOMINAIS": "votos"})

    # Receitas e despesas
    receitas = somar_por_candidato(ler("receitas_candidatos", ["SQ_CANDIDATO", "VR_RECEITA"]), "VR_RECEITA", "receitas")
    despesas = somar_por_candidato(
        ler("despesas_contratadas_candidatos", ["SQ_CANDIDATO", "VR_DESPESA_CONTRATADA"]),
        "VR_DESPESA_CONTRATADA", "despesas")

    # Junção: uma linha por candidato
    final = (cand.merge(votos, on="SQ_CANDIDATO", how="left")
                 .merge(receitas, on="SQ_CANDIDATO", how="left")
                 .merge(despesas, on="SQ_CANDIDATO", how="left"))
    final[["votos", "receitas", "despesas"]] = final[["votos", "receitas", "despesas"]].fillna(0)
    final = final.rename(columns={"NM_URNA_CANDIDATO": "candidato", "SG_PARTIDO": "partido",
                                  "DS_CARGO": "cargo", "DS_SIT_TOT_TURNO": "situacao"})

    saida = config.PASTA_TRATADOS / "tabela_final.csv"
    final.to_csv(saida, index=False)
    print(f"\nTabela final: {len(final):,} candidatos | sem votos: {(final['votos'] == 0).sum():,} | "
          f"sem despesas: {(final['despesas'] == 0).sum():,}")
    print(f"Salva em {saida}")


if __name__ == "__main__":
    main()
