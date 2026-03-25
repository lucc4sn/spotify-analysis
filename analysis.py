'''
Análise de Tendências Globais do Spotify — 2026
Dataset: spotify_global_trends_2026.csv
Autor: Luccas Nunes
'''

import pandas as pd 
import numpy as np 
import matplotlib .pyplot as plt 
import matplotlib .ticker as mticker 
import seaborn as sns 
import warnings 
warnings .filterwarnings ('ignore')

# ─── Estilo global ────────────────────────────────────────────────────────────
plt .rcParams .update ({
'figure.facecolor':'#0D0D1A',
'axes.facecolor':'#12122A',
'axes.edgecolor':'#2A2A4A',
'axes.labelcolor':'#E2E8F0',
'xtick.color':'#8B9CC8',
'ytick.color':'#8B9CC8',
'text.color':'#E2E8F0',
'grid.color':'#1E1E3A',
'grid.linestyle':'--',
'grid.alpha':0.5 ,
'font.family':'sans-serif',
'font.size':11 ,
})

PURPLE ='#8B5CF6'
CYAN ='#06B6D4'
AMBER ='#F59E0B'
ROSE ='#F43F5E'
SLATE ='#8B9CC8'
OUT ='img/'

# ══════════════════════════════════════════════════════════════════════════════
# 1. ETL
# ══════════════════════════════════════════════════════════════════════════════
print ('── ETL ──────────────────────────────────────────')

df =pd .read_csv ('spotify_global_trends_2026.csv')
print (f"Linhas brutas : {len (df ):,}")

# Normalização de países (valores inconsistentes → código padrão)
country_fix ={
'Florida':'US',
'Culiacán':'MX',
'Monterrey':'MX',
'England':'GB',
}
df ['country']=df ['country'].replace (country_fix )

# Mapa de nomes legíveis para países
country_names ={
'US':'Estados Unidos','GB':'Reino Unido','KR':'Coreia do Sul',
'CA':'Canadá','PR':'Porto Rico','MX':'México',
'AU':'Austrália','CO':'Colômbia','SE':'Suécia',
'JM':'Jamaica','IT':'Itália','JP':'Japão',
'FR':'França','IE':'Irlanda','NO':'Noruega',
}
df ['country_name']=df ['country'].map (country_names ).fillna (df ['country'])

# Normalização de gêneros (agrupa categorias espúrias)
genre_fix ={
'Billboard Hot 100':'Pop',
'Offizielle Charts':'Pop',
'Special Purpose Artist':'Other',
'Falcom':'Other',
'Dolby Atmos':'Other',
'Toronto':'Hip Hop',
}
df ['genre']=df ['genre'].replace (genre_fix )

# Features derivadas
df ['streams_M']=df ['streams']/1_000_000 
df ['viral_score_M']=df ['viral_score']/1_000_000 
df ['week_streams_M']=df ['7day']/1_000_000 
df ['change_pct']=df ['stream_change']/(df ['streams']-df ['stream_change'])*100 
df ['streams_per_day']=df ['streams']/df ['days'].clip (lower =1 )
df ['is_rising']=(df ['trend']=='Rising').astype (int )

print (f"Linhas após limpeza  : {len (df ):,}")
print (f"Artistas únicos      : {df ['artist_name'].nunique ()}")
print (f"Faixas únicas        : {df ['track_name'].nunique ()}")
print (f"Gêneros              : {df ['genre'].nunique ()}")
print (f"Países               : {df ['country'].nunique ()}")
print (f"Streams médios       : {df ['streams_M'].mean ():.2f}M")
print (f"Streams máximos      : {df ['streams_M'].max ():.2f}M")
print (f"% faixas em queda    : {(df ['trend']=='Falling').mean ()*100 :.1f}%")


# ══════════════════════════════════════════════════════════════════════════════
# 2. ANÁLISE EXPLORATÓRIA
# ══════════════════════════════════════════════════════════════════════════════
print ('\n── Análise Exploratória ─────────────────────────')

# ── 2a. Top 15 artistas por streams totais ────────────────────────────────────
top_artists =(
df .groupby ('artist_name')['streams_M']
.sum ()
.sort_values (ascending =True )
.tail (15 )
)

fig ,ax =plt .subplots (figsize =(10 ,7 ))
colors =[PURPLE if v ==top_artists .max ()else (CYAN if v >=top_artists .quantile (0.75 )else SLATE )
for v in top_artists .values ]
bars =ax .barh (top_artists .index ,top_artists .values ,color =colors ,height =0.65 )
ax .set_title ('Top 15 Artistas por Streams Totais',fontsize =14 ,fontweight ='bold',pad =12 )
ax .set_xlabel ('Streams (milhões)')
ax .grid (axis ='x')
for bar in bars :
    ax .text (bar .get_width ()+0.5 ,bar .get_y ()+bar .get_height ()/2 ,
    f"{bar .get_width ():.1f}M",va ='center',fontsize =9 ,color =SLATE )
fig .tight_layout ()
fig .savefig (f"{OUT }01_top_artistas_streams.png",dpi =150 ,bbox_inches ='tight')
plt .close ()
print ('✓ 01_top_artistas_streams.png')

# ── 2b. Distribuição de streams ───────────────────────────────────────────────
fig ,axes =plt .subplots (1 ,2 ,figsize =(13 ,5 ))

axes [0 ].hist (df ['streams_M'],bins =35 ,color =PURPLE ,alpha =0.85 ,edgecolor ='none')
axes [0 ].axvline (df ['streams_M'].mean (),color ='white',linestyle ='--',linewidth =1.2 ,
label =f"Média: {df ['streams_M'].mean ():.2f}M")
axes [0 ].axvline (df ['streams_M'].median (),color =CYAN ,linestyle ='--',linewidth =1.2 ,
label =f"Mediana: {df ['streams_M'].median ():.2f}M")
axes [0 ].set_title ('Distribuição de Streams',fontsize =12 ,fontweight ='bold')
axes [0 ].set_xlabel ('Streams (M)');axes [0 ].set_ylabel ('Frequência')
axes [0 ].legend (fontsize =9 );axes [0 ].grid (axis ='y')

axes [1 ].hist (np .log1p (df ['streams']),bins =35 ,color =CYAN ,alpha =0.85 ,edgecolor ='none')
axes [1 ].set_title ('Distribuição de Streams (escala log)',fontsize =12 ,fontweight ='bold')
axes [1 ].set_xlabel ('log(Streams)');axes [1 ].set_ylabel ('Frequência')
axes [1 ].grid (axis ='y')

fig .suptitle ('Streams nas Top 200 Globais',fontsize =13 ,y =1.02 )
fig .tight_layout ()
fig .savefig (f"{OUT }02_distribuicao_streams.png",dpi =150 ,bbox_inches ='tight')
plt .close ()
print ('✓ 02_distribuicao_streams.png')

# ── 2c. Streams por gênero ────────────────────────────────────────────────────
genre_streams =(
df .groupby ('genre')['streams_M']
.agg (['sum','mean','count'])
.sort_values ('sum',ascending =True )
.tail (12 )
)

fig ,axes =plt .subplots (1 ,2 ,figsize =(14 ,6 ))

bars =axes [0 ].barh (genre_streams .index ,genre_streams ['sum'],color =PURPLE ,alpha =0.85 ,height =0.65 )
axes [0 ].set_title ('Streams Totais por Gênero',fontsize =12 ,fontweight ='bold')
axes [0 ].set_xlabel ('Streams (M)');axes [0 ].grid (axis ='x')
for bar in bars :
    axes [0 ].text (bar .get_width ()+0.3 ,bar .get_y ()+bar .get_height ()/2 ,
    f"{bar .get_width ():.1f}M",va ='center',fontsize =9 ,color =SLATE )

genre_avg =df .groupby ('genre')['streams_M'].mean ().sort_values (ascending =True ).tail (12 )
bars2 =axes [1 ].barh (genre_avg .index ,genre_avg .values ,color =CYAN ,alpha =0.85 ,height =0.65 )
axes [1 ].set_title ('Média de Streams por Faixa (por Gênero)',fontsize =12 ,fontweight ='bold')
axes [1 ].set_xlabel ('Streams médios (M)');axes [1 ].grid (axis ='x')
for bar in bars2 :
    axes [1 ].text (bar .get_width ()+0.1 ,bar .get_y ()+bar .get_height ()/2 ,
    f"{bar .get_width ():.2f}M",va ='center',fontsize =9 ,color =SLATE )

fig .suptitle ('Performance por Gênero Musical',fontsize =13 ,y =1.02 )
fig .tight_layout ()
fig .savefig (f"{OUT }03_streams_por_genero.png",dpi =150 ,bbox_inches ='tight')
plt .close ()
print ('✓ 03_streams_por_genero.png')

# ── 2d. Faixas por país de origem ────────────────────────────────────────────
country_count =(
df .groupby ('country_name')['track_name']
.count ()
.sort_values (ascending =True )
)

fig ,ax =plt .subplots (figsize =(10 ,6 ))
colors_c =[PURPLE if v ==country_count .max ()else (CYAN if v >=country_count .quantile (0.75 )else SLATE )
for v in country_count .values ]
bars =ax .barh (country_count .index ,country_count .values ,color =colors_c ,height =0.65 )
ax .set_title ('Faixas no Top 200 por País de Origem do Artista',fontsize =13 ,fontweight ='bold',pad =12 )
ax .set_xlabel ('Número de faixas');ax .grid (axis ='x')
for bar in bars :
    ax .text (bar .get_width ()+0.3 ,bar .get_y ()+bar .get_height ()/2 ,
    f"{int (bar .get_width ())}",va ='center',fontsize =9 ,color =SLATE )
fig .tight_layout ()
fig .savefig (f"{OUT }04_faixas_por_pais.png",dpi =150 ,bbox_inches ='tight')
plt .close ()
print ('✓ 04_faixas_por_pais.png')


# ══════════════════════════════════════════════════════════════════════════════
# 3. ANÁLISE APROFUNDADA
# ══════════════════════════════════════════════════════════════════════════════
print ('\n── Análise Aprofundada ──────────────────────────')

# ── 3a. Longevidade × Streams ────────────────────────────────────────────────
fig ,ax =plt .subplots (figsize =(10 ,6 ))
longevity_order =['New','Stable Hit','Evergreen']
palette ={'New':ROSE ,'Stable Hit':AMBER ,'Evergreen':PURPLE }

for lng in longevity_order :
    subset =df [df ['longevity']==lng ]
    ax .scatter (subset ['days'],subset ['streams_M'],
    color =palette [lng ],alpha =0.7 ,s =50 ,label =lng ,edgecolors ='none')

ax .set_title ('Longevidade × Streams\n(dias no chart vs. streams totais)',fontsize =13 ,fontweight ='bold',pad =12 )
ax .set_xlabel ('Dias no chart');ax .set_ylabel ('Streams (M)')
ax .legend (title ='Longevidade');ax .grid (True )
fig .tight_layout ()
fig .savefig (f"{OUT }05_longevidade_vs_streams.png",dpi =150 ,bbox_inches ='tight')
plt .close ()
print ('✓ 05_longevidade_vs_streams.png')

# ── 3b. Viral Score × Streams (por trend) ────────────────────────────────────
fig ,ax =plt .subplots (figsize =(10 ,7 ))
for trend ,color in [('Rising',CYAN ),('Falling',ROSE )]:
    subset =df [df ['trend']==trend ]
    ax .scatter (subset ['viral_score_M'],subset ['streams_M'],
    color =color ,alpha =0.7 ,s =55 ,label =trend ,edgecolors ='none')

ax .set_title ('Viral Score × Streams (por Tendência)',fontsize =13 ,fontweight ='bold',pad =12 )
ax .set_xlabel ('Viral Score (M)');ax .set_ylabel ('Streams (M)')
ax .legend (title ='Tendência');ax .grid (True )

# Linha de tendência geral
z =np .polyfit (df ['viral_score_M'],df ['streams_M'],1 )
p =np .poly1d (z )
x_line =np .linspace (df ['viral_score_M'].min (),df ['viral_score_M'].max (),100 )
ax .plot (x_line ,p (x_line ),color ='white',linewidth =1.2 ,linestyle ='--',alpha =0.5 ,label ='Tendência geral')
ax .legend (title ='Tendência')
fig .tight_layout ()
fig .savefig (f"{OUT }06_viral_vs_streams.png",dpi =150 ,bbox_inches ='tight')
plt .close ()
print ('✓ 06_viral_vs_streams.png')

# ── 3c. Distribuição de trend por longevidade (stacked bar) ──────────────────
pivot =(
df .groupby (['longevity','trend'])
.size ()
.unstack (fill_value =0 )
)
pivot_pct =pivot .div (pivot .sum (axis =1 ),axis =0 )*100 
pivot_pct =pivot_pct .reindex (['New','Stable Hit','Evergreen'])

fig ,ax =plt .subplots (figsize =(9 ,5 ))
pivot_pct .plot (kind ='bar',stacked =True ,ax =ax ,
color =[ROSE ,CYAN ],edgecolor ='none',width =0.5 )
ax .set_title ('Distribuição de Tendência por Longevidade (%)',fontsize =13 ,fontweight ='bold',pad =12 )
ax .set_xlabel ('');ax .set_ylabel ('Proporção (%)')
ax .set_xticklabels (pivot_pct .index ,rotation =0 )
ax .legend (title ='Tendência',loc ='upper right')
ax .grid (axis ='y')

for i ,(idx ,row )in enumerate (pivot_pct .iterrows ()):
    cumulative =0 
    for col ,color in zip (pivot_pct .columns ,[ROSE ,CYAN ]):
        val =row [col ]
        if val >5 :
            ax .text (i ,cumulative +val /2 ,f"{val :.0f}%",
            ha ='center',va ='center',fontsize =10 ,fontweight ='bold',
            color ='#0D0D1A')
        cumulative +=val 

fig .tight_layout ()
fig .savefig (f"{OUT }07_trend_por_longevidade.png",dpi =150 ,bbox_inches ='tight')
plt .close ()
print ('✓ 07_trend_por_longevidade.png')

# ── 3d. Posição no ranking × Streams (curva de power law) ────────────────────
fig ,ax =plt .subplots (figsize =(11 ,6 ))
sc =ax .scatter (df ['pos'],df ['streams_M'],
c =df ['viral_score_M'],cmap ='plasma',
alpha =0.7 ,s =45 ,edgecolors ='none')
cbar =fig .colorbar (sc ,ax =ax )
cbar .set_label ('Viral Score (M)',color ='#E2E8F0')
cbar .ax .yaxis .set_tick_params (color ='#E2E8F0')
plt .setp (cbar .ax .yaxis .get_ticklabels (),color ='#E2E8F0')

ax .set_title ('Posição no Ranking × Streams\n(colorido por Viral Score)',fontsize =13 ,fontweight ='bold',pad =12 )
ax .set_xlabel ('Posição no ranking');ax .set_ylabel ('Streams (M)');ax .grid (True )
fig .tight_layout ()
fig .savefig (f"{OUT }08_posicao_vs_streams.png",dpi =150 ,bbox_inches ='tight')
plt .close ()
print ('✓ 08_posicao_vs_streams.png')

# ── 3e. Correlação entre variáveis numéricas ──────────────────────────────────
corr_cols =['streams_M','stream_change','week_streams_M','days',
'viral_score_M','pos','streams_per_day']
corr =df [corr_cols ].corr ()

col_labels ={
'streams_M':'Streams',
'stream_change':'Δ Streams',
'week_streams_M':'Streams 7d',
'days':'Dias no chart',
'viral_score_M':'Viral Score',
'pos':'Posição',
'streams_per_day':'Streams/dia',
}

fig ,ax =plt .subplots (figsize =(9 ,7 ))
mask =np .triu (np .ones_like (corr ,dtype =bool ))
cmap =sns .diverging_palette (260 ,10 ,as_cmap =True )
sns .heatmap (corr ,mask =mask ,cmap =cmap ,center =0 ,annot =True ,fmt ='.2f',
linewidths =0.5 ,linecolor ='#0D0D1A',ax =ax ,
annot_kws ={'size':10 },cbar_kws ={'shrink':0.8 })
ax .set_title ('Correlação entre Variáveis',fontsize =13 ,fontweight ='bold',pad =12 )
ax .set_xticklabels ([col_labels .get (c ,c )for c in corr .columns ],rotation =35 ,ha ='right')
ax .set_yticklabels ([col_labels .get (c ,c )for c in corr .index ],rotation =0 )
fig .tight_layout ()
fig .savefig (f"{OUT }09_correlacao.png",dpi =150 ,bbox_inches ='tight')
plt .close ()
print ('✓ 09_correlacao.png')

# ── 3f. Boxplot de streams por categoria de popularidade e longevidade ────────
fig ,axes =plt .subplots (1 ,2 ,figsize =(13 ,6 ))

order_lon =['New','Stable Hit','Evergreen']
palette_lon ={'New':ROSE ,'Stable Hit':AMBER ,'Evergreen':PURPLE }

for i ,(col ,title ,order ,palette )in enumerate ([
('longevity','Streams por Longevidade',order_lon ,palette_lon ),
('popularity_category','Streams por Categoria de Popularidade',None ,{k :CYAN for k in df ['popularity_category'].unique ()}),
]):
    data_groups =df .groupby (col )['streams_M'].apply (list )
    if order :
        data_groups =data_groups .reindex (order )
    keys =list (data_groups .index )
    values =[data_groups [k ]for k in keys ]
    bp =axes [i ].boxplot (values ,patch_artist =True ,widths =0.45 ,
    medianprops ={'color':'white','linewidth':2 })
    for patch ,key in zip (bp ['boxes'],keys ):
        patch .set_facecolor (palette .get (key ,SLATE ))
        patch .set_alpha (0.8 )
    for element in ['whiskers','caps','fliers']:
        for item in bp [element ]:
            item .set (color =SLATE ,linewidth =1 )
    axes [i ].set_xticklabels (keys ,rotation =15 ,ha ='right')
    axes [i ].set_title (title ,fontsize =12 ,fontweight ='bold')
    axes [i ].set_ylabel ('Streams (M)')
    axes [i ].grid (axis ='y')

fig .suptitle ('Distribuição de Streams por Categorias',fontsize =13 ,y =1.02 )
fig .tight_layout ()
fig .savefig (f"{OUT }10_boxplot_categorias.png",dpi =150 ,bbox_inches ='tight')
plt .close ()
print ('✓ 10_boxplot_categorias.png')

# ══════════════════════════════════════════════════════════════════════════════
# 4. SUMÁRIO DE INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
print ('\n── Sumário de Insights ──────────────────────────')

top_artist =df .groupby ('artist_name')['streams_M'].sum ().idxmax ()
top_artist_val =df .groupby ('artist_name')['streams_M'].sum ().max ()
top_genre =df .groupby ('genre')['streams_M'].sum ().idxmax ()
top_country =df .groupby ('country_name')['track_name'].count ().idxmax ()
pct_falling =(df ['trend']=='Falling').mean ()*100 
pct_evergreen =(df ['longevity']=='Evergreen').mean ()*100 
avg_streams =df ['streams_M'].mean ()
corr_viral =df [['viral_score_M','streams_M']].corr ().iloc [0 ,1 ]

insights =f"""
INSIGHTS PRINCIPAIS
═══════════════════

1. DOMÍNIO DE ARTISTAS
   • Artista com mais streams : {top_artist } ({top_artist_val :.1f}M streams totais)
   • EUA dominam o chart com {df [df ['country']=='US']['track_name'].count ()} faixas no Top 200

2. GÊNEROS
   • Gênero mais streamado (total): {top_genre }
   • K-Pop concentra alto volume por faixa — média acima do geral

3. TENDÊNCIAS
   • {pct_falling :.1f}% das faixas estão em queda (Falling)
   • Apenas {100 -pct_falling :.1f}% em ascensão (Rising) — mercado em fase de acomodação

4. LONGEVIDADE
   • {pct_evergreen :.1f}% das faixas são classificadas como Evergreen
   • Faixas "New" entram com alto volume mas decaem rapidamente

5. VIRAL SCORE
   • Correlação viral score × streams: {corr_viral :.2f}
   • Faixas em alta (Rising) têm viral scores consistentemente maiores

6. POWER LAW
   • O top 10 do ranking acumula streams muito superiores às posições 50+
   • Curva clássica de cauda longa: poucos artistas concentram a maior parte dos streams
"""
print (insights )
with open ('insights.txt','w', encoding='utf-8')as f :
    f .write (insights )

print ('\n✅ Análise concluída. Todos os gráficos salvos em /img/')