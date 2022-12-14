# Loading libraries
import warnings
import streamlit as st

apptitle = "CS765 Final Project"
st.set_page_config(page_title=apptitle, page_icon=":heavy_check_mark:")


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