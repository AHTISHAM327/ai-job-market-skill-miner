from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Job-Market Skill Miner", layout="centered")

DATA = Path(__file__).parent / "data"
RULES = DATA / "rules_top_v0.csv"
TOP = DATA / "skills_top_v0.csv"
COLOR = "#b4a7d6"

NAMES = {
    "aws": "AWS", "gcp": "Google Cloud", "llm": "LLMs", "nlp": "NLP", "sql": "SQL",
    "nosql": "NoSQL", "etl": "ETL", "power bi": "Power BI", "pytorch": "PyTorch",
    "tensorflow": "TensorFlow", "generative ai": "Generative AI",
    "collaboration": "Teamwork",
}


def name(skill):
    return NAMES.get(skill, skill[:1].upper() + skill[1:])


def times(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


st.title("Which skills do data and AI jobs ask for?")
st.write(
    "We read **1,578 real LinkedIn job ads** for data and AI jobs (2023–24) "
    "and counted the skills each ad asks for."
)

if not RULES.exists():
    st.error("The file app/data/rules_top_v0.csv is missing.")
    st.stop()
rules = pd.read_csv(RULES)

if TOP.exists():
    top = pd.read_csv(TOP)
    top["Skill"] = top["skill"].map(name)
    top["Percent of job ads"] = (top["share"] * 100).round(1)
    st.header("1. The skills employers ask for most")
    pct = dict(zip(top["skill"], top["Percent of job ads"]))
    if {"python", "sql", "machine learning", "collaboration", "communication"} <= set(pct):
        st.write(
            f"**Python** is in {pct['python']:.0f} of every 100 ads, **SQL** in {pct['sql']:.0f} "
            f"and **machine learning** in {pct['machine learning']:.0f}. "
            f"**Teamwork** and **communication** come up even more often ({pct['collaboration']:.0f} and {pct['communication']:.0f})."
        )
    bars = alt.Chart(top).mark_bar(color=COLOR, cornerRadiusEnd=3).encode(
        x=alt.X("Percent of job ads:Q", title="Out of every 100 job ads"),
        y=alt.Y("Skill:N", sort="-x", title=None, axis=alt.Axis(labelLimit=260)),
        tooltip=["Skill", "Percent of job ads"],
    ).properties(height=380)
    st.altair_chart(bars)
    st.caption("Teamwork and communication may be counted a little high: general company text uses these words too.")

st.header("2. Which skills go with a skill you know?")
skills = sorted(set(rules["if"]) | set(rules["then"]), key=name)
pick = st.selectbox("Your skill", skills, index=skills.index("tensorflow") if "tensorflow" in skills else 0, format_func=name)

lines = []
for _, r in rules.iterrows():
    if r["if"] == pick:
        other, sentence = r["then"], f"{round(r['confidence'] * 10)} in 10 {name(pick)} jobs also ask for {name(r['then'])}"
    elif r["then"] == pick:
        other, sentence = r["if"], f"{round(r['confidence'] * 10)} in 10 {name(r['if'])} jobs also ask for {name(pick)}"
    else:
        continue
    lines.append((r["lift"], f"**{name(other)}**: {sentence} ({times(r['lift'])} times more often than in an average job)."))

st.write(f"Skills that usually come together with **{name(pick)}**:")
for _, text in sorted(lines, reverse=True):
    st.markdown(f"- {text}")
st.caption("Tip: if you learn one skill of a pair, learn the other one too.")

st.header("3. The strongest skill pairs")
st.write("A longer bar means the two skills appear together more often than chance.")
pairs = rules.assign(Pair=rules["if"].map(name) + " + " + rules["then"].map(name), Times=rules["lift"].round(1))
chart = alt.Chart(pairs).mark_bar(color=COLOR, cornerRadiusEnd=3).encode(
    x=alt.X("Times:Q", title="Times more than chance"),
    y=alt.Y("Pair:N", sort="-x", title=None, axis=alt.Axis(labelLimit=260)),
    tooltip=[alt.Tooltip("Pair:N", title="Skills"), alt.Tooltip("Times:Q", title="Times more often")],
).properties(height=420)
st.altair_chart(chart)

with st.expander("Exact numbers (for teachers)"):
    st.write(
        "**Support:** share of all ads that have both skills. "
        "**Confidence:** of the ads with the first skill, the share that also have the second. "
        "**Lift:** how many times more often the two appear together than by chance."
    )
    table = rules.rename(columns={"if": "If an ad asks for", "then": "it also asks for",
                                  "support": "Support", "confidence": "Confidence", "lift": "Lift"})
    st.dataframe(table, hide_index=True)

st.caption(
    "Data: Kaggle 'LinkedIn Job Postings 2023–24' (version 13), mostly US jobs. "
    "It shows what employers ask for, not a promise of a job. Team P08: Ahtisham, Rija, Quratulain."
)
