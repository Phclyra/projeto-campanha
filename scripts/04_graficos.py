"""Etapa 4: gera os gráficos a partir dos resultados (gráficos do Pandas, que usa o Matplotlib)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config

AZUL, AMARELO = "#1D4E9E", "#F2B705"


def salvar(nome: str) -> None:
    plt.tight_layout()
    plt.savefig(config.PASTA_RESULTADOS / nome, dpi=150)
    plt.close()
    print("gerado:", nome)


def main() -> None:
    pasta = config.PASTA_RESULTADOS
    base = pd.read_csv(pasta / "base_analise.csv")
    comp = pd.read_csv(pasta / "eleitos_vs_nao_eleitos.csv", index_col=0)
    faixas = pd.read_csv(pasta / "faixas_de_gasto.csv", index_col=0)
    partidos = pd.read_csv(pasta / "gastos_por_partido.csv", index_col=0)

    comp["despesa_mediana"].plot.bar(color=[AMARELO, AZUL], rot=0, figsize=(6, 4))
    plt.title("Despesa mediana de campanha: eleitos x não eleitos"); plt.ylabel("R$"); plt.xlabel("")
    salvar("1_despesa_eleitos_vs_nao.png")

    ax = base.plot.scatter(x="despesas", y="votos", alpha=0.4, color=AZUL, figsize=(7, 5))
    ax.set_xscale("log"); ax.set_yscale("log")
    plt.title("Despesa x votos (escala logarítmica)"); plt.xlabel("Despesa (R$)"); plt.ylabel("Votos")
    salvar("2_despesa_x_votos.png")

    faixas["pct_eleitos"].plot.bar(color=AZUL, rot=0, figsize=(7, 4))
    plt.title("Percentual de eleitos por faixa de gasto"); plt.ylabel("% de eleitos"); plt.xlabel("Faixa de gasto (quartis)")
    salvar("3_pct_eleitos_por_faixa.png")

    np.log10(base["custo_por_voto"]).plot.hist(bins=30, color=AMARELO, edgecolor="black", figsize=(7, 4))
    plt.title("Distribuição do custo por voto"); plt.xlabel("log10 do custo por voto (R$)"); plt.ylabel("Candidatos")
    salvar("4_distribuicao_custo_por_voto.png")

    partidos["despesa_total"].head(10).sort_values().plot.barh(color=AZUL, figsize=(7, 5))
    plt.title("10 partidos com maior despesa declarada"); plt.xlabel("R$"); plt.ylabel("")
    salvar("5_despesa_por_partido.png")


if __name__ == "__main__":
    main()
