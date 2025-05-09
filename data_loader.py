"""
data_loader.py
Handles database connection and data loading for the Jira Work Visualization App.
"""
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

def get_db_connection_string():
    """Get database connection string from env variable or .env file."""
    return os.getenv("DB_CONN_STR")

def load_jira_data():
    """
    Loads Jira issues data from SQL database into a Pandas DataFrame.
    Returns sample data if DB connection is not configured.
    """
    conn_str = get_db_connection_string()
    if conn_str:
        try:
            engine = create_engine(conn_str)
            query = """
                SELECT issue_type, issue_key, issue_summary, acceptance_criteria, story_points, pulled_date, created_date, resolution_date, status, resolution, Program, ProjectName
                FROM jira_issues
            """
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            print(f"DB connection failed: {e}. Using sample data.")
    # Sample data fallback
    data = [
        {"issue_type": "Story", "issue_key": "ST-101", "issue_summary": "Login page", "acceptance_criteria": "User can log in", "story_points": 3, "pulled_date": "2024-04-01", "created_date": "2024-03-28", "resolution_date": "2024-04-02", "status": "Done", "resolution": "Fixed", "Program": "Alpha", "ProjectName": "Website Redesign"},
        {"issue_type": "Feature", "issue_key": "FE-202", "issue_summary": "Dashboard", "acceptance_criteria": "Show metrics", "story_points": 8, "pulled_date": "2024-04-02", "created_date": "2024-03-27", "resolution_date": "2024-04-10", "status": "In Progress", "resolution": None, "Program": "Alpha", "ProjectName": "Website Redesign"},
        {"issue_type": "Story", "issue_key": "ST-102", "issue_summary": "Forgot password", "acceptance_criteria": "User resets password", "story_points": 5, "pulled_date": "2024-04-03", "created_date": "2024-03-29", "resolution_date": None, "status": "To Do", "resolution": None, "Program": "Beta", "ProjectName": "Mobile App"},
        {"issue_type": "Story", "issue_key": "ST-103", "issue_summary": "User profile", "acceptance_criteria": "User can view/edit profile", "story_points": 2, "pulled_date": "2024-04-04", "created_date": "2024-03-30", "resolution_date": "2024-04-05", "status": "Done", "resolution": "Fixed", "Program": "Beta", "ProjectName": "Mobile App"},
        {"issue_type": "Feature", "issue_key": "FE-203", "issue_summary": "Notifications", "acceptance_criteria": "System sends alerts", "story_points": 5, "pulled_date": "2024-04-05", "created_date": "2024-03-31", "resolution_date": None, "status": "Ready", "resolution": None, "Program": "Gamma", "ProjectName": "API Platform"},
        {"issue_type": "Story", "issue_key": "ST-104", "issue_summary": "Logout", "acceptance_criteria": "User can log out", "story_points": 1, "pulled_date": "2024-04-06", "created_date": "2024-04-01", "resolution_date": "2024-04-07", "status": "Done", "resolution": "Fixed", "Program": "Gamma", "ProjectName": "API Platform"},
        {"issue_type": "Feature", "issue_key": "FE-204", "issue_summary": "Reporting", "acceptance_criteria": "Export data to CSV", "story_points": 8, "pulled_date": "2024-04-07", "created_date": "2024-04-02", "resolution_date": None, "status": "In Progress", "resolution": None, "Program": "Alpha", "ProjectName": "Website Redesign"},
        {"issue_type": "Story", "issue_key": "ST-105", "issue_summary": "Password strength meter", "acceptance_criteria": "Show password strength", "story_points": 2, "pulled_date": "2024-04-08", "created_date": "2024-04-03", "resolution_date": "2024-04-09", "status": "Done", "resolution": "Fixed", "Program": "Beta", "ProjectName": "Mobile App"},
        {"issue_type": "Feature", "issue_key": "FE-205", "issue_summary": "API integration", "acceptance_criteria": "Connect to external API", "story_points": 13, "pulled_date": "2024-04-09", "created_date": "2024-04-04", "resolution_date": None, "status": "Ready", "resolution": None, "Program": "Gamma", "ProjectName": "API Platform"},
        {"issue_type": "Story", "issue_key": "ST-106", "issue_summary": "Accessibility improvements", "acceptance_criteria": "Meets WCAG 2.1", "story_points": 3, "pulled_date": "2024-04-10", "created_date": "2024-04-05", "resolution_date": None, "status": "To Do", "resolution": None, "Program": "Beta", "ProjectName": "Mobile App"},
        {"issue_type": "Feature", "issue_key": "FE-206", "issue_summary": "Dark mode", "acceptance_criteria": "Theme toggle", "story_points": 5, "pulled_date": "2024-04-11", "created_date": "2024-04-06", "resolution_date": None, "status": "Ready", "resolution": None, "Program": "Alpha", "ProjectName": "Website Redesign"},
        {"issue_type": "Story", "issue_key": "ST-107", "issue_summary": "Multi-factor auth", "acceptance_criteria": "User sets up MFA", "story_points": 8, "pulled_date": "2024-04-12", "created_date": "2024-04-07", "resolution_date": None, "status": "In Progress", "resolution": None, "Program": "Gamma", "ProjectName": "API Platform"}
    ]
    df = pd.DataFrame(data)
    # Convert date columns
    for col in ["pulled_date", "created_date", "resolution_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df
