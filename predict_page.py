import streamlit as st
import pickle
import numpy as np

#we need to load our model here so lets create a function:
def load_model():
    with open("saved_steps.pkl","rb") as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_encoder = data["le_education"]

def show_predict_page():

    #this will give the title to the web page
    st.title("Data Scientist Salary Prediction")

    #using 3 # means heading3
    st.write("""Please input the below information to predict the salary:""")


    #We will add 2 boxes for country and education:
    country = (
        "United States of America",
        "India",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "Canada",
        "France",
        "Brazil",
        "Spain",
        "Netherlands",
        "Australia",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
        "Turkey",
        "Switzerland",
        "Israel",
        "Norway"
    )

    education = (
        "Bachelor’s degree",
        "Less than a Bachelors",
        "Master degree",
        "Pro Degree"
    )

    country = st.selectbox("Country",country)
    education = st.selectbox("Education",education)
    experience = st.slider("Years of Coding Experience",0,50,1)

    #add a button to start on website to start prediction
    ok = st.button("Calculate Salary")

    if ok:
        X = np.array([[country,education,experience]])
        X[:,0] = le_country.transform(X[:,0])
        X[:,1] = le_encoder.transform(X[:,1])
        X  = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")