# Gastos de campanha e votos em Pernambuco

Projeto final da disciplina de Big Data.

**Pergunta:** candidatos que gastam mais na campanha recebem mais votos?

**Como respondemos:** baixamos dados abertos do TSE (candidatos, votação, receitas e despesas), limpamos e juntamos as bases com Python e Pandas, calculamos indicadores (custo por voto, correlação, faixas de gasto) e geramos gráficos.

- Painel de acompanhamento do grupo: https://phclyra.github.io/projeto-eleicoes/

## Integrantes e funções

| Integrante | Função |
|---|---|
| 1 – *(nome)* | Coordenação, GitHub e infraestrutura |
| 2 – *(nome)* | Limpeza, tratamento e junção das bases |
| 3 – *(nome)* | Indicadores e análises estatísticas |
| 4 – *(nome)* | Visualização, relatório e justificativa |

## Estrutura de pastas

```
scripts/           código Python (config.py + 4 etapas numeradas)
dados/brutos/      arquivos baixados do TSE (não vão para o GitHub)
dados/tratados/    tabela final, depois da limpeza (não vai para o GitHub)
resultados/        tabelas de indicadores e gráficos gerados
docs/              painel de acompanhamento (GitHub Pages)
```

## Como rodar

Precisa de Python 3.10 ou mais novo. Na pasta principal do projeto:

```bash
pip install -r requirements.txt
python scripts/01_baixar_dados.py     # baixa os dados do TSE (Integrante 1)
python scripts/02_limpar_e_juntar.py  # limpa e junta as bases (Integrante 2)
python scripts/03_indicadores.py      # calcula indicadores (Integrante 3)
python scripts/04_graficos.py         # gera os gráficos (Integrante 4)
```

Cada etapa usa o resultado da anterior. O recorte (ano, estado e cargo) fica em `scripts/config.py`.

## Fonte dos dados

Portal de Dados Abertos do TSE: https://dadosabertos.tse.jus.br

## Cuidados com a interpretação

- Correlação entre gasto e votos não prova que o dinheiro causou os votos.
- Para deputado, o gasto cobre a campanha inteira e não só um município.
