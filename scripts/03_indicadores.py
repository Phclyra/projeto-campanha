"""Etapa 3: calcula os indicadores que respondem à pergunta do projeto."""
import pandas as pd

import config


def main() -> None:
    df = pd.read_csv(config.PASTA_TRATADOS / "tabela_final.csv")
    # Análises usam candidatos com votos e despesas declaradas
    base = df[(df["votos"] > 0) & (df["despesas"] > 0)].copy()
    base["custo_por_voto"] = base["despesas"] / base["votos"]
    print(f"Candidatos analisados: {len(base):,} de {len(df):,}")

    # 1) Eleitos x não eleitos
    comp = base.groupby("eleito").agg(
        candidatos=("candidato", "count"),
        despesa_media=("despesas", "mean"),
        despesa_mediana=("despesas", "median"),
        votos_medios=("votos", "mean"),
        custo_por_voto_mediano=("custo_por_voto", "median"),
    ).round(2)
    comp.index = comp.index.map({True: "Eleitos", False: "Não eleitos"})
    print("\nEleitos x não eleitos\n", comp)

    # 2) Correlação entre gasto e votos
    pearson = base["despesas"].corr(base["votos"])
    spearman = base["despesas"].corr(base["votos"], method="spearman")
    print(f"\nCorrelação gasto x votos: Pearson = {pearson:.2f} | Spearman = {spearman:.2f}")

    # 3) Segmentos por faixa de gasto (quartis)
    base["faixa_gasto"] = pd.qcut(base["despesas"], 4, labels=["1 (menor gasto)", "2", "3", "4 (maior gasto)"])
    faixas = base.groupby("faixa_gasto", observed=True).agg(
        candidatos=("candidato", "count"),
        votos_medios=("votos", "mean"),
        pct_eleitos=("eleito", "mean"),
        custo_por_voto_mediano=("custo_por_voto", "median"),
    ).round(2)
    faixas["pct_eleitos"] = (faixas["pct_eleitos"] * 100).round(1)
    print("\nSegmentos por faixa de gasto\n", faixas)

    # 4) Outliers de custo por voto (regra do IQR)
    q1, q3 = base["custo_por_voto"].quantile([0.25, 0.75])
    limite = q3 + 1.5 * (q3 - q1)
    outliers = base[base["custo_por_voto"] > limite].sort_values("custo_por_voto", ascending=False)
    print(f"\nOutliers (custo por voto acima de R$ {limite:.2f}): {len(outliers):,}")

    # 5) Gastos por partido
    partidos = base.groupby("partido").agg(
        candidatos=("candidato", "count"), despesa_total=("despesas", "sum"),
        votos_totais=("votos", "sum"), eleitos=("eleito", "sum"),
    ).sort_values("despesa_total", ascending=False).round(2)
    partidos["custo_por_voto"] = (partidos["despesa_total"] / partidos["votos_totais"]).round(2)

    pasta = config.PASTA_RESULTADOS
    base.to_csv(pasta / "base_analise.csv", index=False)
    comp.to_csv(pasta / "eleitos_vs_nao_eleitos.csv")
    faixas.to_csv(pasta / "faixas_de_gasto.csv")
    outliers.head(30).to_csv(pasta / "outliers_custo_por_voto.csv", index=False)
    partidos.to_csv(pasta / "gastos_por_partido.csv")
    with open(pasta / "resumo.txt", "w", encoding="utf-8") as f:
        f.write(f"Correlação gasto x votos: Pearson = {pearson:.2f} | Spearman = {spearman:.2f}\n"
                f"Atenção: correlação não prova que o dinheiro causou os votos.\n")
    print(f"\nResultados salvos em {pasta}/")


if __name__ == "__main__":
    main()
