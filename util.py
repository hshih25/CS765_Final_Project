from collections import defaultdict

import pandas as pd
import streamlit as st




def read_data():
    df = pd.read_csv("atussum_0321-reduced.csv")
    temp = list(df.columns)
    temp[temp.index('TESEX')] = "Sex"
    temp[temp.index('TEAGE')] = "Age"
    temp[temp.index('TESPEMPNOT')] = "Employment"
    temp[temp.index('TRSPPRES')] = "Single"
    temp[temp.index('PTDTRACE')] = "Race"
    df.columns = temp
    return df


def draw(fig):
    if len(fig) == 1:
        with st.container():
            st.pyplot(fig[0])
        return 0

def generate_tables(category_groups):
    category_group = category_groups[0]
    col_names = category_group.keys()
    table_data = defaultdict(list)
    for col_name in col_names:
        for category_group in category_groups:
            table_data[col_name].append(category_group[col_name])

    return pd.DataFrame(table_data)


def presentation_scope_adapter(variable):
    if variable == "T01_Personal Care Activities":
        return "t01"
    elif variable == "T05_Work & Work-Related Activities":
        return "t05"
    elif variable == "T12_Socializing, Relaxing, and Leisure":
        return "t12"

def categorical_scope_adapter(categorical_scopes, modify_dict):
    for categorical_scope in categorical_scopes:
        modify_dict[categorical_scope] = True