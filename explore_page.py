import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories,cuttoff):
    categorical_map = {}

    for i in range(len(categories)):
        if categories.values[i]> cuttoff:
            categorical_map[categories.index[i]]=categories.index[i]
        else:
            categorical_map[categories.index[i]]="Others"
    return categorical_map


def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)

def clean_education(x):
    if "Bachelor’s degree (B.A., B.S., B.Eng., etc.)" in x:
        return "Bachelor’s degree"
    if 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)' in x:
        return "Master degree"
    if 'Professional degree (JD, MD, etc.)' in x:
        return "Pro Degree"
    return "Less than a Bachelors"

@st.cache  # Once data is loaded and refresh the page, it save dataset in memory.
def load_data():
    df = pd.read_csv(r"D:\project\survey_results_public.csv")
    df = df[["Country","EdLevel","YearsCode","Employment","ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly":"Salary"}, axis=1)
    df = df.dropna()
    df = df[df["Employment"]=="Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df.Country.map(country_map)
    df = df[df["Salary"]<=250000]
    df = df[df["Salary"]>=100000]
    df = df[df["Country"]!="Others"]
    df["YearsCode"] = df["YearsCode"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    
    return df

df = load_data()

def show_explore_page():
    st.title("Visual Representation of the Data Scientist Salaries")

    data = df["Country"].value_counts()[:5]

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, startangle=90, autopct="%1.1f%%")
    # ax1.axis("equal")

    st.write("""Max Data Scientist Jobs as per Country""")

    st.pyplot(fig1)

    
    st.write("Mean Salary of Data Scientist as per Countries")
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("Salary VS Experience")
    data = df.groupby(["YearsCode"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)