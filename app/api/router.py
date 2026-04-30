from fastapi import APIRouter, HTTPException, Query
from app.core.analyzer import wells_df, production_df, reservoir_df

import plotly.express as px
import json

router = APIRouter(prefix="/api", tags=["explorer"])

@router.get("/ping")
def ping():
    return {"ok": True}

# WELLS
@router.get("/wells")
def get_wells(
    status: str = None,
    reservoir: str = None,
    well_type: str = None
):
    df = wells_df.copy()
    if status:
        df = df[df["status"].str.lower() == status.lower()]
    if reservoir:
        df = df[df["reservoir"].str.lower() == reservoir.lower()]
    if well_type:
        df = df[df["type"].str.lower() == well_type.lower()]
    return {"total": len(df), "wells": df.to_dict(orient="records")}

@router.get("/wells/{well_id}")
def get_well(well_id: str):
    well = wells_df[wells_df["well_id"] == well_id]
    if well.empty:
        raise HTTPException(status_code=404, detail="Well not found")
    return well.to_dict(orient="records")[0]

# PRODUCTION
@router.get("/production")
def get_production(
    well_id: str = None,
    start_date: str = None,
    end_date: str = None
):
    df = production_df.copy()
    if well_id:
        df = df[df["well_id"] == well_id]
    if start_date:
        df = df[df["date"] >= start_date]
    if end_date:
        df = df[df["date"] <= end_date]
    return {"total_records": len(df), "production": df.to_dict(orient="records")}

@router.get("/production/summary")
def get_production_summary():
    df = production_df.copy()
    summary = {
        "total_oil_bbl": round(df["oil_bbl"].sum(), 2),
        "total_gas_mcf": round(df["gas_mcf"].sum(), 2),
        "total_water_bbl": round(df["water_bbl"].sum(), 2),
        "avg_daily_oil_bbl": round(df["oil_bbl"].mean(), 2),
        "top_producing_well": df.groupby("well_id")["oil_bbl"].sum().idxmax(),
    }
    return summary

# RESERVOIRS
@router.get("/reservoirs")
def get_reservoirs(fluid_type: str = None):
    df = reservoir_df.copy()
    if fluid_type:
        df = df[df["fluid_type"].str.lower() == fluid_type.lower()]
    return {"total": len(df), "reservoirs": df.to_dict(orient="records")}

@router.get("/reservoirs/{reservoir_id}")
def get_reservoir(reservoir_id: str):
    res = reservoir_df[reservoir_df["reservoir_id"] == reservoir_id]
    if res.empty:
        raise HTTPException(status_code=404, detail="Reservoir not found")
    return res.to_dict(orient="records")[0]
import plotly.express as px
import json

@router.get("/charts/production-decline")
def production_decline_chart(well_id: str = "W-001"):
    df = production_df[production_df["well_id"] == well_id].copy()
    if df.empty:
        raise HTTPException(status_code=404, detail="Well not found")
    
    fig = px.line(
        df, 
        x="date", 
        y="oil_bbl",
        title=f"Production Decline Curve — {well_id}",
        labels={"oil_bbl": "Oil Production (bbl)", "date": "Date"},
        template="plotly_dark"
    )
    
    return json.loads(fig.to_json())

@router.get("/charts/reservoir-properties")
def reservoir_properties_chart():
    fig = px.scatter(
        reservoir_df,
        x="porosity_pct",
        y="permeability_md",
        size="pressure_psi",
        color="fluid_type",
        hover_name="name",
        title="Reservoir Properties — Porosity vs Permeability",
        labels={
            "porosity_pct": "Porosity (%)",
            "permeability_md": "Permeability (md)"
        },
        template="plotly_dark"
    )
    
    return json.loads(fig.to_json())

@router.get("/charts/production-by-well")
def production_by_well_chart():
    df = production_df.groupby("well_id")["oil_bbl"].sum().reset_index()
    df = df.sort_values("oil_bbl", ascending=False).head(10)
    
    fig = px.bar(
        df,
        x="well_id",
        y="oil_bbl",
        title="Top 10 Wells by Total Oil Production",
        labels={"oil_bbl": "Total Oil (bbl)", "well_id": "Well ID"},
        template="plotly_dark"
    )
    
    return json.loads(fig.to_json())