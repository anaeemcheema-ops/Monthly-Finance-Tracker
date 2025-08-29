import pandas as pd
import matplotlib.pyplot as plt
import gradio as gr

# Global DataFrame to store finances
finance_data = pd.DataFrame(columns=["Type", "Amount", "Category", "Due Date"])

def add_entry(entry_type, amount, category, due_date):
    global finance_data
    new_entry = {"Type": entry_type, "Amount": amount, "Category": category, "Due Date": due_date}
    finance_data = pd.concat([finance_data, pd.DataFrame([new_entry])], ignore_index=True)
    return finance_data, calculate_summary(), generate_bar_chart(), generate_pie_chart()

def calculate_summary():
    income = finance_data[finance_data["Type"] == "Income"]["Amount"].sum()
    expenses = finance_data[finance_data["Type"] == "Expense"]["Amount"].sum()
    balance = income - expenses
    summary = f"💰 Total Income: {income}\n💸 Total Expenses: {expenses}\n📊 Balance: {balance}"
    return summary

def generate_bar_chart():
    if finance_data.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(6,4))
    grouped = finance_data.groupby(["Type", "Category"])["Amount"].sum().unstack(fill_value=0)
    grouped.T.plot(kind="bar", ax=ax)
    
    plt.title("Income vs Expenses by Category")
    plt.ylabel("Amount")
    plt.xlabel("Category")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def generate_pie_chart():
    if finance_data.empty:
        return None
    
    expenses = finance_data[finance_data["Type"] == "Expense"].groupby("Category")["Amount"].sum()
    if expenses.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(5,5))
    expenses.plot(kind="pie", autopct='%1.1f%%', ax=ax)
    plt.title("Expense Distribution by Category")
    plt.ylabel("")
    plt.tight_layout()
    return fig

def reset_data():
    global finance_data
    finance_data = pd.DataFrame(columns=["Type", "Amount", "Category", "Due Date"])
    return finance_data, "Data reset! Add new entries.", None, None

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🏠 Monthly Finance Tracker with Charts")
    
    with gr.Row():
        entry_type = gr.Radio(["Income", "Expense"], label="Type", value="Income")
        amount = gr.Number(label="Amount")
    
    with gr.Row():
        category = gr.Textbox(label="Category (e.g., Rent, Salary, Food)")
        due_date = gr.Textbox(label="Due Date (e.g., 2025-09-05)")
    
    add_btn = gr.Button("Add Entry")
    reset_btn = gr.Button("Reset Data")
    
    finance_table = gr.DataFrame(headers=["Type", "Amount", "Category", "Due Date"], interactive=False)
    summary_box = gr.Textbox(label="Summary", interactive=False)
    bar_chart = gr.Plot(label="Bar Chart: Income vs Expenses by Category")
    pie_chart = gr.Plot(label="Pie Chart: Expense Distribution")
    
    add_btn.click(add_entry, inputs=[entry_type, amount, category, due_date], outputs=[finance_table, summary_box, bar_chart, pie_chart])
    reset_btn.click(reset_data, inputs=None, outputs=[finance_table, summary_box, bar_chart, pie_chart])

demo.launch()
