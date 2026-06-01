# programmieren_2_aufgabe_2-4

# EKG & Power Zone Analyzer

> An interactive Streamlit application for analyzing ECG signals and training data. The app visualizes raw ECG recordings and decomposes power & heart-rate data into the five classic training zones, including the time spent in each zone.

---

## Table of Contents

- [About the Project]
- [Requirements]
- [Installation]
- [Usage]
- [Project Structure]
- [Dependencies]
- [License]
- [Authors]

---

## About the Project

This project is a **Streamlit web application** for analyzing ECG signals and training data. The app visualizes raw ECG recordings and decomposes power & heart-rate data into the five classic training zones, including the time spent in each zone.

In `main.py` the user can **select a test subject** from a dropdown menu. After selection, the corresponding **profile picture** and the **file path** to the person's data are displayed

The analysis view (`interactive_plot.py`) is then structured into **two tabs**:

### Tab 1 — ECG Plot
Displays the raw ECG signal of the selected test subject over time. Useful for visually inspecting heart-rate variability and identifying R-peaks.

### Tab 2 — Power & Heart-Rate Zones
Plots **power output and heart rate** over the duration of an activity and splits the data into the **five training zones**:

| Zone | Name             | % of Max HR |
|------|------------------|-------------|
| 1    | Recovery         | 50–60 %     |
| 2    | Endurance        | 60–70 %     |
| 3    | Tempo            | 70–80 %     |
| 4    | Threshold        | 80–90 %     |
| 5    | Anaerobic / VO₂  | 90–100 %    |

For each zone, the app calculates and displays **how long the test subject stayed in that zone** during the recorded activity.

---

## Requirements

- Python >= 3.13
- uv
- Git
- Internet connection for installing dependencies

---

## Installation

### Install uv

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Clone the Repository

```bash
git clone https://github.com/tjenewein/programmieren_2_aufgabe_2-4.git
cd programmieren_2_aufgabe_2-4
```

### Install Dependencies

Install all required packages:

```bash
uv sync
```

This will:

- Install all Python dependencies
- Create a virtual environment automatically
- Use the exact versions defined in `uv.lock`

---

## Usage

Start the Streamlit app:

```bash
run streamlit run main.py
streamlit run interactive_plot.py
```

Streamlit will open the dashboard in your default browser (usually at `http://localhost:8501`).

Inside the app you can:

1. Select a **test subject** from the dropdown in `main.py` — the corresponding profile picture and picture path are shown.
2. Switch between the **ECG** tab and the **Power & Zones** tab in the analysis view.
3. Inspect the calculated time spent in each of the five training zones.

---

## Project Structure

```text
programmieren_2_aufgabe_2/
│
├── data/
│   ├── activities/
│   │   └── activity.csv         # Activity / power / HR sensor data
│   ├── ekg_data/                # Raw ECG recordings
│   ├── pictures/                # Profile pictures of test subjects
│   └── person_db.json           # Personal data of test subjects
│
├── interactive_plot.py          # Streamlit tabs: ECG + Power/HR zones
├── load_data.py                 # Data loading helpers
├── read_pandas.py               # CSV / dataframe utilities
├── main.py                      # Streamlit entry point — person selection (picture + path)
│
├── pyproject.toml               # Project configuration
├── uv.lock                      # Lockfile
├── .gitignore
├── .python-version
└── README.md
```

---

## Dependencies

All dependencies are defined in `pyproject.toml`. Key packages include:

- **streamlit** — interactive web dashboard
- **pandas** — data handling
- **plotly / matplotlib** — plotting
- **numpy** — numerical computations

Install them automatically with `uv sync`.

---

## License

No License

---

## Authors

Matteo Harrasser, Jeremias Koller und Thomas Jenewein

GitHub: https://github.com/tjenewein