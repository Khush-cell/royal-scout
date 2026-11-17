
from pathlib import Path
from textwrap import dedent

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Royal Scout | Pressure Intelligence",
    page_icon="🏏",
    layout="wide"
)


# ---------------- ROYAL SCOUT VISUAL THEME ----------------

st.markdown(
    """
    <style>
    /* Main canvas */
    .stApp {
        background-color: #f5f2e9;
        color: #183b34;
    }

    [data-testid="stHeader"] {
        background: rgba(245, 242, 233, 0.95);
    }

    [data-testid="stSidebar"] {
        background-color: #10382f;
    }

    [data-testid="stSidebar"] * {
        color: #f5f2e9;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #e6dfcf;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        color: #f5f2e9;
    }

    /* Main content width and typography */
    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: #123f35;
        font-family: Georgia, serif;
    }

    h1 {
        letter-spacing: 0.5px;
    }

    [data-testid="stCaptionContainer"] {
        color: #8b8172;
    }

    /* Tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #e5dfd2;
        border-radius: 8px;
        overflow: hidden;
    }

    /* Dividers */
    hr {
        border-color: #ded8cc;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #fffefa;
        border: 1px solid #e5dfd2;
        border-radius: 10px;
        padding: 14px 16px;
    }

    /* Radio selection accent */
    [data-testid="stSidebar"] [role="radiogroup"] > label {
        padding: 4px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"


# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():
    batters = pd.read_csv(DATA / "final_batter_rankings.csv")
    bowlers = pd.read_csv(DATA / "final_bowler_rankings.csv")

    return batters, bowlers


try:
    batters, bowlers = load_data()
except FileNotFoundError:
    st.error(
        "Ranking files not found. Please run "
        "analysis/build_final_rankings.py first."
    )
    st.stop()


# ---------------- HEADER ----------------

st.title("🏏 ROYAL SCOUT")
st.subheader("Pressure Performance Intelligence")
st.caption(
    "Identifying the most reliable batters and bowlers "
    "under high-pressure T20 chase situations."
)

st.divider()


# ---------------- SIDEBAR ----------------

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Batters", "Bowlers", "Methodology"]
)

st.sidebar.divider()
st.sidebar.caption("Royal Scout | Hackathon Analytics")


# ---------------- HELPER ----------------


def show_ranking_table(df, player_col):
    display_df = df[
        ["rank", player_col, "matches_high", "reliability_score"]
    ].copy()

    display_df = display_df.rename(columns={
        "rank": "Rank",
        player_col: "Player",
        "matches_high": "High-pressure matches",
        "reliability_score": "Reliability score"
    })

    display_df["Reliability score"] = (
        display_df["Reliability score"].round(2)
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=385,
        column_config={
            "Rank": st.column_config.NumberColumn(
                "Rank",
                format="%d",
                width="small"
            ),
            "Player": st.column_config.TextColumn(
                "Player",
                width="medium"
            ),
            "High-pressure matches": st.column_config.NumberColumn(
                "High-pressure matches",
                format="%d",
                width="medium"
            ),
            "Reliability score": st.column_config.NumberColumn(
                "Reliability score",
                format="%.2f",
                width="medium"
            )
        }
    )



def section_title(title, subtitle=None):
    """Display a consistent section heading."""

    st.markdown(
        f"""
        <h2 style="
            font-family: Georgia, serif;
            font-size: 25px;
            color: #123f35;
            margin-bottom: 5px;
        ">
            {title}
        </h2>
        """,
        unsafe_allow_html=True
    )

    if subtitle:
        st.caption(subtitle)


def stat_card(label, value, description=""):
    """Display a dashboard statistic card."""

    html = f"""
    <div style="
        background-color: #fffefa;
        border: 1px solid #e5dfd2;
        border-radius: 10px;
        padding: 16px;
        min-height: 108px;
    ">
        <div style="
            font-size: 10px;
            letter-spacing: 1.5px;
            color: #81796d;
            text-transform: uppercase;
            margin-bottom: 12px;
        ">
            {label}
        </div>
        <div style="
            font-family: Georgia, serif;
            font-size: 27px;
            font-weight: bold;
            color: #123f35;
        ">
            {value}
        </div>
        <div style="
            font-size: 11px;
            color: #888078;
            margin-top: 5px;
        ">
            {description}
        </div>
    </div>
    """

    st.markdown(dedent(html), unsafe_allow_html=True)


# ---------------- OVERVIEW ----------------




if page == "Overview":

    st.header("Tournament Intelligence Overview")

    # KPI cards
    c1, c2, c3, c4 = st.columns([1, 1, 1.4, 1.5])

    c1.metric("Eligible Batters", len(batters))
    c2.metric("Eligible Bowlers", len(bowlers))
    c3.metric("Top Batter", batters.iloc[0]["striker_name"])
    c4.metric("Top Bowler", bowlers.iloc[0]["bowler_name"])

    st.divider()

    # Top 10 ranking tables
    st.subheader("Top 10 Player Rankings")

    left, right = st.columns(2, gap="medium")

    with left:
        st.markdown("**🏏 Top 10 Reliable Batters**")
        show_ranking_table(batters.head(10), "striker_name")

    with right:
        st.markdown("**🎯 Top 10 Reliable Bowlers**")
        show_ranking_table(bowlers.head(10), "bowler_name")

    st.divider()

    # Visual comparison
    st.subheader("Top Performer Comparison")

    left, right = st.columns(2, gap="medium")

    with left:
        st.markdown("**🏏 Top 10 Batters**")

        chart_bat = px.bar(
            batters.head(10).sort_values(
                "reliability_score", ascending=True
            ),
            x="reliability_score",
            y="striker_name",
            orientation="h",
            text="reliability_score",
            labels={
                "reliability_score": "Reliability Score",
                "striker_name": "Player"
            }
        )

        chart_bat.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        chart_bat.update_layout(
            xaxis_title="Reliability Score",
            yaxis_title="",
            showlegend=False
        )

        st.plotly_chart(chart_bat, use_container_width=True)

    with right:
        st.markdown("**🎯 Top 10 Bowlers**")

        chart_bowl = px.bar(
            bowlers.head(10).sort_values(
                "reliability_score", ascending=True
            ),
            x="reliability_score",
            y="bowler_name",
            orientation="h",
            text="reliability_score",
            labels={
                "reliability_score": "Reliability Score",
                "bowler_name": "Player"
            }
        )

        chart_bowl.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        chart_bowl.update_layout(
            xaxis_title="Reliability Score",
            yaxis_title="",
            showlegend=False
        )

        st.plotly_chart(chart_bowl, use_container_width=True)


# ---------------- BATTERS ----------------

elif page == "Batters":

    st.header("🏏 Batter Reliability Rankings")
    st.write(
        "Batters are evaluated using strike rate, improvement "
        "under pressure, runs scored, runs per dismissal, "
        "and boundary contribution."
    )

    search = st.text_input("Search batter")

    filtered = batters.copy()

    if search:
        filtered = filtered[
            filtered["striker_name"].str.contains(
                search, case=False, na=False
            )
        ]

    st.dataframe(
        filtered[
            [
                "rank",
                "striker_name",
                "matches_high",
                "runs_high",
                "balls_high",
                "strike_rate_high",
                "reliability_score"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    selected = st.selectbox(
        "Select a batter to inspect",
        batters["striker_name"].tolist()
    )

    player = batters[
        batters["striker_name"] == selected
    ].iloc[0]

    a, b, c, d = st.columns(4)

    a.metric("Rank", int(player["rank"]))
    b.metric("Reliability Score", round(player["reliability_score"], 2))
    c.metric("High-pressure Runs", int(player["runs_high"]))
    d.metric("Strike Rate", round(player["strike_rate_high"], 2))

    st.write(
        f"**High-pressure matches:** {int(player['matches_high'])}  "
        f"| **Balls faced:** {int(player['balls_high'])}"
    )


# ---------------- BOWLERS ----------------

elif page == "Bowlers":

    st.header("🎯 Bowler Reliability Rankings")
    st.write(
        "Bowlers are evaluated using economy, improvement "
        "under pressure, wickets, bowling average, "
        "and bowling strike rate."
    )

    search = st.text_input("Search bowler")

    filtered = bowlers.copy()

    if search:
        filtered = filtered[
            filtered["bowler_name"].str.contains(
                search, case=False, na=False
            )
        ]

    st.dataframe(
        filtered[
            [
                "rank",
                "bowler_name",
                "matches_high",
                "wickets_high",
                "legal_balls_high",
                "economy_high",
                "reliability_score"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    selected = st.selectbox(
        "Select a bowler to inspect",
        bowlers["bowler_name"].tolist()
    )

    player = bowlers[
        bowlers["bowler_name"] == selected
    ].iloc[0]

    a, b, c, d = st.columns(4)

    a.metric("Rank", int(player["rank"]))
    b.metric("Reliability Score", round(player["reliability_score"], 2))
    c.metric("Wickets", int(player["wickets_high"]))
    d.metric("Economy", round(player["economy_high"], 2))

    st.write(
        f"**High-pressure matches:** {int(player['matches_high'])}  "
        f"| **Legal balls:** {int(player['legal_balls_high'])}"
    )


# ---------------- METHODOLOGY ----------------


elif page == "Methodology":

    st.markdown(
        '<div class="eyebrow">04 / Research & methodology</div>',
        unsafe_allow_html=True
    )

    section_title(
        "The methodology behind the rankings",
        "A transparent framework for identifying reliable T20 performers under pressure."
    )

    st.markdown("""
    Royal Scout evaluates how batters and bowlers perform when a T20 chase
    becomes challenging. The analysis uses ball-by-ball data from IPL
    2022 onwards and T20 Internationals, focusing on completed,
    non-DLS/D-L second innings.
    """)

    st.markdown("---")

    # 01 — Dataset and scope
    section_title("01. Dataset and scope")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        stat_card("Deliveries", "194,014", "Eligible dataset")

    with c2:
        stat_card("Matches", "837", "Eligible matches")

    with c3:
        stat_card("Batters", "824", "Unique players")

    with c4:
        stat_card("Bowlers", "596", "Unique players")

    st.markdown("""
    **Selection criteria**

    - IPL competitions from 2022 onwards and T20 Internationals.
    - DLS/D-L, abandoned and no-result matches excluded from the
      primary chase analysis.
    - Pressure calculated before each delivery using the match
      situation at that point.
    """)

    st.markdown("---")

    # 02 — Pressure framework
    section_title("02. Identifying match pressure")

    st.markdown("""
    Pressure is defined using three factors: required run rate (RRR),
    balls remaining and wickets remaining.

    **High Pressure** — at least one condition must be satisfied:
    """)

    st.code("""
Required run rate >= 12

OR

Balls remaining <= 12
AND required run rate >= 6

OR

Wickets remaining <= 3
AND required run rate >= 8
    """)

    st.markdown("""
    **Medium Pressure** — when the delivery is not High Pressure,
    but at least one of these conditions is satisfied:
    """)

    st.code("""
Required run rate >= 9

OR

Balls remaining <= 18

OR

Wickets remaining <= 5
    """)

    st.markdown("""
    **Normal Pressure** — deliveries that satisfy neither the
    High nor Medium Pressure conditions.

    High Pressure takes priority whenever conditions overlap.
    These thresholds are analytical choices designed for this study,
    rather than universal cricket standards.
    """)

    st.markdown("---")

    # 03 — Eligibility
    section_title("03. Player eligibility")

    st.markdown("""
    To reduce the influence of limited playing exposure, the final
    rankings use the moderate sample-size requirements:
    """)

    st.dataframe(
        pd.DataFrame({
            "Requirement": [
                "High-pressure matches",
                "High-pressure balls",
                "Normal-pressure balls"
            ],
            "Minimum": [
                "8 matches",
                "60 balls",
                "30 balls"
            ]
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("""
    This produces an eligible pool of **59 batters and 97 bowlers**.
    """)

    st.markdown("---")

    # 04 — Scoring framework
    section_title("04. Reliability scoring framework")

    st.markdown("""
    Each metric is converted into a percentile score. Weighted
    percentiles are combined to produce a composite reliability
    score out of 100.
    """)

    batting_col, bowling_col = st.columns(2)

    with batting_col:
        st.markdown("**Batting score**")

        st.dataframe(
            pd.DataFrame({
                "Metric": [
                    "High-pressure strike rate",
                    "Strike-rate improvement",
                    "High-pressure runs",
                    "Runs per dismissal",
                    "Boundary percentage"
                ],
                "Weight": ["30%", "25%", "20%", "15%", "10%"]
            }),
            use_container_width=True,
            hide_index=True
        )

    with bowling_col:
        st.markdown("**Bowling score**")

        st.dataframe(
            pd.DataFrame({
                "Metric": [
                    "High-pressure economy",
                    "Economy improvement",
                    "High-pressure wickets",
                    "Bowling average",
                    "Bowling strike rate"
                ],
                "Weight": ["30%", "25%", "20%", "15%", "10%"]
            }),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("""
    Higher values receive better percentile scores for batting metrics
    and positive bowling contributions. For bowling economy, average
    and strike rate, lower values receive better scores.

    The improvement metrics compare performance under High Pressure
    with the player's Normal Pressure baseline.
    """)

    st.markdown("---")

    # 05 — Validation and robustness
    section_title("05. Validation and robustness")

    st.markdown("""
    Rankings were tested under three different minimum sample-size
    scenarios to assess their stability.
    """)

    st.dataframe(
        pd.DataFrame({
            "Scenario": ["Initial", "Moderate", "Strict"],
            "High-pressure matches": [5, 8, 10],
            "High-pressure balls": [30, 60, 90],
            "Eligible batters": [96, 59, 39],
            "Eligible bowlers": [137, 97, 76]
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("""
    **Key finding:** Rinku Singh remained the leading batter and
    Mohammad Nawaz remained the leading bowler across all three
    sample-size tests.

    **Bowling extras sensitivity:** Deliveries labelled `other`
    were tested under two legal-ball assumptions: excluded in the
    primary scenario and included in the alternative scenario.
    The displayed Top 10 bowling order remained unchanged in this
    comparison. The primary assumption is retained because the
    source classification is ambiguous.
    """)

    st.markdown("---")

    # 06 — Data treatment and limitations
    section_title("06. Data treatment and limitations")

    st.markdown("""
    **Data treatment**

    - Batter balls faced exclude wides.
    - Bowler legal balls exclude wides, Overstep and `other`
      in the primary scenario.
    - Byes and leg-byes are not charged to the bowler.
    - Penalty runs are excluded from bowler runs conceded.
    - Bowler-credited wickets include Bowled, Caught, LBW,
      Stump and Hit Wicket.
    - Batter dismissals use the actual dismissed-player ID,
      including non-striker run-outs.
    """)

    st.markdown("""
    **Limitations and interpretation**

    - Pressure thresholds and metric weights are analytical choices;
      different choices may produce different rankings.
    - The Normal Pressure baseline includes only normal-pressure
      second-innings chase deliveries, not all T20 innings.
    - One wicket record lacked a dismissed-player ID and could
      not be assigned to a batter.
    - The `other` extras category is ambiguous in the source data.
    - Composite scores are relative to the eligible player pool.
      They are not probabilities of winning or predictions of
      future performance.
    - Results are limited to the competitions and seasons supplied
      in the dataset.
    """)

    st.markdown("---")

    st.markdown("""
    **Research principle**

    Royal Scout uses historical match evidence to identify
    performance under pressure. The rankings are intended to
    support cricket analysis, not replace the broader evaluation
    of a player's ability.
    """)
