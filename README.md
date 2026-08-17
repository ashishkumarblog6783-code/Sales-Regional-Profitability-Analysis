# Retail Sales & Regional Profitability Analysis

This project provides an interactive dashboard and data analysis for retail sales, profitability, regional performance, and customer behavior. It uses Python, Pandas, and Streamlit to process and visualize data.

## Features
- **Sales & Profitability Analysis:** View overall sales, total profit, profit margin, and total orders.
- **Category & Sub-Category Insights:** Understand which product categories and sub-categories are the most profitable.
- **Regional Performance:** Analyze state-wise sales and profit.
- **Time-Series Analysis:** Track monthly profit margin trends.
- **Customer Behavior:** Segment customers by order size and compare repeat vs. one-time customers.

## Files included
- `dashboard.py`: The main Streamlit application for the dashboard.
- `Untitled.ipynb`: Jupyter notebook for data exploration and preprocessing.
- `data/`: Contains the processed data file `merged.csv`.
- `List_of_Orders.xlsx`, `Order_Details.xlsx`, `Sales_target.xlsx`: Raw data files containing sales records and targets.

## Setup Instructions
1. Clone this repository.
2. Ensure you have Python installed.
3. Install the required libraries (e.g., `pip install pandas streamlit`).
4. Run the dashboard using the following command:
   ```bash
   streamlit run dashboard.py
   ```

## Requirements
- Python 3
- Pandas
- Streamlit
