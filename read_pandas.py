import pandas as pd
import plotly.express as px


def read_my_csv():
    # Einlesen eines Dataframes
    ## "\t" steht für das Trennzeichen in der txt-Datei (Tabulator anstelle von Beistrich)
    ## header = None: es gibt keine Überschriften in der txt-Datei
    df = pd.read_csv("data/ekg_data/01_Ruhe.txt", sep="\t", header=None)

    

    df.columns = ["Messwerte in mV","Zeit in ms"]
    # Setzt die Columnnames im Dataframe
    return df

def read_pd():
    df1 = pd.read_csv("C:\\Git\\programmieren_2_aufgabe_2\\programmieren_2_aufgabe_2-4\\data\\activities\\activity.csv")
    return df1


def make_plot(df):
    fig1 = px.line(df.head(2000), x = "Zeit in ms", y = "Messwerte in mV")
    return fig1


def pwr_plot(df1):


    df1["Zeit_min"] = df1["Duration"].cumsum() / 60
    fig = px.line(y = df1["PowerOriginal"]  , x= df1["Zeit_min"], title="Leistung/Zeit(min)")
    labels = {"PowerOriginal": "Leistung", "Zeit_min": "Zeit (min)"}
    fig.update_layout(xaxis_title=labels["Zeit_min"], yaxis_title=labels["PowerOriginal"])
    return fig

'''
def heartrate(df1):
    df1["Zeit_min"] = df1["Duration"].cumsum() / 60
    fig = px.line(y = df1["HeartRate"]  , x= df1["Zeit_min"], title="Herzfrequenz/Zeit(min)")
    labels = {"HeartRate": "Herzfrequenz", "Zeit_min": "Zeit (min)"}
    fig.update_layout(xaxis_title=labels["Zeit_min"], yaxis_title=labels["HeartRate"])
    return fig
'''

def heartrate_plot(df1):
    df1["Zeit_min"] = df1["Duration"].cumsum() / 60
    fig = px.line(y=df1["HeartRate"], x=df1["Zeit_min"], title="Herzfrequenz/Zeit(min)")

    # Zonen als farbige Hintergrundbereiche
    fig.add_hrect(y0=220*0.5, y1=220*0.6, fillcolor="blue",   opacity=0.1, line_width=0, annotation_text="Zone 1")
    fig.add_hrect(y0=220*0.6, y1=220*0.7, fillcolor="green",  opacity=0.1, line_width=0, annotation_text="Zone 2")
    fig.add_hrect(y0=220*0.7, y1=220*0.8, fillcolor="yellow", opacity=0.1, line_width=0, annotation_text="Zone 3")
    fig.add_hrect(y0=220*0.8, y1=220*0.9, fillcolor="orange", opacity=0.1, line_width=0, annotation_text="Zone 4")
    fig.add_hrect(y0=220*0.9, y1=220,     fillcolor="red",    opacity=0.1, line_width=0, annotation_text="Zone 5")

    fig.update_layout(xaxis_title="Zeit (min)", yaxis_title="Herzfrequenz")
    return fig



def pwr_hr_plot(slide,df1):
    df1["Zeit_min"] = df1["Duration"].cumsum() / 60

    df_melt = df1[["Zeit_min", "PowerOriginal", "HeartRate"]].melt(
        id_vars="Zeit_min",
        value_vars=["PowerOriginal", "HeartRate"],
        var_name="Messung",
        value_name="Wert"
    )


    fig = px.line(df_melt, x="Zeit_min", y="Wert", color="Messung",
                  title="Leistung & Herzfrequenz vs. Zeit")
    
    fig.for_each_trace(lambda t: t.update(yaxis="y2") if t.name == "HeartRate" else t)


    min_heart_rate = df1["HeartRate"].min()
    max_heart_rate = df1["HeartRate"].max()
    
    fig.add_hrect(y0=min_heart_rate, y1=slide*0.6, fillcolor="blue",   opacity=0.1, line_width=0, annotation_text="Zone 1", yref="y2")
    fig.add_hrect(y0=slide*0.6, y1=slide*0.7, fillcolor="green",  opacity=0.1, line_width=0, annotation_text="Zone 2", yref="y2")
    fig.add_hrect(y0=slide*0.7, y1=slide*0.8, fillcolor="yellow", opacity=0.1, line_width=0, annotation_text="Zone 3", yref="y2")
    fig.add_hrect(y0=slide*0.8, y1=slide*0.9, fillcolor="orange", opacity=0.1, line_width=0, annotation_text="Zone 4", yref="y2")
    fig.add_hrect(y0=slide*0.9, y1=max_heart_rate, fillcolor="red",    opacity=0.1, line_width=0, annotation_text="Zone 5", yref="y2")

    fig.data[0].update(line=dict(color="blue"))   # PowerOriginal
    fig.data[1].update(line=dict(color="green"))    # HeartRate

    fig.update_layout(xaxis_title="Zeit (min)", yaxis = dict(title="Leistung (W)", side="left"),
        yaxis2=dict(title="Herzfrequenz (bpm)", side="right", overlaying = "y"), width = 1200, height = 600)
    return fig
'''
def add_zones(df1):
    
    df1["Zone1"] = df1["HeartRate"] > 220*0.5 and df1["HeartRate"] <= 220*0.6 
    df1["Zone2"] = df1["HeartRate"] > 220*0.6 and df1["HeartRate"] <= 220*0.7  
    df1["Zone3"] = df1["HeartRate"] > 220*0.7 and df1["HeartRate"] <= 220*0.8
    df1["Zone4"] = df1["HeartRate"] > 220*0.8 and df1["HeartRate"] <= 220*0.9
    df1["Zone5"] = df1["HeartRate"] > 220*0.9 
'''

