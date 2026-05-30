import pandas as pd
import plotly.express as px

#Hier wird die CSV-Datei mit den EKG-Daten eingelesen
def read_my_csv():
    df = pd.read_csv("data/ekg_data/01_Ruhe.txt", sep="\t", header=None)
    df.columns = ["Messwerte in mV","Zeit in ms"]
    return df

# Hier wird die CSV-Datei mit den Leistungs- und Herzfrequenzdaten eingelesen
def read_pd():
    df1 = pd.read_csv("C:\\Git\\programmieren_2_aufgabe_2\\programmieren_2_aufgabe_2-4\\data\\activities\\activity.csv")
    return df1

# Hier wird ein Liniendiagramm erstellt, für die EKG-Daten
def make_plot(df):
    fig1 = px.line(df.head(2000), x = "Zeit in ms", y = "Messwerte in mV")
    return fig1

# Hier wird ein Liniendiagramm erstellt, das die Leistung über die Zeit darstellt
def pwr_plot(df1):
    df1["Zeit_min"] = df1["Duration"].cumsum() / 60
    fig = px.line(y = df1["PowerOriginal"]  , x= df1["Zeit_min"], title="Leistung/Zeit(min)")
    labels = {"PowerOriginal": "Leistung", "Zeit_min": "Zeit (min)"}
    fig.update_layout(xaxis_title=labels["Zeit_min"], yaxis_title=labels["PowerOriginal"])
    return fig



def get_zones(slide, df1): 
    max_heart_rate = df1["HeartRate"].max()  # Maximal mögliche Herzfrequenz
    #Hier wird die Herzfrequenz in 5 Zonen eingeteilt, basierend auf dem Slider-Wert (slide) und der maximalen Herzfrequenz im Datensatz
    return [
        (slide * 0.5, slide * 0.6, "Zone 1", "blue"),
        (slide * 0.6, slide * 0.7, "Zone 2", "green"),
        (slide * 0.7, slide * 0.8, "Zone 3", "yellow"),
        (slide * 0.8, slide * 0.9, "Zone 4", "orange"),
        (slide * 0.9, max_heart_rate, "Zone 5", "red"),
    ]

# Hier wird ein Liniendiagramm erstellt, das die Herzfrequenz über die Zeit darstellt, mit farblich markierten Bereichen für die verschiedenen Herzfrequenzzonen basierend auf dem Slider-Wert (slide)
def heartrate_plot(df1, slide):
    df1["Zeit_min"] = df1["Duration"].cumsum() / 60
    fig = px.line(y=df1["HeartRate"], x=df1["Zeit_min"], title="Herzfrequenz/Zeit(min)")

    for untere, obere, name, farbe in get_zones(slide):
        fig.add_hrect(y0=untere, y1=obere, fillcolor=farbe, opacity=0.1,
                      line_width=0, annotation_text=name)

    fig.update_layout(xaxis_title="Zeit (min)", yaxis_title="Herzfrequenz")
    return fig

# Hier wird die Zeit berechnet, die in jeder Herzfrequenzzone verbracht wurde, basierend auf den Daten im DataFrame df1 und den definierten Zonen
def read_zones(df1, slide):
    ergebnisse = []
    for untere, obere, name, _ in get_zones(slide, df1):
        in_zone = df1[(df1["HeartRate"] >= untere) & (df1["HeartRate"] < obere)]
        zeit_sekunden = in_zone["Duration"].sum()
        ergebnisse.append({
            "Zone": name,
            "Zeit (s)": round(zeit_sekunden, 1),
            "Zeit (min)": round(zeit_sekunden / 60, 2),
        })
    return pd.DataFrame(ergebnisse)

# Hier wird ein kombiniertes Diagramm erstellt, das sowohl die Leistung als auch die Herzfrequenz über die Zeit darstellt, mit farblich markierten Herzfrequenzzonen basierend auf dem Slider-Wert (slide)
def pwr_hr_plot(slide, df1):
    df1["Zeit_min"] = df1["Duration"].cumsum() / 60

    import plotly.graph_objects as go

    fig = go.Figure()

    # Power auf linker Achse
    fig.add_trace(go.Scatter(
        x=df1["Zeit_min"], y=df1["PowerOriginal"],
        name="PowerOriginal", yaxis="y1", line=dict(color="blue")
    ))

    # HeartRate auf rechter Achse
    fig.add_trace(go.Scatter(
        x=df1["Zeit_min"], y=df1["HeartRate"],
        name="HeartRate", yaxis="y2", line=dict(color="green")
    ))

    # Zonen korrekt auf y2
    for untere, obere, name, farbe in get_zones(slide, df1):
        fig.add_hrect(y0=untere, y1=obere, fillcolor=farbe, opacity=0.1,
                      line_width=0, annotation_text=name, yref="y2")

    fig.update_layout(
        title="Leistung & Herzfrequenz vs. Zeit",
        xaxis_title="Zeit (min)",
        yaxis=dict(title="Leistung (W)", side="left"),
        yaxis2=dict(title="Herzfrequenz (bpm)", side="right", overlaying="y"),
        width=1200, height=600
    )
    return fig





'''
def add_zones(df1):
    
    df1["Zone1"] = df1["HeartRate"] > 220*0.5 and df1["HeartRate"] <= 220*0.6 
    df1["Zone2"] = df1["HeartRate"] > 220*0.6 and df1["HeartRate"] <= 220*0.7  
    df1["Zone3"] = df1["HeartRate"] > 220*0.7 and df1["HeartRate"] <= 220*0.8
    df1["Zone4"] = df1["HeartRate"] > 220*0.8 and df1["HeartRate"] <= 220*0.9
    df1["Zone5"] = df1["HeartRate"] > 220*0.9 
'''

'''
def heartrate(df1):
    df1["Zeit_min"] = df1["Duration"].cumsum() / 60
    fig = px.line(y = df1["HeartRate"]  , x= df1["Zeit_min"], title="Herzfrequenz/Zeit(min)")
    labels = {"HeartRate": "Herzfrequenz", "Zeit_min": "Zeit (min)"}
    fig.update_layout(xaxis_title=labels["Zeit_min"], yaxis_title=labels["HeartRate"])
    return fig
'''
