# P08 dashboard. Code written with AI help (Claude); every number comes from the team notebooks (see app/data/*.csv).
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI Job-Market Skill Miner",
    page_icon=":material/analytics:",
    layout="wide",
)

DATA = Path(__file__).parent / "data"

NAMES = {
    "aws": "AWS", "gcp": "Google Cloud", "llm": "LLMs", "nlp": "NLP", "sql": "SQL",
    "nosql": "NoSQL", "etl": "ETL", "power bi": "Power BI", "pytorch": "PyTorch",
    "tensorflow": "TensorFlow", "generative ai": "Generative AI", "collaboration": "Teamwork",
}


def name(skill: str) -> str:
    return NAMES.get(skill, skill[:1].upper() + skill[1:])


@st.cache_data
def load(file: str) -> pd.DataFrame:
    path = DATA / file
    if not path.exists():
        st.error(f"Missing data file: app/data/{file}")
        st.stop()
    return pd.read_csv(path)


rules = load("rules_top_v0.csv")
skills = load("skills_top_v0.csv")
groups = load("skill_groups_v0.csv")
bands = load("salary_bands_v0.csv")
scores = load("salary_scores_v0.csv")
report = load("salary_band_report_v0.csv")
clusters = load("clusters_v0.csv")
sweep = load("cluster_k_sweep_v0.csv")

top_rule = rules.iloc[0]
best = scores.loc[scores["macro_f1"].idxmax()]
base = scores[(scores["model"] == "Logistic regression") & (scores["features"] == "Job details only")].iloc[0]
families = clusters[clusters["kind"] == "Job family"]

# ---------------------------------------------------------------- header
st.title("AI Job-Market Skill Miner", icon=":material/analytics:")
st.caption("1,578 LinkedIn job ads for data and AI roles (2023–24): the skills they ask for, the job families, and what predicts pay.")

with st.container(horizontal=True):
    st.metric("Job ads analysed", "1,578", help="123,849 LinkedIn ads → 1,753 data/AI titles → 1,578 after removing repeats", border=True)
    st.metric("Most asked-for skill", name(skills.iloc[0]["skill"]), f"{skills.iloc[0]['share']:.0%} of ads", delta_arrow="off", border=True)
    st.metric("Strongest skill pair", f"{top_rule['lift']:.0f}× more than chance", f"{name(top_rule['if'])} + {name(top_rule['then'])}", delta_arrow="off", border=True)
    st.metric("Job families found", f"{len(families)}", f"of 7 groups", delta_arrow="off", border=True)
    st.metric("Pay-band model score", f"{best['macro_f1']:.2f}", f"{best['macro_f1'] - base['macro_f1']:+.2f} with skills + family", help="Macro-F1 (0 to 1). Always guessing one band scores 0.17.", border=True)

tab_skills, tab_pay, tab_families = st.tabs([
    ":material/school: Skills",
    ":material/payments: Pay bands",
    ":material/work: Job families",
])

# ---------------------------------------------------------------- skills
with tab_skills:
    left, right = st.columns([3, 2])
    with left:
        with st.container(border=True):
            st.subheader("Skills employers ask for most", icon=":material/trending_up:")
            chart = skills.assign(Skill=skills["skill"].map(name), share=(skills["share"] * 100).round(1))
            st.bar_chart(chart, x="Skill", y="share", x_label="", y_label="Share of job ads (%)", horizontal=True, sort="-share", height=430,
                         alt="Share of ads per skill, teamwork and communication first, then Python and SQL")
            st.caption("Teamwork and communication may count a little high: general company text uses these words too.")
    with right:
        with st.container(border=True):
            st.subheader("Skills that go together", icon=":material/link:")
            all_skills = sorted(set(rules["if"]) | set(rules["then"]), key=name)
            pick = st.selectbox("Pick a skill you know", all_skills, index=all_skills.index("tensorflow"), format_func=name)
            found = []
            for _, r in rules.iterrows():
                if r["if"] == pick:
                    found.append((r["lift"], r["then"], f"{round(r['confidence'] * 10)} in 10 {name(pick)} ads also ask for {name(r['then'])}"))
                elif r["then"] == pick:
                    found.append((r["lift"], r["if"], f"{round(r['confidence'] * 10)} in 10 {name(r['if'])} ads also ask for {name(pick)}"))
            for lift, other, sentence in sorted(found, reverse=True):
                st.metric(name(other), f"{lift:.1f}× more than chance", sentence, delta_arrow="off", border=True)
            st.caption("Learn the pair, not just one skill.")
        with st.container(border=True):
            st.subheader("Most common skill trios", icon=":material/group_work:")
            trio = pd.DataFrame({"Skills together": groups["group"].map(lambda g: " · ".join(name(w) for w in g.split(" + "))),
                                 "Share of ads": (groups["support"] * 100).round(1)}).head(5)
            st.dataframe(trio, hide_index=True, column_config={
                "Skills together": st.column_config.TextColumn(width="medium"),
                "Share of ads": st.column_config.ProgressColumn(format="%.0f%%", min_value=0, max_value=30, width="small"),
            }, alt="Most common groups of three skills, led by teamwork, communication and Python")

    with st.expander("Exact numbers (association rules)", icon=":material/table_chart:"):
        st.caption("Support: share of all ads with both skills. Confidence: of the ads with the first skill, the share that also have the second. "
                   "Lift: how many times more often the two appear together than by chance. FP-Growth, minimum support 5%, 58 skills searched, 56 kept, 862 rules.")
        st.dataframe(rules.rename(columns={"if": "If an ad asks for", "then": "it also asks for", "support": "Support", "confidence": "Confidence", "lift": "Lift"}),
                     hide_index=True, alt="Top 15 skill rules with support, confidence and lift")

# ---------------------------------------------------------------- pay bands
with tab_pay:
    with st.container(horizontal=True):
        for _, b in bands.iterrows():
            st.metric(f"{b['band']} pay band", f"${b['min_usd']:,.0f} – ${b['max_usd']:,.0f}", f"{b['postings']} ads", delta_arrow="off", border=True,
                      help="Yearly pay in USD. The 552 ads with pay were sorted and cut into 3 equal bands.")
    left, right = st.columns([3, 2])
    with left:
        with st.container(border=True):
            st.subheader("Can we guess the pay band from the ad?", icon=":material/model_training:")
            st.caption("Score = macro-F1 over 5-fold cross-validation (0 to 1). Always guessing one band scores 0.17.")
            order = ["Job details only", "+ skills", "+ job family", "+ skills + job family"]
            short = {"Job details only": "Job details", "+ skills": "+ skills", "+ job family": "+ family", "+ skills + job family": "+ both"}
            comp = scores[scores["model"] != "Always guess one band"].copy()
            comp["Clues"] = pd.Categorical(comp["features"].map(short), [short[o] for o in order], ordered=True)
            comp = comp.rename(columns={"model": "Model"}).sort_values("Clues")
            st.bar_chart(comp, x="Clues", y="macro_f1", color="Model", stack=False, horizontal=True, sort=False, x_label="", y_label="Score (macro-F1)", height=360,
                         alt="Model scores by clue set; random forest with skills and job family is best at 0.595")
    with right:
        with st.container(border=True):
            st.subheader("How well each band is guessed", icon=":material/target:")
            rep = report.assign(band=pd.Categorical(report["band"], ["Low", "Mid", "High"], ordered=True)).sort_values("band")
            st.bar_chart(rep.rename(columns={"band": "Band"}), x="Band", y="f1", horizontal=True, sort=False, x_label="", y_label="F1 score", height=200, alt="F1 per band: low 0.65, mid 0.48, high 0.66")
            st.caption("Mid is the hardest band: it gets mixed with both neighbours.")
        with st.container(border=True):
            st.subheader("What the model leans on", icon=":material/insights:")
            st.markdown("1. Being in the **data / BI analyst** family\n2. Asking for **machine learning**\n3. Mentioning **leadership**")
            st.caption("Random forest feature importance (use, not cause).")

    with st.expander("Exact numbers (salary model)", icon=":material/table_chart:"):
        st.caption("Job details = experience level, work type, remote. Random forest: 300 trees. Train score far above test score means the forest memorises (to tune in M4). "
                   "Label-shuffle check: 0.332 ± 0.041, the same as random guessing, so nothing leaks the answer.")
        wide = scores.pivot(index="model", columns="features", values="macro_f1")[order]
        st.dataframe(wide, alt="Macro-F1 of every model and clue set")
        st.dataframe(report.rename(columns={"band": "Band", "precision": "Precision", "recall": "Recall", "f1": "F1", "postings": "Ads"}), hide_index=True,
                     alt="Precision, recall and F1 per pay band")

# ---------------------------------------------------------------- job families
with tab_families:
    left, right = st.columns([3, 2])
    with left:
        with st.container(border=True):
            st.subheader("Groups found in the ad text", icon=":material/hub:")
            size = pd.DataFrame({"Group": clusters["name"], "Kind": clusters["kind"],
                                 "Share of ads (%)": (clusters["postings"] / clusters["postings"].sum() * 100).round(1)})
            bars = alt.Chart(size).mark_bar(cornerRadiusEnd=3).encode(
                x=alt.X("Share of ads (%):Q", title="Share of ads (%)"),
                y=alt.Y("Group:N", sort="-x", title=None, axis=alt.Axis(labelLimit=260)),
                color=alt.Color("Kind:N", sort=["Job family", "Doubtful", "Not a job family"], legend=alt.Legend(title=None, orient="bottom")),
                tooltip=["Group", "Kind", "Share of ads (%)"],
            ).properties(height=300)
            st.altair_chart(bars, alt="Seven groups by size: four real job families, one doubtful, two boilerplate text groups")
            st.caption("k-means on the ad text (TF-IDF, 5,000 words → 50 topics). 4 of 7 groups are real job families.")
    with right:
        with st.container(border=True):
            st.subheader("Why 7 groups?", icon=":material/tune:")
            st.line_chart(sweep, x="k", y="silhouette", x_label="Number of groups (k)", y_label="Silhouette", height=220,
                          alt="Silhouette for k from 2 to 10; 7 is the best between 3 and 8")
            st.caption("Silhouette scores are all low (under 0.1), so the groups overlap. k = 7 was the best between 3 and 8.")

    cards = st.columns(4)
    for col, (_, fam) in zip(cards, families.iterrows()):
        with col:
            with st.container(border=True, height="stretch"):
                st.markdown(f"**{fam['name']}**")
                st.caption(f"{fam['postings']} ads · {fam['postings'] / clusters['postings'].sum():.0%}")
                st.markdown(" ".join(f":violet-badge[{w.strip()}]" for w in fam["top_words"].split(",")[:4]))
                st.caption("Typical titles: " + fam["top_titles"].replace("; ", ", "))

    with st.expander("Exact numbers (clustering)", icon=":material/table_chart:"):
        st.caption("TF-IDF 1,578 × 5,000, SVD to 50 components (23.1% of variance kept), k-means with seed 42. Stability over 5 seeds: mean ARI 0.714 (lowest 0.591). "
                   "k-means against hierarchical (ward): ARI 0.495.")
        st.dataframe(clusters.rename(columns={"cluster": "Cluster", "name": "Name", "kind": "Kind", "postings": "Ads", "top_words": "Top words", "top_titles": "Top titles"}),
                     hide_index=True, alt="All seven clusters with sizes, top words and top titles")
        st.dataframe(sweep.rename(columns={"k": "k", "inertia": "Inertia", "silhouette": "Silhouette"}), hide_index=True, alt="Inertia and silhouette for k from 2 to 10")

st.caption("Data: Kaggle “LinkedIn Job Postings 2023–24” (version 13), mostly US ads. It shows what employers ask for, not a promise of a job. "
           "Team P08, NUST: Ahtisham (salary model, app), Rija (job families), Quratulain (skill rules).")
