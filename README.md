# Project: Lionel Messi Goals Analysis

This project involves analyzing the goals scored by the footballer Lionel Messi throughout his career. Data is extracted from an online source, processed, and stored in a SQLite database. Additionally, a Power BI dashboard is provided to visualize the results.

## Project Structure

The project consists of several files and components:

- `get_goals.py`: Python script to extract data from the web and process it.
- `create_db.py`: Python script to create a SQLite database and update it with the processed information.
- `ImportGoalsADB.ipynb`: Databricks notebook to perform tasks similar to `get_goals.py`.
- `dashboard_LM_career_goals.pbix`: Power BI dashboard to visualize the results.
- `README.md`: This file, providing an overview of the project and its structure.

## Usage

1. Clone or download this repository to your local machine.
2. Run `get_goals.py` to fetch and process Messi's goal data.
3. Open `dashboard_LM_career_goals.pbix` in Power BI to visualize the results.

## Dependencies

The project requires the following dependencies:

- Python 3.x
- pandas
- sqlite3
- schedule (for task scheduling)
- Power BI Desktop (for viewing the dashboard)

## Additional Notes

- The `get_goals.py` script is scheduled to run daily at 9:00 AM to keep the database updated with the latest available data.
- The `ImportGoalsADB.ipynb` file can be run on Databricks to perform the same tasks as `get_goals.py` in a cloud-based big data analysis environment.

## Contribution

If you'd like to contribute to this project, feel free to send pull requests or open issues for suggestions and corrections.

## License

This project is licensed under the [MIT License](LICENSE).
