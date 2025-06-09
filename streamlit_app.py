import streamlit as st
import pandas as pd
from dateutil import parser
from io import StringIO
import base64

st.set_page_config(page_title="CleanCart - CSV Cleaner", layout="centered")

st.title("🧹 CleanCart")
st.markdown("Upload your messy CSV file and get a cleaned version with a full report!")

def clean_csv(file):
    df = pd.read_csv(file)
    report = []

    report.append(f"Original shape: {df.shape}")
    # Remove duplicates
    before = df.shape[0]
    df = df.drop_duplicates()
    report.append(f"Removed {before - df.shape[0]} duplicate rows.")

    # Fill blank cells
    blanks = df.isnull().sum().sum()
    df.fillna("MISSING", inplace=True)
    report.append(f"Filled {blanks} blank cells with 'MISSING'.")

    # Date normalization
    date_cols = []
    for col in df.columns:
        try:
            parsed = df[col].apply(lambda x: parser.parse(str(x), fuzzy=True) if x != "MISSING" else x)
            if all(isinstance(x, (pd.Timestamp, str)) for x in parsed):
                df[col] = parsed.apply(lambda x: x.strftime("%Y-%m-%d") if isinstance(x, pd.Timestamp) else x)
                date_cols.append(col)
        except Exception:
            continue

    if date_cols:
        report.append(f"Standardized date format in: {', '.join(date_cols)}")
    else:
        report.append("No date columns found to standardize.")

    return df, "\n".join(report)

def generate_download_link(df, filename, label):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{label}</a>'
    return href

def generate_text_download(report, filename, label):
    b64 = base64.b64encode(report.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="{filename}">{label}</a>'
    return href

uploaded_file = st.file_uploader("📄 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        cleaned_df, report = clean_csv(uploaded_file)

        st.success("✅ File cleaned successfully!")

        st.subheader("📊 Preview of Cleaned Data")
        st.dataframe(cleaned_df.head())

        st.subheader("📝 Cleaning Report")
        st.text(report)

        st.markdown(generate_download_link(cleaned_df, "cleaned_data.csv", "⬇️ Download Cleaned CSV"), unsafe_allow_html=True)
        st.markdown(generate_text_download(report, "cleaning_report.txt", "⬇️ Download Cleaning Report"), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
