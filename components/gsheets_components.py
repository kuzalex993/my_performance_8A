
import streamlit as st
import pandas as pd



def add_new_record(table_name: str, values_to_add: list, conn, rerun=True):
    data_from_gsh = conn.read(worksheet=table_name)
    data_from_gsh = data_from_gsh.dropna(subset=[f"{table_name}_id"])
    next_id = data_from_gsh[f"{table_name}_id"].max() + 1
    for row in values_to_add:
        row[f"{table_name}_id"] = next_id
        new_row = pd.DataFrame([row])
        data_from_gsh = pd.concat([data_from_gsh, new_row], ignore_index=True)
        next_id += 1

    response = conn.update(worksheet=table_name, data=data_from_gsh)
    if rerun:
        st.cache_data.clear()
        st.rerun()
    print(response)


def update_table_in_db(table_name: str, df: pd.DataFrame, conn, rerun=True):
    response = conn.update(worksheet=table_name, data=df)
    if rerun:
        st.cache_data.clear()
        st.rerun()
    print(response)
