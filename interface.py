# Loading libraries
import warnings
from collections import defaultdict

import pandas as pd
import streamlit as st

from core import *
from util import *


apptitle = "CS765 Final Project"
st.set_page_config(page_title=apptitle, page_icon=":heavy_check_mark:")

df = read_data()

categorical_scope_dict = {
    "Sex": False,
    "Race": False,
    "Employment": False,
    "Age": False,
    "Single": False,
}

category_list = [
    "Sex",
    "Race",
    "Employment",
    "Age",
    "Single",
]


present_list = [
    "T01_Personal Care Activities",
    "T05_Work & Work-Related Activities",
    "T12_Socializing, Relaxing, and Leisure",
]

# streamlit interface

st.sidebar.markdown("## Grouping Helper")

categorical_scope = st.sidebar.multiselect(
    label="Select Categorical Variables",
    options=category_list,
    default=[category_list[0], category_list[1], category_list[3]]
)

# Display warning messages
if len(categorical_scope) == 0:
    warnings.warn("No categorical variables are selected!")
    st.markdown(
        "<p style='color:red;'>WARNING: </p>Please select categorical variables to begin!",
        unsafe_allow_html=True,
    )

presentation_scope = st.sidebar.multiselect(
    label="Select Presentation Variables",
    options=present_list,
    default=[present_list[0]]
)

if len(presentation_scope) == 0:
    warnings.warn("No Presentation variables are selected!")
    st.markdown(
        "<p style='color:red;'>WARNING: </p>Please select Presentation variables to begin!",
        unsafe_allow_html=True,
    )


max_value = st.sidebar.number_input(
    label = 'Max sample Size',
    min_value = 0
)

min_value = st.sidebar.number_input(
    label = 'Min sample Size',
    min_value = 0
)


if max_value < min_value and max != 0:
    warnings.warn("Min value cannot greater than max")
    st.markdown(
        "<p style='color:red;'>WARNING: </p>Please select correct min value to begin!",
        unsafe_allow_html=True,
    )


categorical_scope_adapter(categorical_scope, categorical_scope_dict)
check_model = CheckSampleSizeModel(data=df, user_selected=categorical_scope_dict, min_sample_size=min_value)

check_result = check_model.validate_sample_size()
if check_result["msg"] != "valid":
    warnings.warn("The number of sample size in one or more than one group is out of the sample size limit.")
    st.markdown(
        "<p style='color:red;'>WARNING: </p>Please reduce the number of category or modify the sample size limit!",
        unsafe_allow_html=True,
    )
else:
    plot_data = check_model.get_group_data()
    presentation_list = [presentation_scope_adapter(i) for i in presentation_scope]
    vis = Vis(data=plot_data['data'], category_group=plot_data['category_group'], dependent=presentation_list, bin_num=10)
    fig = vis.distribution_plot()
    draw(fig)

    # input_group_column, presentation_column = st.columns([1, 1])
    input_group_column, presentation_column = st.columns([1, 1])
    input_group_column.caption("Current Group Levels")
    display_category_group = generate_tables(plot_data['category_group'])
    input_group_column.write(display_category_group)

