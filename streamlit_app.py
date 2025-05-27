import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Police Resource Allocation Dashboard")
st.markdown("This dashboard shows recommended police deployment hours based on predicted burglary risk.")

# Sample data (you can later load this from a CSV instead)
data = [
    {"Area Code": "E01000005", "Ward Code": "E05009333", "Hours": 39.4, "Risk": 91},
    {"Area Code": "E01000006", "Ward Code": "E05000035", "Hours": 73.1, "Risk": 18},
    {"Area Code": "E01000008", "Ward Code": "E05000487", "Hours": 215.0, "Risk": 190},
    {"Area Code": "E01000009", "Ward Code": "E05000035", "Hours": 475.1, "Risk": 117},
    {"Area Code": "E01000013", "Ward Code": "E05000027", "Hours": 279.3, "Risk": 147},
    {"Area Code": "E01000014", "Ward Code": "E05000037", "Hours": 283.5, "Risk": 112}
]

df = pd.DataFrame(data)

# Filters
min_risk = st.slider("Minimum Risk Level", min_value=0, max_value=200, value=0)
filtered_df = df[df["Risk"] >= min_risk]

# Table
st.subheader("Deployment Recommendations")
st.dataframe(filtered_df)

# Bar chart
fig = px.bar(filtered_df, x="Area Code", y="Hours", color="Risk", title="Police Hours by Area Code")
st.plotly_chart(fig)

#nice