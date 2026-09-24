import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Actividad económica del Ecuador",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# 2. PALETA DE COLORES - DIRECCIÓN TÉCNICA CIP
# ============================================================

# Azules DT
DT_AZUL_CLARO = "#4DB3FF"
DT_AZUL_2 = "#3D9BF9"
DT_AZUL = "#2472E2"
DT_AZUL_MEDIO = "#1E5EB8"
DT_AZUL_5 = "#184D96"
DT_AZUL_6 = "#133B74"
DT_AZUL_OSCURO = "#0D2A52"

# Amarillos / naranjas DT
DT_MARRON = "#A5690A"
DT_NARANJA_OSCURO = "#C18118"
DT_NARANJA_MEDIO = "#DD9A26"
DT_NARANJA = "#F8B229"
DT_AMARILLO = "#FED976"
DT_AMARILLO_CLARO = "#FFFFD4"
DT_AMARILLO_CLARO_2 = "#FFFFB2"

# Escala cálida / negativos
DT_NARANJA_ALERTA = "#FEB24C"
DT_NARANJA_ROJO = "#FD8D3C"
DT_ROJO_CLARO = "#F03B20"
DT_ROJO = "#E31A1C"

# Complementarios DT
DT_VERDE_CLARO = "#D9F0A3"
DT_VERDE_AGUA = "#99D8C9"
DT_TURQUESA_CLARO = "#7FCDBB"
DT_TURQUESA = "#41B6C4"
DT_CELESTE = "#43A2CA"

# Neutros
DT_BLANCO = "#FFFFFF"
DT_FONDO = "#F7F9FC"
DT_GRID = "#E7ECF2"
DT_TEXTO = "#263244"
DT_GRIS = "#6B7280"


# ============================================================
# 3. ESTILO GENERAL DEL DASHBOARD
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {DT_BLANCO};
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1550px;
    }}

    h1 {{
        color: {DT_AZUL_OSCURO};
        font-weight: 700;
    }}

    h2, h3 {{
        color: {DT_AZUL_6};
    }}

    p {{
        color: {DT_TEXTO};
    }}

    /* Tarjetas KPI */
    div[data-testid="stMetric"] {{
        background-color: {DT_BLANCO};
        border: 1px solid #E5EAF0;
        padding: 18px 20px;
        border-radius: 14px;
        box-shadow: 0px 4px 12px rgba(13, 42, 82, 0.06);
        min-height: 130px;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {DT_GRIS};
        font-weight: 600;
        font-size: 0.85rem;
    }}

    div[data-testid="stMetricValue"] {{
        color: {DT_AZUL_OSCURO};
        font-weight: 700;
    }}

    /* Tabs */
    button[data-baseweb="tab"] {{
        font-weight: 600;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {DT_AZUL_OSCURO};
        border-bottom-color: {DT_NARANJA};
    }}

    /* Selectores */
    div[data-baseweb="select"] > div {{
        border-radius: 9px;
    }}

    /* Separadores */
    hr {{
        border: none;
        border-top: 1px solid {DT_GRID};
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. CARGA DE DATOS
# ============================================================

archivo = "data/base_dashboard_actividad_economica_ecuador.xlsx"


@st.cache_data
def cargar_datos():

    pib = pd.read_excel(
        archivo,
        sheet_name="01_PIB_trimestral"
    )

    contribucion = pd.read_excel(
        archivo,
        sheet_name="02_Contribucion_PIB"
    )

    componentes = pd.read_excel(
        archivo,
        sheet_name="03_Componentes_PIB"
    )

    industrias = pd.read_excel(
        archivo,
        sheet_name="04_Industrias"
    )

    proyecciones = pd.read_excel(
        archivo,
        sheet_name="05_Proyecciones"
    )

    return (
        pib,
        contribucion,
        componentes,
        industrias,
        proyecciones
    )


pib, contribucion, componentes, industrias, proyecciones = cargar_datos()


# ============================================================
# 5. FUNCIONES AUXILIARES
# ============================================================

def formato_porcentaje(valor):

    if pd.isna(valor):
        return "N/D"

    return f"{valor:.1f}%"


def estilo_grafico(fig, titulo=None, altura=430):

    fig.update_layout(
        template="plotly_white",
        height=altura,
        margin=dict(
            l=25,
            r=25,
            t=65,
            b=35
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        legend_title_text="",
        hovermode="x unified",
        font=dict(
            family="Arial",
            size=12,
            color=DT_TEXTO
        ),
        paper_bgcolor=DT_BLANCO,
        plot_bgcolor=DT_BLANCO
    )

    if titulo:

        fig.update_layout(
            title=dict(
                text=titulo,
                font=dict(
                    size=17,
                    color=DT_AZUL_OSCURO
                ),
                x=0
            )
        )

    fig.update_xaxes(
        showgrid=False,
        linecolor=DT_GRID,
        tickfont=dict(color=DT_GRIS)
    )

    fig.update_yaxes(
        gridcolor=DT_GRID,
        zeroline=True,
        zerolinecolor="#AEB8C4",
        tickfont=dict(color=DT_GRIS)
    )

    return fig


def agregar_etiqueta_final(
    fig,
    x,
    y,
    texto,
    color
):

    if pd.isna(y):
        return

    fig.add_annotation(
        x=x,
        y=y,
        text=texto,
        showarrow=False,
        xshift=25,
        font=dict(
            color=color,
            size=11
        ),
        bgcolor=DT_BLANCO,
        bordercolor=color,
        borderwidth=1,
        borderpad=3
    )


# ============================================================
# 6. ENCABEZADO
# ============================================================

st.title("Actividad económica del Ecuador")

st.caption(
    "Dirección Técnica · Cámara de Industrias y Producción | "
    "Fuente: Banco Central del Ecuador"
)


# ============================================================
# 7. FILTROS GENERALES
# ============================================================

with st.container(border=True):

    st.markdown("**Filtros del panel**")

    col_filtro1, col_filtro2, col_filtro3 = st.columns(
        [1, 1, 2]
    )

    anios_disponibles = sorted(
        pib["anio"]
        .dropna()
        .astype(int)
        .unique()
    )

    anio_default = 2019

    if anio_default not in anios_disponibles:
        anio_default = anios_disponibles[0]

    with col_filtro1:

        anio_inicial = st.selectbox(
            "Mostrar información desde",
            options=anios_disponibles,
            index=anios_disponibles.index(anio_default)
        )

    with col_filtro2:

        ultimo_trimestre = (
            pib.sort_values("orden")
            .iloc[-1]["trimestre"]
        )

        st.markdown(
            f"""
            **Último período disponible**  
            {ultimo_trimestre}
            """
        )

    with col_filtro3:

        st.markdown(
            """
            **Criterio de las series**  
            Datos trimestrales ajustados de estacionalidad.
            """
        )


# ============================================================
# 8. PESTAÑAS
# ============================================================

(
    tab_general,
    tab_componentes,
    tab_industrias,
    tab_proyecciones,
    tab_datos
) = st.tabs(
    [
        "Visión general",
        "Componentes del PIB",
        "Industrias",
        "Proyecciones",
        "Datos"
    ]
)


# ============================================================
# 9. VISIÓN GENERAL
# ============================================================

with tab_general:

    st.markdown("### Panorama de la actividad económica")

    pib_filtrado = pib[
        pib["anio"] >= anio_inicial
    ].copy()

    pib_ultimo = (
        pib.dropna(
            subset=["var_interanual_pct"]
        )
        .sort_values("orden")
        .iloc[-1]
    )

    pib_trimestral_ultimo = (
        pib.dropna(
            subset=["var_intertrimestral_pct"]
        )
        .sort_values("orden")
        .iloc[-1]
    )

    vab_total = (
        industrias[
            industrias["industria"] == "VAB TOTAL"
        ]
        .sort_values("orden")
    )

    vab_ultimo = (
        vab_total.iloc[-1]
        if len(vab_total) > 0
        else None
    )

    proy_bce_2026 = proyecciones[
        (proyecciones["tipo"] == "Proyección Ecuador") &
        (proyecciones["anio"] == 2026) &
        (proyecciones["organismo"] == "BCE")
    ]

    proy_bce = (
        proy_bce_2026.iloc[0]["crecimiento_pib_pct"]
        if len(proy_bce_2026) > 0
        else None
    )


    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            label=f"PIB interanual · {pib_ultimo['trimestre']}",
            value=formato_porcentaje(
                pib_ultimo["var_interanual_pct"]
            )
        )

    with col2:

        st.metric(
            label=(
                f"PIB intertrimestral · "
                f"{pib_trimestral_ultimo['trimestre']}"
            ),
            value=formato_porcentaje(
                pib_trimestral_ultimo[
                    "var_intertrimestral_pct"
                ]
            )
        )

    with col3:

        if vab_ultimo is not None:

            st.metric(
                label=(
                    f"VAB interanual · "
                    f"{vab_ultimo['trimestre']}"
                ),
                value=formato_porcentaje(
                    vab_ultimo[
                        "var_interanual_pct"
                    ]
                )
            )

        else:

            st.metric(
                label="VAB interanual",
                value="N/D"
            )

    with col4:

        st.metric(
            label="Proyección PIB BCE · 2026",
            value=formato_porcentaje(proy_bce)
        )


    st.markdown("### Evolución del PIB")


    # --------------------------------------------------------
    # PIB
    # --------------------------------------------------------

    fig_pib = go.Figure()

    fig_pib.add_trace(
        go.Scatter(
            x=pib_filtrado["trimestre"],
            y=pib_filtrado["var_interanual_pct"],
            mode="lines+markers",
            name="Interanual",
            line=dict(
                color=DT_AZUL,
                width=3
            ),
            marker=dict(
                size=6,
                color=DT_AZUL
            )
        )
    )

    fig_pib.add_trace(
        go.Scatter(
            x=pib_filtrado["trimestre"],
            y=pib_filtrado["var_intertrimestral_pct"],
            mode="lines+markers",
            name="Intertrimestral",
            line=dict(
                color=DT_NARANJA,
                width=2.5
            ),
            marker=dict(
                size=5,
                color=DT_NARANJA
            )
        )
    )

    fig_pib.add_hline(
        y=0,
        line_width=1,
        line_color="#AEB8C4"
    )

    if len(pib_filtrado) > 0:

        ultimo = pib_filtrado.iloc[-1]

        agregar_etiqueta_final(
            fig_pib,
            ultimo["trimestre"],
            ultimo["var_interanual_pct"],
            formato_porcentaje(
                ultimo["var_interanual_pct"]
            ),
            DT_AZUL
        )

        agregar_etiqueta_final(
            fig_pib,
            ultimo["trimestre"],
            ultimo["var_intertrimestral_pct"],
            formato_porcentaje(
                ultimo["var_intertrimestral_pct"]
            ),
            DT_NARANJA_OSCURO
        )

    fig_pib.update_yaxes(
        title="Variación (%)",
        ticksuffix="%"
    )

    fig_pib = estilo_grafico(
        fig_pib,
        "Producto Interno Bruto"
    )

    st.plotly_chart(
        fig_pib,
        use_container_width=True
    )


    # --------------------------------------------------------
    # CONTRIBUCIÓN
    # --------------------------------------------------------

    st.markdown("### Motores del crecimiento")

    contrib_filtrada = contribucion[
        contribucion["anio"] >= anio_inicial
    ].copy()

    fig_contrib = go.Figure()

    series_contrib = [
        (
            "hogares_pp",
            "Consumo de hogares",
            DT_AZUL_CLARO
        ),
        (
            "gobierno_pp",
            "Gobierno",
            DT_AZUL_MEDIO
        ),
        (
            "fbkf_pp",
            "FBKF",
            DT_TURQUESA
        ),
        (
            "existencias_pp",
            "Variación de existencias",
            DT_AMARILLO
        ),
        (
            "exportaciones_pp",
            "Exportaciones",
            DT_AZUL
        ),
        (
            "importaciones_pp",
            "Importaciones",
            DT_NARANJA
        )
    ]

    for columna, nombre, color in series_contrib:

        fig_contrib.add_trace(
            go.Bar(
                x=contrib_filtrada["trimestre"],
                y=contrib_filtrada[columna],
                name=nombre,
                marker_color=color
            )
        )

    fig_contrib.add_trace(
        go.Scatter(
            x=contrib_filtrada["trimestre"],
            y=contrib_filtrada[
                "pib_var_interanual_pct"
            ],
            name="PIB",
            mode="lines+markers",
            line=dict(
                color=DT_AZUL_OSCURO,
                width=3
            ),
            marker=dict(
                size=6,
                color=DT_AZUL_OSCURO
            )
        )
    )

    fig_contrib.update_layout(
        barmode="relative"
    )

    fig_contrib.update_yaxes(
        title="Puntos porcentuales",
        ticksuffix="%"
    )

    fig_contrib = estilo_grafico(
        fig_contrib,
        "Contribución al crecimiento interanual"
    )

    st.plotly_chart(
        fig_contrib,
        use_container_width=True
    )


# ============================================================
# 10. COMPONENTES DEL PIB
# ============================================================

with tab_componentes:

    st.markdown("### Componentes del PIB")

    componentes_disponibles = [
        x
        for x in componentes[
            "componente"
        ].dropna().unique()
        if x != "PIB"
    ]

    componente_seleccionado = st.selectbox(
        "Selecciona un componente",
        componentes_disponibles
    )

    componente_df = componentes[
        (
            componentes["componente"]
            == componente_seleccionado
        ) &
        (
            componentes["anio"]
            >= anio_inicial
        )
    ].copy()


    # --------------------------------------------------------
    # GRÁFICO PRINCIPAL
    # --------------------------------------------------------

    fig_comp = go.Figure()

    fig_comp.add_trace(
        go.Scatter(
            x=componente_df["trimestre"],
            y=componente_df[
                "var_interanual_pct"
            ],
            mode="lines+markers",
            name="Interanual",
            line=dict(
                color=DT_AZUL,
                width=3
            ),
            marker=dict(
                color=DT_AZUL,
                size=6
            )
        )
    )

    fig_comp.add_trace(
        go.Scatter(
            x=componente_df["trimestre"],
            y=componente_df[
                "var_intertrimestral_pct"
            ],
            mode="lines+markers",
            name="Intertrimestral",
            line=dict(
                color=DT_NARANJA,
                width=2.5
            ),
            marker=dict(
                color=DT_NARANJA,
                size=5
            )
        )
    )

    fig_comp.add_hline(
        y=0,
        line_width=1,
        line_color="#AEB8C4"
    )

    if len(componente_df) > 0:

        ultimo = componente_df.iloc[-1]

        agregar_etiqueta_final(
            fig_comp,
            ultimo["trimestre"],
            ultimo["var_interanual_pct"],
            formato_porcentaje(
                ultimo["var_interanual_pct"]
            ),
            DT_AZUL
        )

        agregar_etiqueta_final(
            fig_comp,
            ultimo["trimestre"],
            ultimo["var_intertrimestral_pct"],
            formato_porcentaje(
                ultimo[
                    "var_intertrimestral_pct"
                ]
            ),
            DT_NARANJA_OSCURO
        )

    fig_comp.update_yaxes(
        title="Variación (%)",
        ticksuffix="%"
    )

    fig_comp = estilo_grafico(
        fig_comp,
        componente_seleccionado
    )

    st.plotly_chart(
        fig_comp,
        use_container_width=True
    )


    # --------------------------------------------------------
    # GRÁFICOS RESUMEN
    # --------------------------------------------------------

    st.markdown(
        "### Evolución de los principales componentes"
    )

    componentes_graficos = [
        "Gasto de consumo final de hogares",
        "Gasto de consumo final del Gobierno General",
        "FBKF",
        "Exportaciones de bienes y servicios",
        "Importaciones de bienes y servicios"
    ]

    for i in range(
        0,
        len(componentes_graficos),
        2
    ):

        columnas = st.columns(2)

        for j in range(2):

            posicion = i + j

            if posicion >= len(
                componentes_graficos
            ):
                continue

            comp = componentes_graficos[
                posicion
            ]

            df_comp = componentes[
                (
                    componentes["componente"]
                    == comp
                ) &
                (
                    componentes["anio"]
                    >= anio_inicial
                )
            ].copy()

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df_comp["trimestre"],
                    y=df_comp[
                        "var_interanual_pct"
                    ],
                    name="Interanual",
                    mode="lines+markers",
                    line=dict(
                        color=DT_AZUL,
                        width=2.5
                    ),
                    marker=dict(
                        size=4
                    )
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=df_comp["trimestre"],
                    y=df_comp[
                        "var_intertrimestral_pct"
                    ],
                    name="Intertrimestral",
                    mode="lines+markers",
                    line=dict(
                        color=DT_NARANJA,
                        width=2
                    ),
                    marker=dict(
                        size=4
                    )
                )
            )

            fig.add_hline(
                y=0,
                line_width=1,
                line_color="#C8CFD8"
            )

            fig.update_yaxes(
                ticksuffix="%"
            )

            fig = estilo_grafico(
                fig,
                comp,
                altura=380
            )

            with columnas[j]:

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


# ============================================================
# 11. INDUSTRIAS
# ============================================================

with tab_industrias:

    st.markdown(
        "### Actividad económica por industria"
    )

    tipo_variacion = st.radio(
        "Indicador",
        [
            "Variación interanual",
            "Variación intertrimestral"
        ],
        horizontal=True
    )

    if (
        tipo_variacion
        == "Variación interanual"
    ):

        variable_industria = (
            "var_interanual_pct"
        )

    else:

        variable_industria = (
            "var_intertrimestral_pct"
        )


    industrias_sin_total = industrias[
        industrias["industria"]
        != "VAB TOTAL"
    ].copy()

    industrias_filtradas = (
        industrias_sin_total[
            industrias_sin_total["anio"]
            >= anio_inicial
        ]
        .copy()
    )

    if len(industrias_filtradas) == 0:
        industrias_filtradas = (
            industrias_sin_total.copy()
        )

    ultimo_periodo_orden = (
        industrias_sin_total["orden"].max()
    )

    ultimo_periodo = (
        industrias_sin_total[
            industrias_sin_total["orden"]
            == ultimo_periodo_orden
        ]
        .copy()
    )


    # --------------------------------------------------------
    # RANKING ÚLTIMO TRIMESTRE
    # --------------------------------------------------------

    periodo_nombre = (
        ultimo_periodo[
            "trimestre"
        ].iloc[0]
    )

    st.markdown(
        f"### Ranking de industrias · {periodo_nombre}"
    )

    ranking = (
        ultimo_periodo
        .dropna(
            subset=[
                variable_industria
            ]
        )
        .sort_values(
            variable_industria,
            ascending=True
        )
    )

    colores_ranking = [
        DT_AZUL
        if valor >= 0
        else DT_ROJO
        for valor in ranking[
            variable_industria
        ]
    ]

    fig_rank = go.Figure()

    fig_rank.add_trace(
        go.Bar(
            x=ranking[
                variable_industria
            ],
            y=ranking["industria"],
            orientation="h",
            marker_color=colores_ranking,
            text=[
                formato_porcentaje(x)
                for x in ranking[
                    variable_industria
                ]
            ],
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Variación: %{x:.1f}%"
                "<extra></extra>"
            )
        )
    )

    fig_rank.add_vline(
        x=0,
        line_width=1,
        line_color="#AEB8C4"
    )

    fig_rank.update_xaxes(
        title="Variación (%)",
        ticksuffix="%"
    )

    fig_rank.update_layout(
        showlegend=False
    )

    fig_rank = estilo_grafico(
        fig_rank,
        altura=720
    )

    st.plotly_chart(
        fig_rank,
        use_container_width=True
    )


    # --------------------------------------------------------
    # HEATMAP
    # --------------------------------------------------------

    st.markdown(
        "### Evolución por industria"
    )

    heatmap_data = (
        industrias_filtradas
        .pivot_table(
            index="industria",
            columns="trimestre",
            values=variable_industria,
            aggfunc="first"
        )
    )

    orden_periodos = (
        industrias_filtradas[
            [
                "trimestre",
                "orden"
            ]
        ]
        .drop_duplicates()
        .sort_values("orden")[
            "trimestre"
        ]
        .tolist()
    )

    columnas_heatmap = [
        periodo
        for periodo in orden_periodos
        if periodo
        in heatmap_data.columns
    ]

    heatmap_data = (
        heatmap_data[
            columnas_heatmap
        ]
    )

    fig_heat = go.Figure(
        data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            zmid=0,
            colorscale=[
                [0.00, DT_ROJO],
                [0.25, DT_NARANJA_ROJO],
                [0.45, DT_AMARILLO],
                [0.50, DT_BLANCO],
                [0.70, DT_TURQUESA_CLARO],
                [1.00, DT_AZUL]
            ],
            colorbar=dict(
                title="%"
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "%{x}<br>"
                "%{z:.1f}%"
                "<extra></extra>"
            )
        )
    )

    fig_heat.update_layout(
        height=720,
        margin=dict(
            l=30,
            r=30,
            t=20,
            b=30
        ),
        font=dict(
            family="Arial",
            color=DT_TEXTO
        ),
        paper_bgcolor=DT_BLANCO
    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )


# ============================================================
# 12. PROYECCIONES
# ============================================================

with tab_proyecciones:

    st.markdown(
        "### Perspectivas de crecimiento económico"
    )


    # --------------------------------------------------------
    # ECUADOR
    # --------------------------------------------------------

    historico_ec = proyecciones[
        (
            proyecciones["tipo"]
            == "Histórico"
        ) &
        (
            proyecciones["pais"]
            == "Ecuador"
        )
    ].copy()

    proy_ec = proyecciones[
        proyecciones["tipo"]
        == "Proyección Ecuador"
    ].copy()

    fig_proy = go.Figure()

    fig_proy.add_trace(
        go.Scatter(
            x=historico_ec["anio"],
            y=historico_ec[
                "crecimiento_pib_pct"
            ],
            mode="lines+markers",
            name="Histórico BCE",
            line=dict(
                color=DT_AZUL_OSCURO,
                width=3
            ),
            marker=dict(
                size=7,
                color=DT_AZUL_OSCURO
            )
        )
    )

    organismos = [
        "BCE",
        "FMI",
        "Banco Mundial",
        "CEPAL"
    ]

    colores_organismos = {
        "BCE": DT_AZUL,
        "FMI": DT_ROJO,
        "Banco Mundial": DT_NARANJA,
        "CEPAL": DT_TURQUESA
    }

    for organismo in organismos:

        df_org = proy_ec[
            proy_ec["organismo"]
            == organismo
        ].sort_values("anio")

        if len(df_org) > 0:

            fig_proy.add_trace(
                go.Scatter(
                    x=df_org["anio"],
                    y=df_org[
                        "crecimiento_pib_pct"
                    ],
                    mode="lines+markers",
                    name=organismo,
                    line=dict(
                        dash="dash",
                        color=colores_organismos[
                            organismo
                        ],
                        width=2.5
                    ),
                    marker=dict(
                        size=7
                    )
                )
            )

    fig_proy.add_hline(
        y=0,
        line_width=1,
        line_color="#AEB8C4"
    )

    fig_proy.update_yaxes(
        title="Crecimiento (%)",
        ticksuffix="%"
    )

    fig_proy.update_xaxes(
        dtick=1
    )

    fig_proy = estilo_grafico(
        fig_proy,
        "Crecimiento histórico y proyecciones de Ecuador"
    )

    st.plotly_chart(
        fig_proy,
        use_container_width=True
    )


    # --------------------------------------------------------
    # COMPARATIVO REGIONAL
    # --------------------------------------------------------

    st.markdown(
        "### Comparativo regional 2026"
    )

    regional = proyecciones[
        (
            proyecciones["tipo"]
            == "Comparativo regional"
        ) &
        (
            proyecciones["anio"]
            == 2026
        )
    ].copy()

    fig_regional = px.bar(
        regional,
        x="pais",
        y="crecimiento_pib_pct",
        color="organismo",
        barmode="group",
        color_discrete_map={
            "Banco Mundial": DT_NARANJA,
            "CEPAL": DT_TURQUESA,
            "FMI": DT_AZUL
        },
        labels={
            "pais": "",
            "crecimiento_pib_pct":
                "Crecimiento (%)",
            "organismo":
                "Organismo"
        },
        text_auto=".1f"
    )

    fig_regional.update_traces(
        texttemplate="%{y:.1f}%",
        textposition="outside"
    )

    fig_regional.update_yaxes(
        ticksuffix="%"
    )

    fig_regional = estilo_grafico(
        fig_regional,
        "Proyecciones de crecimiento económico · 2026"
    )

    st.plotly_chart(
        fig_regional,
        use_container_width=True
    )


# ============================================================
# 13. DATOS
# ============================================================

with tab_datos:

    st.markdown(
        "### Base de datos"
    )

    st.caption(
        "Consulta y descarga de las series utilizadas "
        "en el dashboard."
    )

    base_seleccionada = st.selectbox(
        "Selecciona una tabla",
        [
            "PIB trimestral",
            "Contribución al crecimiento",
            "Componentes del PIB",
            "Industrias",
            "Proyecciones"
        ]
    )

    if (
        base_seleccionada
        == "PIB trimestral"
    ):

        tabla = pib

    elif (
        base_seleccionada
        == "Contribución al crecimiento"
    ):

        tabla = contribucion

    elif (
        base_seleccionada
        == "Componentes del PIB"
    ):

        tabla = componentes

    elif (
        base_seleccionada
        == "Industrias"
    ):

        tabla = industrias

    else:

        tabla = proyecciones


    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True
    )


    csv = tabla.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="Descargar datos en CSV",
        data=csv,
        file_name=(
            "actividad_economica_ecuador.csv"
        ),
        mime="text/csv"
    )


# ============================================================
# 14. PIE DE PÁGINA
# ============================================================

st.markdown("---")

st.caption(
    "Fuente: Banco Central del Ecuador. "
    "Elaboración: Dirección Técnica - "
    "Cámara de Industrias y Producción."
)
