import json
import pandas as pd
import plotly.express as px


class EKGdata:

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms'])
        self.df = self.df.iloc[:5000]

    def find_peaks(self):
        series = self.df["Messwerte in mV"].dropna()
        threshold = series.min() + (series.max() - series.min()) * 0.55

        # Lokales Maximum in einem Fenster von 50 Samples
        rolling_max = series.rolling(50, center=True).max()
        is_peak = (series == rolling_max) & (series > threshold)

        # Nur den ersten Punkt pro Peak-Gruppe behalten
        peak_mask = is_peak & (~is_peak.shift(1, fill_value=False))

        self.peaks = self.df.loc[series[peak_mask].index]
        print("Threshold:", threshold, "Anzahl Peaks:", len(self.peaks))
        return self.peaks

    def estimate_hr(self):
        self.find_peaks()
        self.peaks['Zeitdifferenz'] = self.peaks['Zeit in ms'].diff()
        self.peaks['HR'] = 60000 / self.peaks['Zeitdifferenz']
        return self.peaks[['Zeit in ms', 'Messwerte in mV', 'HR']]
    
    def plot_time_series(self, threshold=None):
        self.estimate_hr()
        self.fig = px.line(self.df.head(6000), x="Zeit in ms", y="Messwerte in mV")
        self.fig.add_scatter(x=self.peaks['Zeit in ms'], y=self.peaks['Messwerte in mV'], mode='markers', name='Peaks')
        return self.fig


if __name__ == "__main__":
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    ekg = EKGdata(ekg_dict)
    print("Anzahl Peaks:", len(ekg.find_peaks()))
    series = ekg.df["Messwerte in mV"]
    print("Werte über 336:", (series > 336).sum())
    print("Werte über 350:", (series > 350).sum())
    show = ekg.plot_time_series()
    show.show()