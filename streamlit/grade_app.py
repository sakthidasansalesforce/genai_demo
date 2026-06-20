import streamlit as st

st.set_page_config(
    page_title="Grade Calculator",
    page_icon="🎓",
    layout="centered"
)

def calculate_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"

st.title("🎓 Student Grade Calculator")

st.write("Please enter the mark between 0 and 100, then click Submit.")

with st.form("grade_form"):
    mark = st.number_input(
        "Enter Mark",
        min_value=0,
        max_value=100,
        value=0,
        step=1,
        help="Please enter the mark between 0 and 100."
    )

    submitted = st.form_submit_button("Submit")

if submitted:
    grade = calculate_grade(mark)

    st.success("Grade calculated successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Entered Mark", mark)

    with col2:
        st.metric("Grade", grade)

    st.markdown("### Grade Scale")

    st.table({
        "Mark Range": ["90-100", "80-89", "70-79", "60-69", "Below 60"],
        "Grade": ["A", "B", "C", "D", "E"]
    })