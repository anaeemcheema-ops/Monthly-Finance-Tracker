import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state for storing data
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Type", "Category", "Amount", "Due Date"]
    )

st.title("💰 Monthly Finance Tracker")

# Sidebar for adding new entries
st.sidebar.header("Add Income/Expense")

entry_type = st.sidebar.selectbox("Type", ["Income", "Expense"])
category = st.sidebar.text_input("Category (e.g., Salary, Rent, Food)")
amount = st.sidebar.number_input("Amount", min_value=0.0, step=0.01)
due_date = st.sidebar.date_input("Due Date")

if st.sidebar.button("Add Entry"):
    new_entry = {"Type": entry_type, "Category": category,
                 "Amount": amount, "Due Date": due_date}
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_entry])],
        ignore_index=True
    )
    st.sidebar.success("Entry added!")

# Display data
st.subheader("📊 Finance Data")
if not st.session_state.data.empty:
    st.dataframe(st.session_state.data)

    # Summary
    income = st.session_state.data[st.session_state.data["Type"] == "Income"]["Amount"].sum()
    expenses = st.session_state.data[st.session_state.data["Type"] == "Expense"]["Amount"].sum()
    balance = income - expenses

    st.metric("Total Income", f"${income:,.2f}")
    st.metric("Total Expenses", f"${expenses:,.2f}")
    st.metric("Balance", f"${balance:,.2f}")

    # Visualization
    st.subheader("📈 Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        st.session_state.data.groupby("Type")["Amount"].sum().plot(kind="bar", ax=ax)
        ax.set_ylabel("Amount")
        ax.set_title("Income vs Expenses")
        st.pyplot(fig)

    with col2:
        expense_data = st.session_state.data[st.session_state.data["Type"] == "Expense"]
        if not expense_data.empty:
            fig, ax = plt.subplots()
            expense_data.groupby("Category")["Amount"].sum().plot(
                kind="pie", autopct="%1.1f%%", ax=ax
            )
            ax.set_ylabel("")
            ax.set_title("Expenses Breakdown")
            st.pyplot(fig)

else:
    st.info("No data yet. Add income or expenses from the sidebar.")

# Reset button
if st.button("Reset Data"):
    st.session_state.data = pd.DataFrame(
        columns=["Type", "Category", "Amount", "Due Date"]
    )
    st.success("Data reset!")
