import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Initialize session state for data storage
if "finance_data" not in st.session_state:
    st.session_state.finance_data = pd.DataFrame(columns=["Type", "Amount", "Category", "Due Date"])

st.set_page_config(page_title="Monthly Finance Tracker", page_icon="💰", layout="centered")

st.title("🏠 Monthly Finance Tracker")

# --- Input form ---
with st.form("entry_form"):
    col1, col2 = st.columns(2)
    with col1:
        entry_type = st.radio("Type", ["Income", "Expense"])
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    with col2:
        category = st.text_input("Category (e.g., Rent, Salary, Food)")
        due_date = st.text_input("Due Date (YYYY-MM-DD)")

    submitted = st.form_submit_button("➕ Add Entry")
    if submitted:
        if amount > 0 and category.strip() != "":
            new_entry = {"Type": entry_type, "Amount": amount, "Category": category, "Due Date": due_date}
            st.session_state.finance_data = pd.concat(
                [st.session_state.finance_data, pd.DataFrame([new_entry])],
                ignore_index=True
            )
            st.success("Entry added!")
        else:
            st.warning("Please enter a valid amount and category.")

# Reset button
if st.button("🔄 Reset All Data"):
    st.session_state.finance_data = pd.DataFrame(columns=["Type", "Amount", "Category", "Due Date"])
    st.success("All data has been reset!")

st.markdown("---")

# --- Show data table ---
st.subheader("📋 Entries")
st.dataframe(st.session_state.finance_data, use_container_width=True)

# --- Summary section ---
income = st.session_state.finance_data[st.session_state.finance_data["Type"] == "Income"]["Amount"].sum()
expenses = st.session_state.finance_data[st.session_state.finance_data["Type"] == "Expense"]["Amount"].sum()
balance = income - expenses

st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Income", f"${income:,.2f}")
col2.metric("💸 Total Expenses", f"${expenses:,.2f}")
col3.metric("🏦 Balance", f"${balance:,.2f}")

# --- Charts ---
if not st.session_state.finance_data.empty:
    grouped = st.session_state.finance_data.groupby(["Type", "Category"])["Amount"].sum().unstack(fill_value=0)

    st.subheader("📈 Income vs Expenses by Category")
    st.bar_chart(grouped)

    expenses_by_cat = st.session_state.finance_data[st.session_state.finance_data["Type"] == "Expense"].groupby("Category")["Amount"].sum()
    if not expenses_by_cat.empty:
        st.subheader("🥧 Expense Distribution")
        fig, ax = plt.subplots()
        expenses_by_cat.plot(kind="pie", autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)
