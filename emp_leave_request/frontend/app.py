import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import date

API_URL = "http://127.0.0.1:8000"
st.markdown("""
<style>

.main-title {
    font-size: 36px;
    font-weight: bold;
    color: #4F46E5;
}

div.stButton > button {
    width: 100%;
    height: 45px;
    border-radius: 10px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

USERS = {
    "sakthi": {
        "password": "emp123",
        "role": "Employee",
        "name": "Sakthi"
    },
    "hayden": {
        "password": "emp123",
        "role": "Employee",
        "name": "Hayden"
    },
    "smith": {
        "password": "mgr123",
        "role": "Manager",
        "name": "Smith"
    }
}

st.set_page_config(page_title="Employee Leave Management", page_icon="🗓️", layout="wide")

st.markdown("""
<style>
.main-title {
    font-size: 36px;
    font-weight: bold;
    color: #4F46E5;
}
</style>
""", unsafe_allow_html=True)


def get_statistics():
    try:
        response = requests.get(f"{API_URL}/statistics")
        if response.status_code == 200:
            return response.json()
        st.error(f"Backend API error: {response.status_code}")
        st.write(response.text)
        st.stop()
    except Exception as e:
        st.error("Backend is not running.")
        st.write(e)
        st.stop()


def get_employees():
    try:
        response = requests.get(f"{API_URL}/employees")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []


def get_all_leaves():
    try:
        response = requests.get(f"{API_URL}/leave/all")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []


def login_page():

    st.markdown("""
    <h1 style='text-align:center;color:#4F46E5;'>
        Employee Leave Management
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h4 style='text-align:center;color:gray;'>
        Sign in to continue
    </h4>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    left, center, right = st.columns([1, 2, 1])

    with center:

        username = st.text_input(
            "Username",
            placeholder="Enter Username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter Password"
        )

        st.write("")

        login_clicked = st.button(
            "Login",
            use_container_width=True
        )

    if login_clicked:

        username = username.strip().lower()
        password = password.strip()

        if username in USERS and USERS[username]["password"] == password:

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = USERS[username]["role"]
            st.session_state.name = USERS[username]["name"]

            st.rerun()

        else:
            st.error("Invalid username or password")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
    st.stop()


st.sidebar.success(f"Logged in as: {st.session_state.name}")
st.sidebar.write(f"Role: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

st.markdown("""<h1 style='text-align:center;color:#4F46E5;'>Employee Leave Management </h1>x""", unsafe_allow_html=True)

if st.session_state.role == "Employee":
    menu = st.sidebar.radio("Navigation", ["Employee Dashboard", "Apply Leave", "Leave History"])
else:
    menu = st.sidebar.radio("Navigation", ["Manager Approval", "Employee Details", "Leave Statistics"])


if menu == "Employee Dashboard":
    st.subheader("Employee Dashboard")

    stats = get_statistics()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Leaves", stats["total"])
    col2.metric("Approved", stats["approved"])
    col3.metric("Pending", stats["pending"])
    col4.metric("Rejected", stats["rejected"])

    st.divider()

    leaves = get_all_leaves()
    if leaves:
        df = pd.DataFrame(leaves)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No leave records found.")


elif menu == "Apply Leave":
    st.subheader("Apply Leave")

    employees = get_employees()

    if not employees:
        st.warning("Please ask manager to add employee first.")
    else:
        emp_names = {f"{emp['name']} - {emp['department']}": emp for emp in employees}

        selected = st.selectbox("Select Employee", list(emp_names.keys()))
        emp = emp_names[selected]

        leave_type = st.selectbox(
            "Leave Type",
            ["Casual Leave", "Sick Leave", "Earned Leave", "Work From Home", "Emergency Leave"]
        )

        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", date.today())
        end_date = col2.date_input("End Date", date.today())

        reason = st.text_area("Reason")

        if st.button("Submit Leave Request"):
            if end_date < start_date:
                st.error("End date should not be before start date.")
            elif reason.strip() == "":
                st.error("Please enter reason.")
            else:
                payload = {
                    "employee_id": emp["id"],
                    "employee_name": emp["name"],
                    "leave_type": leave_type,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "reason": reason
                }

                res = requests.post(f"{API_URL}/leave/apply", json=payload)

                if res.status_code == 200:
                    st.success("Leave request submitted successfully.")
                else:
                    st.error("Something went wrong.")


elif menu == "Leave History":
    st.subheader("Leave History")

    employees = get_employees()

    if not employees:
        st.warning("No employees found.")
    else:
        emp_names = {f"{emp['name']} - {emp['department']}": emp for emp in employees}

        selected = st.selectbox("Select Employee", list(emp_names.keys()))
        emp = emp_names[selected]

        try:
            response = requests.get(f"{API_URL}/leave/employee/{emp['id']}")
            leaves = response.json() if response.status_code == 200 else []
        except:
            leaves = []

        if leaves:
            df = pd.DataFrame(leaves)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No leave history found.")


elif menu == "Manager Approval":
    st.subheader("Manager Approval Dashboard")

    leaves = get_all_leaves()

    if leaves:
        pending_leaves = [leave for leave in leaves if leave["status"] == "Pending"]

        if pending_leaves:
            for leave in pending_leaves:
                with st.container(border=True):
                    st.write(f"**Employee:** {leave['employee_name']}")
                    st.write(f"**Leave Type:** {leave['leave_type']}")
                    st.write(f"**From:** {leave['start_date']}")
                    st.write(f"**To:** {leave['end_date']}")
                    st.write(f"**Reason:** {leave['reason']}")

                    col1, col2 = st.columns(2)

                    if col1.button("Approve", key=f"approve_{leave['id']}"):
                        requests.put(f"{API_URL}/leave/{leave['id']}/approve")
                        st.success("Leave approved.")
                        st.rerun()

                    if col2.button("Reject", key=f"reject_{leave['id']}"):
                        requests.put(f"{API_URL}/leave/{leave['id']}/reject")
                        st.error("Leave rejected.")
                        st.rerun()
        else:
            st.info("No pending leave requests.")
    else:
        st.info("No leave requests found.")


elif menu == "Employee Details":
    st.subheader("Employee Details")

    with st.form("employee_form"):
        name = st.text_input("Employee Name")
        email = st.text_input("Email")
        role = st.selectbox("Role", ["Employee", "Manager", "HR"])
        department = st.selectbox("Department", ["IT", "HR", "Finance", "Sales", "Support", "Admin"])

        submitted = st.form_submit_button("Add Employee")

        if submitted:
            if name.strip() == "" or email.strip() == "":
                st.error("Name and email are required.")
            else:
                payload = {
                    "name": name,
                    "email": email,
                    "role": role,
                    "department": department
                }

                res = requests.post(f"{API_URL}/employees", json=payload)

                if res.status_code == 200:
                    st.success("Employee added successfully.")
                else:
                    st.error("Failed to add employee.")

    st.divider()

    employees = get_employees()

    if employees:
        df = pd.DataFrame(employees)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No employees found.")


elif menu == "Leave Statistics":
    st.subheader("Leave Statistics")

    stats = get_statistics()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", stats["total"])
    col2.metric("Approved", stats["approved"])
    col3.metric("Pending", stats["pending"])
    col4.metric("Rejected", stats["rejected"])

    chart_data = pd.DataFrame({
        "Status": ["Approved", "Pending", "Rejected"],
        "Count": [stats["approved"], stats["pending"], stats["rejected"]]
    })

    fig = px.pie(chart_data, names="Status", values="Count", title="Leave Status Chart")
    st.plotly_chart(fig, use_container_width=True)