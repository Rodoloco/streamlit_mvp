# Jira Work Visualization and Insights App (MVP)

A visually appealing, modular Streamlit dashboard for Jira analytics, its still work progress. 

## Features
- Interactive dashboards for Jira Features and Stories
- Modern, responsive charts and metrics
- SQL backend integration (configurable)
- Modular, maintainable codebase

## Setup
1. Clone or copy this folder to your computer.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your database connection string in a `.env` file or as an environment variable `DB_CONN_STR` (see below).
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Database Connection
- By default, the app looks for a `.env` file with `DB_CONN_STR="your-connection-string"`.
- If not set, the app uses sample data so you can explore the UI immediately.

## Customization
- Update `.streamlit/config.toml` to tweak theming.
- Edit `visuals.py` for chart styles.

## Requirements
- Python 3.9+
- Access to your SQL Server (if using live data)

## File Structure
- `app.py`: Main Streamlit app
- `data_loader.py`: Data access and loading
- `visuals.py`: Chart and metric rendering
- `.streamlit/config.toml`: Theme settings

---

