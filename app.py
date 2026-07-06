import streamlit as st
import pandas as pd
import plotly.express as px

# Konfiguracja strony
st.set_page_config(
    page_title="Analiza snu",
    page_icon="😴",
    layout="wide"
)

# Wczytanie danych z cachowaniem.
@st.cache_data
def wczytaj_dane():
    df = pd.read_csv("sleep_clean.csv")
    return df

df = wczytaj_dane()

# Filtry w panelu bocznym
st.sidebar.header("Filtry")

# Filtr 1: kraj
kraje = sorted(df["country"].unique())
wybrane_kraje = st.sidebar.multiselect(
    "Kraj",
    options=kraje,
    default=kraje
)

# Filtr 2: zawód
zawody = sorted(df["occupation"].unique())
wybrane_zawody = st.sidebar.multiselect(
    "Zawód",
    options=zawody,
    default=zawody
)

# Filtr 3: przedział wiekowy
wiek_min = int(df["age"].min())
wiek_max = int(df["age"].max())
zakres_wieku = st.sidebar.slider(
    "Wiek",
    min_value=wiek_min,
    max_value=wiek_max,
    value=(wiek_min, wiek_max)
)

# Filtr 4: chronotyp
chronotypy = ["Wszystkie"] + sorted(df["chronotype"].unique())
wybrany_chronotyp = st.sidebar.selectbox("Chronotyp", options=chronotypy)

# Filtrowanie danych
df_filtered = df[
    (df["country"].isin(wybrane_kraje)) &
    (df["occupation"].isin(wybrane_zawody)) &
    (df["age"].between(zakres_wieku[0], zakres_wieku[1]))
]

if wybrany_chronotyp != "Wszystkie":
    df_filtered = df_filtered[df_filtered["chronotype"] == wybrany_chronotyp]


# KPI
st.subheader("Kluczowe wskaźniki")

# Zabezpieczenie przed brakiem danych po filtrach
if len(df_filtered) == 0:
    st.warning("Brak danych dla wybranych filtrów. Zmień ustawienia w panelu bocznym.")
    st.stop()

# Ustawienie kolumn dla KPI
kol1, kol2, kol3, kol4 = st.columns(4)

kol1.metric(
    "Liczba osób",
    f"{len(df_filtered):,}".replace(",", " ")
)
kol2.metric(
    "Średnia długość snu",
    f"{df_filtered['sleep_duration_hrs'].mean():.1f} h"
)
kol3.metric(
    "Średnia jakość snu",
    f"{df_filtered['sleep_quality_score'].mean():.1f} / 10"
)
kol4.metric(
    "Czuło się wypoczętych",
    f"{(df_filtered['felt_rested'] == 'Tak').mean() * 100:.0f}%"
)

# Tabs dla trzech analiz
tab1, tab2, tab3 = st.tabs([
    "Co wpływa na sen?",
    "Jak sen wpływa na nas?",
    "Kto jest w grupie ryzyka?"
])

with tab1:
    st.header("Co wpływa na jakość snu?")
    st.markdown("Czynniki stylu życia i zdrowia powiązane z jakością snu.")
    st.divider()

    # Wykres 1
    st.subheader("Korelacje czynników z jakością snu")

    kolumny_akt1 = [
        "stress_score", "wake_episodes_per_night", "work_hours_that_day",
        "sleep_latency_mins", "alcohol_units_before_bed", "screen_time_before_bed_mins",
        "caffeine_mg_before_bed", "steps_that_day", "sleep_quality_score"
    ]

    macierz = df_filtered[kolumny_akt1].corr()

    fig_heatmap = px.imshow(
        macierz,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        aspect="auto",
        zmin=-1, zmax=1,
        # title="Korelacje: czynniki stylu życia a jakość snu"
    )
    fig_heatmap.update_traces(
        hovertemplate="X: %{x}<br>Y: %{y}<br>Korelacja: %{z:.2f}<extra></extra>"
    )
    fig_heatmap.update_layout(template="plotly_white")

    st.plotly_chart(fig_heatmap, width="stretch")

    st.markdown(
        "*Najsilniejszym czynnikiem powiązanym z jakością snu jest **stres** - im wyższy, tym gorszy sen. Kofeina, alkohol i czas przed ekranem mają zaskakująco słaby wpływ.*"
    )
    st.divider()

    # Wykres 2
    st.subheader("Jakość snu a poziom stresu")

    fig_box_stres = px.box(
        df_filtered,
        x="stress_group",
        y="sleep_quality_score",
        color="stress_group",
        category_orders={
            "stress_group": ["Niski", "Umiarkowany", "Wysoki", "Bardzo wysoki"]
        },
        labels={"stress_group": "Poziom stresu", "sleep_quality_score": "Jakość snu"},
        # title="Jakość snu w zależności od poziomu stresu"
    )
    fig_box_stres.update_layout(template="plotly_white", showlegend=False)
    st.plotly_chart(fig_box_stres, width="stretch")

    st.markdown(
        "*Mediana jakości snu spada schodkowo wraz ze wzrostem stresu — od najwyższej przy niskim stresie do najniższej przy bardzo wysokim.*"
    )
    st.divider()


    # Wykres 3
    st.subheader("Jakość snu w zależności od zawodu")

    srednie = (
        df_filtered.groupby("occupation", observed=True)["sleep_quality_score"]
        .mean()
        .sort_values()
        .reset_index()
    )

    fig_bar_zawod = px.bar(
        srednie,
        x="sleep_quality_score",
        y="occupation",
        orientation="h",
        color="sleep_quality_score",
        color_continuous_scale="RdYlGn",
        labels={"sleep_quality_score": "Średnia jakość snu", "occupation": "Zawód"},
        # title="Średnia jakość snu wg zawodu"
    )
    fig_bar_zawod.update_layout(
        template="plotly_white",
        coloraxis_showscale=False,
        hovermode="y unified"    # tooltip przy wierszu, na który najeżdżasz
    )
    fig_bar_zawod.update_traces(
        hovertemplate="Zawód: %{y}<br>Średnia jakość snu: %{x:.2f}<extra></extra>"
    )
    st.plotly_chart(fig_bar_zawod, width="stretch")

    st.markdown(
        "*Najlepiej śpią emeryci i osoby z elastycznym grafikiem, najgorzej — zawody stresujące i zmianowe (prawnicy, pielęgniarki, lekarze, kierowcy).*"
    )


with tab2:
    st.header("Jak sen wpływa na wydajność poznawczą?")
    st.markdown("Sen jako czynnik wpływający na funkcjonowanie umysłu.")
    st.divider()

    # Wykres 4
    st.subheader("Jakość snu a wydajność poznawcza")

    # Próbka dla czytelności - przy dużej liczbie punktów wykres byłby nieczytelny
    probka = df_filtered.sample(min(3000, len(df_filtered)), random_state=42)

    fig_scatter = px.scatter(
        probka,
        x="sleep_quality_score",
        y="cognitive_performance_score",
        color="enough_sleep",
        color_discrete_map={
            "Tak": "#00cc96",
            "Nie": "#ef553b"
        },
        opacity=0.5,
        labels={
            "sleep_quality_score": "Jakość snu",
            "cognitive_performance_score": "Wydajność poznawcza",
            "enough_sleep": "Wystarczający sen"
        },
        # title="Jakość snu a wydajność poznawcza"
    )
    fig_scatter.update_layout(template="plotly_white")
    st.plotly_chart(fig_scatter, width="stretch")

    st.markdown(
        "*Najsilniejsza zależność w całym zbiorze (korelacja **0.86**) — im lepsza jakość snu, tym wyższa wydajność poznawcza. Osoby śpiące wystarczająco długo (≥7h) skupiają się w prawym górnym rogu.*"
    )
    st.divider()

    # Wykres 5
    st.subheader("Rozkład wydajności poznawczej")

    fig_hist = px.histogram(
        df_filtered,
        x="cognitive_performance_score",
        color="felt_rested",
        color_discrete_map={
            "Tak": "#00cc96",
            "Nie": "#ef553b"
        },
        nbins=40,
        barmode="overlay",
        opacity=0.6,
        labels={
            "cognitive_performance_score": "Wydajność poznawcza",
            "felt_rested": "Czuł się wypoczęty"
        },
        # title="Rozkład wydajności poznawczej"
    )
    fig_hist.update_layout(template="plotly_white")
    st.plotly_chart(fig_hist, width="stretch")

    st.markdown(
        "*Osoby wypoczęte (kolor odrębny) mają rozkład przesunięty w prawo — poczucie wypoczęcia pokrywa się z realnie wyższą wydajnością poznawczą.*"
    )

with tab3:
    st.header("Kto jest w grupie ryzyka?")
    st.markdown("Profile najbardziej narażone na zaburzenia snu.")
    st.divider()

    # Wykres 6
    st.subheader("Ryzyko zaburzeń snu wg zawodu")
    st.markdown("*Kliknij zawód, aby przybliżyć jego rozkład ryzyka.*")

    df_sunburst = df_filtered[["occupation", "sleep_disorder_risk"]].astype(str)

    fig_sunburst = px.sunburst(
        df_sunburst,
        path=["occupation", "sleep_disorder_risk"],
        color="sleep_disorder_risk",
        color_discrete_map={
            "Healthy": "#2ca02c", "Mild": "#ffdd57",
            "Moderate": "#ff7f0e", "Severe": "#d62728", "(?)": "#cccccc"
        }
    )
    fig_sunburst.update_layout(height=700)
    st.plotly_chart(fig_sunburst, width="stretch")

    st.markdown(
        "*Emeryci są niemal w całości zdrowi. Najwięcej ciężkiego ryzyka mają pielęgniarki, prawnicy, lekarze i kierowcy — te same zawody, które śpią najgorzej.*"
    )
    st.divider()


    # Wykres 7
    st.subheader("Ryzyko zaburzeń snu wg grupy wiekowej")

    tabela = pd.crosstab(
        df_filtered["age_group"],
        df_filtered["sleep_disorder_risk"],
        normalize="index"
    ) * 100
    tabela = tabela[["Healthy", "Mild", "Moderate", "Severe"]]

    fig_heat_wiek = px.imshow(
        tabela,
        text_auto=".1f",
        color_continuous_scale="Reds",
        aspect="auto",
        labels={"x": "Poziom ryzyka", "y": "Grupa wiekowa", "color": "% w grupie"},
        # title="Ryzyko zaburzeń snu wg grupy wiekowej (% w grupie)"
    )
    fig_heat_wiek.update_traces(
        hovertemplate="Poziom ryzyka: %{x}<br>Grupa wiekowa: %{y}<br>% w grupie: %{z:.1f}%<extra></extra>"
    )
    fig_heat_wiek.update_layout(template="plotly_white")
    st.plotly_chart(fig_heat_wiek, width="stretch")

    st.markdown(
        "*Ryzyko rośnie z wiekiem — odsetek osób zdrowych spada, a ciężkiego ryzyka rośnie z wiekiem ponad dwukrotnie. Najbardziej zagrożeni to starsi oraz osoby w stresujących zawodach.*"
    )
