from collections import defaultdict

import pandas as pd
import streamlit as st


category_level_dict = {
    "Sex": {
        1: "Male",
        2: "Female",
    },
    "Employment": {
        1: "Employed",
        2: "Unemployed",
    },
    "Single": {
        1: "Spourse present",
        2: "Unmarried partner present",
        3: "Single",
    },
    "Race": {
        1: "White",
        2: "Black",
        4: "Asian",
    },
}






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

def generate_tables(category_groups, df):
    category_group = category_groups[0]
    col_names = category_group.keys()
    table_data = defaultdict(list)
    for col_name in col_names:
        for category_group in category_groups:
            if col_name != "Age":
                table_data[col_name].append(category_level_dict[col_name][category_group[col_name]])
            else:
                table_data[col_name].append(category_group[col_name])
    for idx in range(len(category_groups)):
        table_data["Sample size"].append(len(df[df['group_column'] == idx]))

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