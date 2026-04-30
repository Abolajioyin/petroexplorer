import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_well_data():
    wells = [
        {"well_id": f"W-{i:03d}", 
         "name": f"Well {i}",
         "location": f"Block {i//5 + 1}",
         "depth_m": round(np.random.uniform(2000, 5000), 2),
         "type": np.random.choice(["Producer", "Injector", "Observer"]),
         "drilling_date": (datetime(2010, 1, 1) + timedelta(days=int(np.random.uniform(0, 3650)))).strftime("%Y-%m-%d"),
         "reservoir": np.random.choice(["Reservoir A", "Reservoir B", "Reservoir C"]),
         "status": np.random.choice(["Active", "Inactive", "Abandoned"], p=[0.7, 0.2, 0.1])
        }
        for i in range(1, 51)
    ]
    return pd.DataFrame(wells)

def generate_production_data():
    records = []
    for well_id in [f"W-{i:03d}" for i in range(1, 21)]:
        base_oil = np.random.uniform(500, 2000)
        for month in range(60):
            date = datetime(2019, 1, 1) + timedelta(days=month * 30)
            decline = np.exp(-0.02 * month)
            records.append({
                "well_id": well_id,
                "date": date.strftime("%Y-%m-%d"),
                "oil_bbl": round(base_oil * decline * np.random.uniform(0.9, 1.1), 2),
                "gas_mcf": round(base_oil * decline * np.random.uniform(0.5, 1.5), 2),
                "water_bbl": round(base_oil * (1 - decline) * np.random.uniform(0.8, 1.2), 2),
            })
    return pd.DataFrame(records)

def generate_reservoir_data():
    reservoirs = [
        {"reservoir_id": f"R-{i:03d}",
         "name": f"Reservoir {chr(64+i)}",
         "porosity_pct": round(np.random.uniform(10, 35), 2),
         "permeability_md": round(np.random.uniform(1, 500), 2),
         "pressure_psi": round(np.random.uniform(2000, 8000), 2),
         "temperature_f": round(np.random.uniform(150, 350), 2),
         "depth_m": round(np.random.uniform(2000, 5000), 2),
         "fluid_type": np.random.choice(["Oil", "Gas", "Oil & Gas"])
        }
        for i in range(1, 11)
    ]
    return pd.DataFrame(reservoirs)

wells_df = generate_well_data()
production_df = generate_production_data()
reservoir_df = generate_reservoir_data()