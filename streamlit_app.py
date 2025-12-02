import streamlit as st
import requests
import pandas as pd

API_URL = "https://aimind-mongodb-api.onrender.com" 

st.title("Customers Database")

# ------------------------
# Insert ONE record
# ------------------------
st.subheader("Insert One Customer")
id_ = st.number_input("Customer ID", min_value=1)
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=100)
loc = st.text_input("Location")

if st.button("Insert-One"):
    payload = {
        "id": id_,
        "name":name,
        "age": age,
        "loc": loc

    }
    res = requests.post(f"{API_URL}/insert-one",json=payload)
    st.success("Record inseted successfully")

# ------------------------
# Insert MANY customers
# ------------------------
st.subheader("Insert Many Customers")   

many_input = st.text_area(
    "Enter list of customers (JSON array format)",
    """
[
  {"id":1,"name":"alice","age":18,"loc":"delhi"},
  {"id":2,"name":"mike","age":30,"loc":"dallas"}
]
"""
)
if st.button("Insert Many"):
    try:
        data =eval(many_input)
        res = requests.post(f"{API_URL}/insert-many",json=data)
        st.success("All records inserted successfully")
    except Exception as e:
        st.error("Invalid JSON input!")

# ------------------------
# View ALL customers
# ------------------------
st.subheader("View All Customers")

if st.button("Fetch All"):
     res = requests.get(f"{API_URL}/all-data")
     data = res.json()["data"]
     df = pd.DataFrame(data)
     st.dataframe(df)


