import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Battery Analytics", page_icon="🔋", layout="wide")

# ---------------- MODERN THEME ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp{
    background:
    radial-gradient(circle at top left, rgba(59,130,246,.18), transparent 25%),
    radial-gradient(circle at bottom right, rgba(168,85,247,.15), transparent 25%),
    linear-gradient(135deg,#020617,#071124,#0f172a);
    color:white;
}

section[data-testid="stSidebar"]{
    background:rgba(15,23,42,.7);
    backdrop-filter:blur(10px);
}

[data-testid="metric-container"]{
    background:rgba(15,23,42,.7);
    border:1px solid rgba(255,255,255,.08);
    border-radius:16px;
    padding:15px;
}

.stButton>button{
    background:linear-gradient(135deg,#2563eb,#7c3aed);
    color:white;
    border:none;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def health_score(v,t,c,d,cur):
    score=((v/4.2)*40)+(((50-t)/50)*20)+(((500-c)/500)*20)+(((120-d)/120)*10)+(((3-cur)/3)*10)
    return round(max(0,min(100,score)),2)

def donut(value,label):
    fig=go.Figure(go.Pie(
        values=[value,100-value],
        hole=.86,
        sort=False,
        direction='clockwise',
        marker=dict(colors=["#38bdf8","#1e293b"])
    ))

    fig.update_layout(
        height=400,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=0,b=0,l=0,r=0),
        annotations=[
            dict(text=f"{value}%", x=0.5, y=0.53, showarrow=False,
                 font=dict(size=42,color="white")),
            dict(text=label, x=0.5, y=0.43, showarrow=False,
                 font=dict(size=15,color="#94a3b8"))
        ]
    )
    return fig

def style(fig,x,y):
    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        template="plotly_dark",
        paper_bgcolor="rgba(15,23,42,.7)",
        plot_bgcolor="rgba(15,23,42,.7)",
        font=dict(family="Space Grotesk",color="white")
    )
    return fig

# ---------------- TITLE ----------------
st.title("Smart Battery Analytics Dashboard")

st.write("""
Upload a battery CSV containing:
- Voltage
- Temperature
- Charge Cycles
- Current
- Charging Duration
""")

file = st.file_uploader("Upload CSV", type="csv")

# ---------------- MAIN APP ----------------
if file:

    df = pd.read_csv(file)
    df.columns = [i.replace("_"," ").title() for i in df.columns]
    df["Reading Number"] = range(1, len(df)+1)

    # ---------------- IDEAL BATTERY DATA ----------------
    n = len(df)

    ideal_df = pd.DataFrame({
        "Reading Number": range(1, n+1),
        "Voltage": [4.1]*n,
        "Temperature": [30]*n,
        "Charge Cycles": df["Charge Cycles"],
        "Current": [1.0]*n,
        "Charging Duration": [60]*n
    })

    avg_v = df["Voltage"].mean()
    avg_t = df["Temperature"].mean()
    max_c = df["Charge Cycles"].max()
    avg_cur = df["Current"].mean()
    avg_d = df["Charging Duration"].mean()

    battery = health_score(avg_v, avg_t, max_c, avg_d, avg_cur)

    page = st.sidebar.radio("Navigation",
        ["Overview","Dataset","Graphs","Predictor","Insights"])

    # ---------------- OVERVIEW ----------------
    if page == "Overview":

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Voltage", f"{avg_v:.2f} V")
        c2.metric("Temperature", f"{avg_t:.1f} °C")
        c3.metric("Charge Cycles", int(max_c))
        c4.metric("Charging Duration", f"{avg_d:.1f} min")

        st.plotly_chart(donut(battery,"Battery Health"), use_container_width=True)

        if battery >= 85:
            st.success("Battery Condition: Excellent")
        elif battery >= 65:
            st.warning("Battery Condition: Moderate")
        else:
            st.error("Battery Condition: Critical")

    # ---------------- DATASET ----------------
    elif page == "Dataset":
        st.dataframe(df, use_container_width=True)
        st.write(df.describe())

    # ---------------- GRAPHS ----------------
    elif page == "Graphs":

        st.subheader("Real vs Ideal Battery Comparison")

        c1,c2 = st.columns(2)

        with c1:
            fig1 = px.line(df, x="Reading Number", y="Voltage",
                           markers=True, title="Actual Voltage Trend")
            fig1.update_traces(line=dict(color="#38bdf8", width=4))
            st.plotly_chart(style(fig1,"Cycle","Voltage (V)"),
                            use_container_width=True)

        with c2:
            fig1_i = px.line(ideal_df, x="Reading Number", y="Voltage",
                             markers=True, title="Ideal Voltage Trend")
            fig1_i.update_traces(line=dict(color="#22c55e", width=4))
            st.plotly_chart(style(fig1_i,"Cycle","Voltage (V)"),
                            use_container_width=True)

        c1,c2 = st.columns(2)

        with c1:
            fig2 = px.area(df, x="Reading Number", y="Temperature",
                           title="Actual Temperature")
            fig2.update_traces(line=dict(color="#f97316", width=3))
            st.plotly_chart(style(fig2,"Cycle","Temperature (°C)"),
                            use_container_width=True)

        with c2:
            fig2_i = px.line(ideal_df, x="Reading Number", y="Temperature",
                             title="Ideal Temperature")
            fig2_i.update_traces(line=dict(color="#22c55e", width=3))
            st.plotly_chart(style(fig2_i,"Cycle","Temperature (°C)"),
                            use_container_width=True)

        c1,c2 = st.columns(2)

        with c1:
            fig3 = px.scatter(
                df,
                x="Charge Cycles",
                y="Voltage",
                color="Temperature",
                size="Current",
                hover_data=["Charging Duration"],
                title="Actual: Cycles vs Voltage"
            )
            st.plotly_chart(style(fig3,"Charge Cycles","Voltage (V)"),
                            use_container_width=True)

        with c2:
            fig3_i = px.scatter(
                ideal_df,
                x="Charge Cycles",
                y="Voltage",
                color="Temperature",
                size="Current",
                title="Ideal: Cycles vs Voltage"
            )
            st.plotly_chart(style(fig3_i,"Charge Cycles","Voltage (V)"),
                            use_container_width=True)

    # ---------------- PREDICTOR ----------------
    elif page == "Predictor":

        c1,c2 = st.columns(2)

        with c1:
            v = st.slider("Voltage",3.0,5.0,4.0)
            t = st.slider("Temperature",20,60,30)
            c = st.slider("Charge Cycles",0,1000,200)

        with c2:
            cur = st.slider("Current",0.5,5.0,1.5)
            d = st.slider("Charging Duration",10,200,60)

        if st.button("Predict Battery Health"):
            pred = health_score(v,t,c,d,cur)
            st.plotly_chart(donut(pred,"Predicted Health"), use_container_width=True)

    # ---------------- INSIGHTS ----------------
    elif page == "Insights":

        st.subheader("Battery Insights")

        if avg_t < 40:
            st.success("Temperature is within safe range.")
        else:
            st.error("High temperature detected.")

        if max_c < 350:
            st.success("Charge cycle count is healthy.")
        else:
            st.warning("Battery degradation likely due to cycles.")

        if avg_v > 3.7:
            st.success("Voltage levels are stable.")
        else:
            st.warning("Voltage is below optimal.")

        st.info("Recommendation: Avoid overheating and overcharging.")

else:
    st.warning("Upload a CSV file to begin.")