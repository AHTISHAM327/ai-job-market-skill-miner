from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Job-Market Skill Miner", layout="wide")
st.title("AI Job-Market Skill Miner")
st.caption("Data/AI job postings from LinkedIn 2023-24 (Kaggle). This page: which skills are asked for together.")

DATA = Path(__file__).parent / "data" / "rules_top_v0.csv"
if not DATA.exists():
    st.error("The file app/data/rules_top_v0.csv is missing.")
    st.stop()
rules = pd.read_csv(DATA)

st.subheader("Skills that go together")
st.write(
    "Read a row like this: if a posting asks for the skill in **if**, it also asks for the skill in **then** "
    "in *confidence* share of the cases. *Lift* above 1 means the two skills go together more often than by chance."
)

skills = sorted(set(rules["if"]) | set(rules["then"]))
pick = st.multiselect("Show only rules with these skills (empty = all)", skills)
lo, hi = float(rules["lift"].min()), float(rules["lift"].max())
min_lift = st.slider("Minimum lift", lo, hi, lo, 0.1) if lo < hi else lo

view = rules[rules["lift"] >= min_lift]
if pick:
    view = view[view["if"].isin(pick) | view["then"].isin(pick)]

st.dataframe(view.reset_index(drop=True), hide_index=True)
if len(view):
    chart = view.head(10).assign(rule=lambda d: d["if"] + " -> " + d["then"]).set_index("rule")["lift"]
    st.bar_chart(chart)
st.caption("First quick version (rules_top_v0). The salary-band page and the job-families page come next.")
