# Retail Sales & Business Insights Dashboard

A beginner-friendly Business Analyst portfolio project built with Python, Streamlit, Pandas and Plotly.

## Files
- `app.py` — Streamlit dashboard application
- `sample_sales_data.csv` — illustrative sample retail dataset
- `requirements.txt` — Python packages needed by Streamlit Cloud

## Run on your computer
1. Install Python.
2. Open this folder in VS Code.
3. Open Terminal and run:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. The dashboard will open in your browser.

## Deploy free with Streamlit Community Cloud
1. Create a GitHub repository and upload all three files (`app.py`, `requirements.txt`, `sample_sales_data.csv`) to the repository root.
2. Sign in at https://share.streamlit.io/ using GitHub.
3. Select **Create app**, choose your repository and branch, and set the main file path to `app.py`.
4. Select **Deploy**. Streamlit will build the app and provide a public URL if deployment succeeds.

## Dataset columns
`Order ID`, `Order Date`, `City`, `Category`, `Product`, `Quantity`, `Sales`, `Profit`

You can upload another CSV from the dashboard sidebar, provided it has these columns.

## Important
The included dataset is fictional and for learning/demo purposes only. Do not present its numbers as actual company results. The business insights are simple observations from the selected data, not guaranteed business recommendations.
