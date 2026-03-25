# 🎵 Análise de Tendências Globais do Spotify — 2026

Análise completa das **178 faixas do Top 200 Global do Spotify** em 2026, cobrindo 104 artistas, 15 países e 34 gêneros musicais.

---

## 📊 O que este projeto explora

- **ETL completo**: normalização de países e gêneros inconsistentes, engenharia de features (streams por dia, variação percentual, viral score normalizado)
- **Análise Exploratória**: ranking de artistas, distribuição de streams, performance por gênero e representatividade geográfica
- **Análise Aprofundada**: longevidade vs. performance, correlação viral score × streams, power law do ranking, tendências por categoria e heatmap de correlações

---

## 🔍 Principais Insights

| # | Insight | Detalhe |
|---|---------|---------|
| 1 | **BTS domina o período** | 72.8M streams totais — mais que o dobro do 2º colocado |
| 2 | **EUA concentram 45% das faixas** | Hegemonia cultural clara no Top 200 Global |
| 3 | **77% das faixas em queda** | Mercado em fase de acomodação — poucos lançamentos em ascensão |
| 4 | **Faixas novas decaem rápido** | "New" entra com alto volume e queda acentuada nas primeiras semanas |
| 5 | **Viral Score × Streams: correlação 0.76** | Alta viralidade é forte indicador de streams, mas não garante tendência de alta |
| 6 | **Power law clara no ranking** | Top 10 gera streams médios ~4x maiores que posições acima de 50 |

---

## 📁 Estrutura do projeto

```
spotify-analysis/
│
├── notebook.ipynb                    # Análise completa com visualizações
├── analysis.py                       # Script Python equivalente (standalone)
├── spotify_global_trends_2026.csv    # Dataset original
├── insights.txt                      # Resumo dos insights gerados
│
└── img/
    ├── 01_top_artistas_streams.png
    ├── 02_distribuicao_streams.png
    ├── 03_streams_por_genero.png
    ├── 04_faixas_por_pais.png
    ├── 05_longevidade_vs_streams.png
    ├── 06_viral_vs_streams.png
    ├── 07_trend_por_longevidade.png
    ├── 08_posicao_vs_streams.png
    ├── 09_correlacao.png
    └── 10_boxplot_categorias.png
```

---

## 🗃️ Sobre o Dataset

| Campo | Descrição |
|-------|-----------|
| `track_name` | Nome da faixa |
| `artist_name` | Nome do artista |
| `streams` | Total de streams no período |
| `stream_change` | Variação de streams em relação ao período anterior |
| `7day` | Streams acumulados nos últimos 7 dias |
| `genre` | Gênero musical |
| `country` | País de origem do artista |
| `pos` | Posição no ranking |
| `days` | Dias consecutivos no chart |
| `viral_score` | Score de viralidade da plataforma |
| `trend` | Tendência atual (Rising / Falling) |
| `popularity_category` | Categoria de popularidade |
| `longevity` | Classificação de longevidade (New / Stable Hit / Evergreen) |

**Features criadas durante o ETL:**

| Feature | Descrição |
|---------|-----------|
| `streams_M` | Streams em milhões |
| `viral_score_M` | Viral score em milhões |
| `week_streams_M` | Streams semanais em milhões |
| `change_pct` | Variação percentual de streams |
| `streams_per_day` | Média diária de streams |
| `is_rising` | Flag binária de tendência de alta |
| `country_name` | Nome legível do país |

---

## 🛠️ Como rodar

```bash
# Clone o repositório
git clone https://github.com/lucc4sn/spotify-analysis.git
cd spotify-analysis

# Instale as dependências
pip install pandas numpy matplotlib seaborn

# Execute o script
python analysis.py

# Ou abra o notebook
jupyter notebook notebook.ipynb
```

---

## 📦 Dependências

```
pandas
numpy
matplotlib
seaborn
jupyter (para o notebook)
```

---

## 👤 Autor

**Luccas Nunes**  
Analista de Social Media & Dados Digitais  
[LinkedIn](https://www.linkedin.com/in/luccas-nunes/) · [GitHub](https://github.com/lucc4sn)
