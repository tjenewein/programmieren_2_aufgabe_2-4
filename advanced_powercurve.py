import pandas as pd
import plotly.graph_objects as go
import numpy as np


def read_activity(path="data/activities/activity.csv"):
    # CSV einlesen und PowerOriginal-Spalte als numpy-Array zurückgeben
    df = pd.read_csv(path)
    return df["PowerOriginal"].dropna().values


def compute_power_curve(power, time_resolution_s: float = 1.0, durations=None) -> pd.DataFrame:
    # Eingabe in numpy-Array umwandeln
    power = np.asarray(power, dtype=float)
    n = len(power)
    total_duration_s = n * time_resolution_s

    if durations is None:
        # Logarithmisch verteilte Dauern von 1s bis zur Gesamtdauer
        durations_s = np.unique(
            np.geomspace(time_resolution_s, total_duration_s, num=200).astype(int)
        )
    else:
        durations_s = np.asarray(durations, dtype=float)

    # Dauern in Sekunden in Anzahl Messpunkte umrechnen
    window_sizes = np.unique(
        np.maximum(1, np.round(durations_s / time_resolution_s).astype(int))
    )

    # Präfixsumme für effiziente Rolling-Average-Berechnung (O(n) pro Fenster)
    cumsum = np.cumsum(np.insert(power, 0, 0.0))

    results = []
    for w in window_sizes:
        if w > n:
            break
        # Alle Rolling-Averages der Fensterbreite w berechnen
        averages = (cumsum[w:] - cumsum[:-w]) / w
        results.append({
            "duration_s": w * time_resolution_s,
            "max_avg_power_w": float(averages.max()),  # bestes Fenster speichern
        })

    return pd.DataFrame(results)


def find_best_window(power, duration_s: float, time_resolution_s: float = 1.0) -> dict:
    power = np.asarray(power, dtype=float)
    # Dauer in Sekunden in Anzahl Messpunkte umrechnen
    w = max(1, round(duration_s / time_resolution_s))

    cumsum = np.cumsum(np.insert(power, 0, 0.0))
    averages = (cumsum[w:] - cumsum[:-w]) / w

    # Index des besten Fensters (höchster Durchschnitt)
    best_idx = int(np.argmax(averages))
    return {
        "start_s": best_idx * time_resolution_s,
        "end_s": (best_idx + w) * time_resolution_s,
        "avg_power": float(averages[best_idx]),
    }


def plot_window_comparison(power, durations_s: list, time_resolution_s: float = 1.0) -> go.Figure:
    power = np.asarray(power, dtype=float)
    n = len(power)
    time_axis = np.arange(n) * time_resolution_s

    fig = go.Figure()

    # Rohe Leistungsdaten als Hintergrund in grau
    fig.add_trace(go.Scatter(
        x=time_axis,
        y=power,
        mode="lines",
        line=dict(color="gray", width=1),
        name="Leistung (W)",
        opacity=0.5,
    ))

    colors = ["#EF9F27", "#1D9E75"]

    for i, dur in enumerate(durations_s):
        window = find_best_window(power, dur, time_resolution_s)
        color = colors[i % len(colors)]

        # Nur die Datenpunkte im besten Fenster auswählen
        mask = (time_axis >= window["start_s"]) & (time_axis <= window["end_s"])
        # Bestes Fenster farbig hervorheben
        fig.add_trace(go.Scatter(
            x=time_axis[mask],
            y=power[mask],
            mode="lines",
            fill="tozeroy",
            line=dict(color=color, width=2),
            fillcolor=color,
            opacity=0.4,
            name=f"{int(dur)}s – Ø {window['avg_power']:.1f} W",
        ))

        # Gestrichelte Linie auf Höhe des Durchschnitts
        fig.add_shape(
            type="line",
            x0=window["start_s"], x1=window["end_s"],
            y0=window["avg_power"], y1=window["avg_power"],
            line=dict(color=color, width=2, dash="dash"),
        )

    fig.update_layout(
        title="Bestes Fenster der ausgewählten Dauern im Vergleich",
        xaxis_title="Zeit (s)",
        yaxis_title="Leistung (W)",
        template="plotly_dark",
        
    )
    return fig


def plot_power_curve(df_curve: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    # Fläche unter der Kurve füllen
    fig.add_trace(go.Scatter(
        x=df_curve["duration_s"],
        y=df_curve["max_avg_power_w"],
        mode="lines",
        fill="tozeroy",
        line=dict(width=2),
    ))
    fig.update_layout(
        title="Power Duration Curve",
        xaxis_title="Dauer (s-min)",
        yaxis_title="Max. Durchschnittsleistung (W)",
        xaxis_type="log",  
        xaxis=dict(
            tickvals=[1, 5, 10, 30, 60, 300, 600, 1800, 3600],
            ticktext=["1s", "5s", "10s", "30s", "1min", "5min", "10min", "30min", "1h"],
        ),
        template="plotly_dark",
    )
    return fig


if __name__ == "__main__":
    power = read_activity()
    curve = compute_power_curve(power, time_resolution_s=1.0)
    plot_power_curve(curve).show()

    # Fenstervergleich: 7min (420s) vs 10min (600s) zur Kontrolle der Power-Curve
    plot_window_comparison(power, durations_s=[420, 600], time_resolution_s=1.0).show()