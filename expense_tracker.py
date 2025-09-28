import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    """Toggle between light and dark theme"""
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# Dark theme CSS (unchanged)
dark_theme_css = """
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .metric-card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .income-card {
        border-left: 5px solid #00cc96;
    }
    .expense-card {
        border-left: 5px solid #ef553b;
    }
    .balance-card {
        border-left: 5px solid #ffa15a;
        background: linear-gradient(135deg, #262730 0%, #1c1c1c 100%);
    }
    .positive-balance {
        color: #00cc96;
        font-weight: bold;
        font-size: 2.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .negative-balance {
        color: #ef553b;
        font-weight: bold;
        font-size: 2.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .metric-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #fafafa;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #fafafa;
    }
    /* Text colors for dark theme */
    .stMarkdown, .stText, .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        color: #fafafa !important;
    }
    /* Delete button styling */
    .delete-btn {
        background-color: #ff4444;
        color: white;
        border: none;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        cursor: pointer;
        font-size: 0.8rem;
    }
    .delete-btn:hover {
        background-color: #cc0000;
    }
    /* Transaction row styling */
    .transaction-row {
        border-bottom: 1px solid #444;
        padding: 0.5rem 0;
    }
    /* Upload section styling */
    .upload-section {
        background-color: #1c1c1c;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #1f77b4;
        margin: 1rem 0;
        color: #fafafa !important;
    }
    .upload-section h4 {
        color: #1f77b4 !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .upload-section p {
        color: #fafafa !important;
        margin-bottom: 0;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    /* Sidebar styling */
    .css-1d391kg, .css-1y4p8pa {
        background-color: #262730;
    }
    /* Theme toggle button */
    .theme-toggle {
        background: linear-gradient(45deg, #1f77b4, #ff7f0e);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        margin: 1rem 0;
    }
    /* Fix for dataframes in dark mode */
    .dataframe {
        background-color: #262730 !important;
        color: #fafafa !important;
    }
    .dataframe th {
        background-color: #1f77b4 !important;
        color: white !important;
    }
    .dataframe td {
        background-color: #262730 !important;
        color: #fafafa !important;
        border-color: #444 !important;
    }
</style>
"""

# Apply the current theme
if st.session_state.theme == 'light':
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            color: #ad7334;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stApp {
            background-color: #f9eee2;
            color: #ad7334;
        }
        .metric-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 0.5rem 0;
            border-left: 5px solid #ad7334;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .income-card {
            border-left: 5px solid #00cc96;
        }
        .expense-card {
            border-left: 5px solid #ef553b;
        }
        .balance-card {
            border-left: 5px solid #ffa15a;
            background: linear-gradient(135deg, #fffaf0 0%, #f0f2f6 100%);
        }
        .positive-balance {
            color: #00cc96;
            font-weight: bold;
            font-size: 2.5rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .negative-balance {
            color: #ef553b;
            font-weight: bold;
            font-size: 2.5rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .metric-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #ad7334;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2c3e50;
        }
        /* Main page text colors */
        .main .stMarkdown, 
        .main .stText, 
        .main .stAlert, 
        .main .stInfo, 
        .main .stSuccess, 
        .main .stWarning, 
        .main .stError,
        .main .stSubheader,
        .main .stHeader {
            color: #ad7334 !important;
        }
        /* Delete button styling */
        .delete-btn {
            background-color: #ff4444;
            color: white;
            border: none;
            padding: 0.3rem 0.6rem;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.8rem;
        }
        .delete-btn:hover {
            background-color: #cc0000;
        }
        /* Transaction row styling */
        .transaction-row {
            border-bottom: 1px solid #e0e0e0;
            padding: 0.5rem 0;
        }
        /* Upload section styling */
        .upload-section {
            background-color: #f0f8ff;
            padding: 1.5rem;
            border-radius: 10px;
            border: 2px dashed #ad7334;
            margin: 1rem 0;
            color: #ad7334 !important;
        }
        .upload-section h4 {
            color: #ad7334 !important;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .upload-section p {
            color: #ad7334 !important;
            margin-bottom: 0;
            font-size: 0.95rem;
            line-height: 1.4;
        }
        /* Sidebar styling - Keep original colors */
        .css-1d391kg, .css-1y4p8pa {
            background-color: #ffffff;
            color: #2c3e50 !important;
        }
        .sidebar .stMarkdown,
        .sidebar .stText,
        .sidebar .stAlert,
        .sidebar .stInfo,
        .sidebar .stSuccess,
        .sidebar .stWarning,
        .sidebar .stError {
            color: #2c3e50 !important;
        }
        /* Theme toggle button */
        .theme-toggle {
            background: linear-gradient(45deg, #ad7334, #ff7f0e);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            margin: 1rem 0;
        }
        /* Fix for specific elements in main content */
        .main .stMetric {
            color: #2c3e50;
        }
        .main .stMetric label {
            color: #ad7334 !important;
        }
        .main .stDataFrame {
            color: #2c3e50;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(dark_theme_css, unsafe_allow_html=True)

# Initialize session state for transactions
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

def add_transaction(date, category, description, amount, transaction_type):
    """Add a new transaction to the session state"""
    transaction = {
        'id': len(st.session_state.transactions),  # Add unique ID for deletion
        'Date': date,
        'Category': category,
        'Description': description,
        'Amount': amount,
        'Type': transaction_type
    }
    st.session_state.transactions.append(transaction)

def add_transactions_from_dataframe(df):
    """Add multiple transactions from a DataFrame"""
    for _, row in df.iterrows():
        # Check if required columns exist
        if all(col in row for col in ['Date', 'Category', 'Description', 'Amount', 'Type']):
            add_transaction(
                row['Date'],
                row['Category'],
                row['Description'],
                row['Amount'],
                row['Type']
            )

def delete_transaction(transaction_id):
    """Delete a transaction by ID"""
    st.session_state.transactions = [
        t for t in st.session_state.transactions if t['id'] != transaction_id
    ]

def delete_all_transactions():
    """Delete all transactions"""
    st.session_state.transactions = []

def calculate_totals():
    """Calculate total income, expenses, and balance"""
    if not st.session_state.transactions:
        return 0, 0, 0
    
    df = pd.DataFrame(st.session_state.transactions)
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expenses = df[df['Type'] == 'Expense']['Amount'].sum()
    balance = total_income - total_expenses
    
    return total_income, total_expenses, balance

def export_to_excel():
    """Export transactions to Excel format"""
    if not st.session_state.transactions:
        return None
    
    df = pd.DataFrame(st.session_state.transactions)
    # Remove ID column for export
    df_export = df.drop('id', axis=1)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_export.to_excel(writer, sheet_name='Transactions', index=False)
        
        # Add summary sheet
        summary_data = {
            'Metric': ['Total Income', 'Total Expenses', 'Balance'],
            'Amount': [*calculate_totals()]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    output.seek(0)
    return output

def export_to_pdf():
    """Export transactions to PDF format"""
    if not st.session_state.transactions:
        return None
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("Expense Tracker Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Summary
    total_income, total_expenses, balance = calculate_totals()
    summary_text = f"Total Income: ${total_income:,.2f} | Total Expenses: ${total_expenses:,.2f} | Balance: ${balance:,.2f}"
    summary = Paragraph(summary_text, styles['Normal'])
    elements.append(summary)
    elements.append(Spacer(1, 20))
    
    # Transactions table (without ID)
    df = pd.DataFrame(st.session_state.transactions)
    df_display = df.drop('id', axis=1)
    table_data = [df_display.columns.tolist()] + df_display.values.tolist()
    
    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def process_uploaded_file(uploaded_file):
    """Process uploaded Excel file and return DataFrame"""
    try:
        if uploaded_file.name.endswith('.xlsx'):
            # Read the Excel file
            df = pd.read_excel(uploaded_file, sheet_name='Transactions')
            
            # Convert Date column to datetime if it's not already
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date']).dt.date
            
            # Validate required columns
            required_columns = ['Date', 'Category', 'Description', 'Amount', 'Type']
            if all(col in df.columns for col in required_columns):
                return df
            else:
                st.error("❌ Uploaded file is missing required columns.")
                return None
        else:
            st.error("❌ Please upload an Excel file (.xlsx)")
            return None
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        return None

def main():
    # Header with theme toggle
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown('<h1 class="main-header">💰 Personal Expense Tracker</h1>', unsafe_allow_html=True)
    
    with col3:
        theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
        theme_label = "Dark Mode" if st.session_state.theme == 'light' else "Light Mode"
        if st.button(f"{theme_icon} {theme_label}", key="theme_toggle", help="Switch theme"):
            toggle_theme()
            st.rerun()
    
    # Sidebar for adding transactions and file upload
    with st.sidebar:
        st.header("🎨 Theme")
        st.write(f"Current theme: **{st.session_state.theme.title()} Mode**")
        
        st.header("📁 Data Import/Export")
        
        # File upload section
        st.subheader("Upload Excel File")
        uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'], 
                                        help="Upload a previously exported Excel file to load your data")
        
        if uploaded_file is not None:
            df = process_uploaded_file(uploaded_file)
            if df is not None:
                st.success(f"✅ File loaded successfully! Found {len(df)} transactions.")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📥 Replace Current Data", use_container_width=True):
                        delete_all_transactions()
                        add_transactions_from_dataframe(df)
                        st.success("✅ Data replaced successfully!")
                        st.rerun()
                
                with col2:
                    if st.button("📥 Append to Current Data", use_container_width=True):
                        add_transactions_from_dataframe(df)
                        st.success("✅ Data appended successfully!")
                        st.rerun()
                
                # Show preview
                with st.expander("Preview Uploaded Data"):
                    st.dataframe(df.head())
        
        st.markdown("---")
        st.header("➕ Add New Transaction")
        
        with st.form("transaction_form", clear_on_submit=True):
            date = st.date_input("Date", datetime.today())
            category = st.selectbox("Category", [
                "Fund", "Food & Dining", "Transportation", "Shopping", 
                "Entertainment", "Bills & Utilities", "Healthcare",
                "Education", "Travel", "Salary", "Freelance", 
                "Investments", "Other"
            ])
            description = st.text_input("Description")
            amount = st.number_input("Amount (RM)", min_value=0.0, format="%.2f")
            transaction_type = st.radio("Type", ["Income", "Expense"])
            
            submitted = st.form_submit_button("Add Transaction")
            
            if submitted:
                if description and amount > 0:
                    add_transaction(date, category, description, amount, transaction_type)
                    st.success("✅ Transaction added successfully!")
                else:
                    st.error("❌ Please fill in all fields correctly.")
    
    # Main content area
    st.header("📊 Financial Summary")
    
    total_income, total_expenses, balance = calculate_totals()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Total Income",
            value=f"RM{total_income:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Total Expenses",
            value=f"RM{total_expenses:,.2f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Current Balance",
            value=f"RM{balance:,.2f}",
            delta=None
        )
        
        # Additional visual indicator
        if balance > 0:
            st.success("💰 Positive Balance")
        elif balance < 0:
            st.error("⚠️ Negative Balance")
        else:
            st.info("⚖️ Balance is Zero")
    
    # Transactions table with delete functionality
    st.header("📋 Transaction History")
    
    if st.session_state.transactions:
        # Display transactions with delete buttons
        st.subheader("Your Transactions")
        
        # Create a DataFrame for display
        df = pd.DataFrame(st.session_state.transactions)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date', ascending=False)
        
        # Display each transaction with a delete button
        for i, transaction in enumerate(st.session_state.transactions):
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 3, 2, 2, 1])
            
            with col1:
                st.write(f"**{transaction['Date']}**")
            with col2:
                st.write(transaction['Category'])
            with col3:
                st.write(transaction['Description'])
            with col4:
                amount_color = "#00cc96" if transaction['Type'] == 'Income' else "#ef553b"
                st.markdown(f"<span style='color: {amount_color}; font-weight: bold;'>${transaction['Amount']:,.2f}</span>", 
                           unsafe_allow_html=True)
            with col5:
                type_color = "#00cc96" if transaction['Type'] == 'Income' else "#ef553b"
                st.markdown(f"<span style='color: {type_color};'>{transaction['Type']}</span>", 
                           unsafe_allow_html=True)
            with col6:
                # Delete button for each transaction
                if st.button("🗑️", key=f"delete_{transaction['id']}", help="Delete this transaction"):
                    delete_transaction(transaction['id'])
                    st.success("✅ Transaction deleted successfully!")
                    st.rerun()
            
            st.markdown("---")
        
        # Alternative: Display as dataframe with bulk delete options
        st.subheader("Quick Delete Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Delete by date range
            st.write("**Delete by Date Range**")
            dates = [t['Date'] for t in st.session_state.transactions]
            min_date = min(dates) if dates else datetime.today().date()
            max_date = max(dates) if dates else datetime.today().date()
            
            start_date = st.date_input("Start Date", min_date, key="delete_start")
            end_date = st.date_input("End Date", max_date, key="delete_end")
            
            if st.button("Delete Transactions in Date Range"):
                transactions_to_delete = [
                    t for t in st.session_state.transactions 
                    if start_date <= t['Date'] <= end_date
                ]
                if transactions_to_delete:
                    for transaction in transactions_to_delete:
                        delete_transaction(transaction['id'])
                    st.success(f"✅ Deleted {len(transactions_to_delete)} transactions!")
                    st.rerun()
                else:
                    st.warning("No transactions found in the selected date range.")
        
        with col2:
            # Delete by type
            st.write("**Delete by Type**")
            delete_type = st.selectbox("Select type to delete", ["Income", "Expense"])
            
            if st.button(f"Delete All {delete_type} Transactions"):
                transactions_to_delete = [
                    t for t in st.session_state.transactions 
                    if t['Type'] == delete_type
                ]
                if transactions_to_delete:
                    for transaction in transactions_to_delete:
                        delete_transaction(transaction['id'])
                    st.success(f"✅ Deleted {len(transactions_to_delete)} {delete_type.lower()} transactions!")
                    st.rerun()
                else:
                    st.warning(f"No {delete_type.lower()} transactions found.")
        
        # Visualization section
        st.header("📈 Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Expenses by Category")
            if len(df[df['Type'] == 'Expense']) > 0:
                expense_df = df[df['Type'] == 'Expense']
                category_totals = expense_df.groupby('Category')['Amount'].sum()
                
                fig, ax = plt.subplots(figsize=(8, 6))
                colors = sns.color_palette('pastel')
                wedges, texts, autotexts = ax.pie(
                    category_totals.values, 
                    labels=category_totals.index, 
                    autopct='%1.1f%%',
                    colors=colors
                )
                
                for autotext in autotexts:
                    autotext.set_color('black')
                    autotext.set_fontsize(10)
                
                ax.set_title('Expense Distribution by Category', fontsize=14, fontweight='bold')
                st.pyplot(fig)
            else:
                st.info("No expense data available for pie chart.")
        
        with col2:
            st.subheader("Income vs Expenses Over Time")
            if len(df) > 0:
                # Sort by date and ensure proper datetime format
                df_sorted = df.sort_values('Date').copy()
                
                # Create separate columns for income and expenses
                df_sorted['Income'] = df_sorted.apply(lambda x: x['Amount'] if x['Type'] == 'Income' else 0, axis=1)
                df_sorted['Expense'] = df_sorted.apply(lambda x: x['Amount'] if x['Type'] == 'Expense' else 0, axis=1)
                
                # Group by date to get daily totals
                daily_totals = df_sorted.groupby('Date').agg({
                    'Income': 'sum',
                    'Expense': 'sum'
                }).reset_index()
                
                # Calculate cumulative values
                daily_totals['Cumulative_Income'] = daily_totals['Income'].cumsum()
                daily_totals['Cumulative_Expense'] = daily_totals['Expense'].cumsum()
                
                # Create the plot
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Plot cumulative income and expenses
                ax.plot(daily_totals['Date'], daily_totals['Cumulative_Income'], 
                        marker='o', linewidth=2, markersize=4, color='#00cc96', label='Cumulative Income')
                ax.plot(daily_totals['Date'], daily_totals['Cumulative_Expense'], 
                        marker='s', linewidth=2, markersize=4, color='#ef553b', label='Cumulative Expenses')
                
                # Customize the plot
                ax.set_xlabel('Date')
                ax.set_ylabel('Amount (RM)')
                ax.set_title('Income vs Expenses Over Time', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
                ax.legend()
                
                # Format x-axis dates
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                st.pyplot(fig)
                
                # Monthly breakdown
                st.subheader("Monthly Summary")
                df_sorted['Month'] = df_sorted['Date'].dt.to_period('M')
                monthly_summary = df_sorted.groupby(['Month', 'Type'])['Amount'].sum().unstack(fill_value=0)
                monthly_summary['Balance'] = monthly_summary.get('Income', 0) - monthly_summary.get('Expense', 0)
                
                st.dataframe(monthly_summary.style.format("RM{:,.2f}"))
                
            else:
                st.info("Not enough data for time series chart.")
        
        # Export section
        st.header("📤 Export Reports")
        
        st.markdown("""
        <div class="upload-section">
        <h4>💡 Save Your Data</h4>
        <p>Export your data to an Excel file to save it permanently. 
        You can upload this file later to continue where you left off!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Excel Export")
            if st.button("📊 Export to Excel", use_container_width=True):
                excel_file = export_to_excel()
                if excel_file:
                    st.download_button(
                        label="💾 Download Excel File",
                        data=excel_file,
                        file_name=f"expense_tracker_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
        
        with col2:
            st.subheader("PDF Export")
            if st.button("📄 Export to PDF", use_container_width=True):
                pdf_file = export_to_pdf()
                if pdf_file:
                    st.download_button(
                        label="💾 Download PDF Report",
                        data=pdf_file,
                        file_name=f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
    
    else:
        st.info("📝 No transactions yet. Start by adding transactions using the sidebar form or upload an existing Excel file!")
        
        # Quick start guide
        with st.expander("🚀 Quick Start Guide"):
            st.markdown("""
            ### How to get started:
            
            1. **Add transactions manually** using the form in the sidebar
            2. **Upload existing data** by dragging an Excel file to the upload area in the sidebar
            3. **Export your data** regularly to save your progress
            
            ### File Format for Upload:
            - Use Excel files (.xlsx) exported from this tracker
            - Required columns: Date, Category, Description, Amount, Type
            - Type should be either 'Income' or 'Expense'
            """)
    
    # Data Management in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Data Management")
    
    if st.session_state.transactions:
        st.sidebar.write(f"**Total Transactions:** {len(st.session_state.transactions)}")
        
        # Quick delete options in sidebar
        st.sidebar.subheader("Quick Actions")
        
        if st.sidebar.button("🗑️ Delete Last Transaction", use_container_width=True):
            if st.session_state.transactions:
                last_transaction = st.session_state.transactions[-1]
                delete_transaction(last_transaction['id'])
                st.sidebar.success("Last transaction deleted!")
                st.rerun()
        
        # Clear all data with confirmation
        if st.sidebar.button("⚠️ Clear All Data", use_container_width=True):
            st.warning("This will delete ALL transactions. This action cannot be undone!")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, Delete Everything", use_container_width=True):
                    delete_all_transactions()
                    st.success("All data cleared successfully!")
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.info("Deletion cancelled.")
    else:
        st.sidebar.info("No transactions to manage.")

if __name__ == "__main__":
    main()