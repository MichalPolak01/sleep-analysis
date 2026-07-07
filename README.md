# 😴 Analiza zdrowia snu

Interaktywny dashboard analizujący, **co wpływa na jakość snu** i **jak sen przekłada się na wydajność poznawczą** oraz ryzyko zaburzeń snu.

🔗 **Aplikacja na żywo:** [sleep-analysis-michal.streamlit.app](https://sleep-analysis-michalpolak01.streamlit.app/)

## Opis projektu

Projekt bada zależności między stylem życia, jakością snu a funkcjonowaniem człowieka na zbiorze 100 000 rekordów pochodzącym z serwisu Kaggle. Dashboard prowadzi przez trzy pytania:

1. **Co wpływa na jakość snu?** — czynniki stylu życia i zdrowia (stres, praca, używki, aktywność).
2. **Jak sen wpływa na nas?** — związek jakości snu z wydajnością poznawczą.
3. **Kto jest w grupie ryzyka?** — profile najbardziej narażone na zaburzenia snu (wg zawodu i wieku).

Najważniejsze obserwacje: głównym czynnikiem pogarszającym sen jest **stres**, a jakość snu wykazuje bardzo silny związek z **wydajnością poznawczą**. Ryzyko zaburzeń rośnie z wiekiem i jest najwyższe w stresujących, zmianowych zawodach.

## Zakres wykonania

Projekt składa się z dwóch części: **notebooka** z przygotowaniem danych i analizą (`data_preparation.ipynb`) oraz **aplikacji** prezentującej wyniki (`app.py`).

### Przygotowanie danych (notebook)

Choć zbiór był stosunkowo czysty, notebook przechodzi przez pełny proces przygotowania danych, aby zademonstrować poszczególne techniki:

- **Obsługa braków** — wykrywanie braków oraz demonstracja ich uzupełniania (mediana / moda) i usuwania na kontrolowanej próbce.
- **Konwersje typów** — zamiana kolumn 0/1 na czytelne etykiety oraz kolumn tekstowych na typ `category`, co zmniejszyło zużycie pamięci o ok. 45%.
- **Transformacje** — transformacja logarytmiczna (`log1p`) zmiennych o silnie skośnym rozkładzie.
- **Kolumny pochodne** — grupy wiekowe, kategorie BMI (wg progów WHO) oraz flagi (np. „dużo ekranu przed snem", „wystarczający sen").

### Eksploracyjna analiza danych — EDA (notebook)

Analiza jest zorganizowana wokół trzech pytań (aktów narracji), każdy poparty statystykami, wykresami i wnioskami:

1. **Co wpływa na jakość snu?** — analiza korelacji wykazała, że dominującym czynnikiem jest **stres** (korelacja −0.64), a używki (kofeina, alkohol) i czas przed ekranem mają zaskakująco słaby wpływ.
2. **Jak sen wpływa na wydajność poznawczą?** — jakość snu okazała się najsilniej powiązaną zmienną w całym zbiorze (korelacja **0.86**).
3. **Kto jest w grupie ryzyka?** — ryzyko zaburzeń snu rośnie z wiekiem i jest najwyższe w stresujących, zmianowych zawodach (pielęgniarki, prawnicy, lekarze, kierowcy).

Notebook kończy się zapisem oczyszczonego zbioru `sleep_clean.csv`, który stanowi wejście do aplikacji.

### Dashboard (aplikacja)

- **7 interaktywnych wykresów** — heatmapy, wykres słupkowy, boxplot, scatter, histogram, sunburst.
- **4 filtry** — kraj, zawód, przedział wiekowy, chronotyp; wszystkie wykresy reagują na filtry na żywo.
- **Pasek wskaźników KPI** — liczba osób, średnia długość i jakość snu, odsetek wypoczętych.
- **Układ z zakładkami** — trzy zakładki odpowiadające trzem aktom narracji.

## Uruchomienie lokalne

```bash
# Sklonuj repozytorium
git clone https://github.com/[twoj-login]/sleep-analysis.git
cd sleep-analysis

# Zainstaluj zależności i uruchom aplikację
uv add streamlit pandas plotly
uv run streamlit run app.py
```

Aplikacja otworzy się pod adresem `http://localhost:8501`.

## Użyte technologie

- **Python** — język analizy
- **pandas** — wczytywanie, czyszczenie i przetwarzanie danych
- **Plotly** — interaktywne wizualizacje
- **Streamlit** — budowa i wdrożenie dashboardu
- **Jupyter** — notebook z przygotowaniem danych i EDA
- **uv** — zarządzanie środowiskiem i zależnościami

## Struktura projektu

```
sleep-analysis/
├── app.py                    # aplikacja Streamlit (dashboard)
├── data_preparation.ipynb    # czyszczenie danych i EDA
├── sleep_health_dataset.csv  # surowe dane (Kaggle)
├── sleep_clean.csv           # oczyszczone dane (wejście do aplikacji)
├── requirements.txt          # zależności do wdrożenia
└── README.md
```