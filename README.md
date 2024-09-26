# Bike Rental Data Analysis Project by Fajri Fathur Rahman✨

## Project Overview
This project focuses on analyzing bike rental data to uncover patterns and insights that can help optimize bike-sharing services. We explore various factors affecting bike rentals, including weather conditions, seasonality, and user types. The analysis aims to provide valuable information for bike-sharing companies to improve their services and increase user satisfaction.
Key features of this project include:

- Data cleaning and preprocessing of bike rental datasets
- Exploratory data analysis to identify trends and correlations
- Visualization of rental patterns based on weather, season, and time
- Interactive dashboard for easy exploration of insights

The project utilizes Python for data analysis and Streamlit for creating an interactive web application to showcase the findings.


## Setup Environment - Anaconda

To set up the environment using Anaconda, follow these steps:

1. **Create and activate a new Conda environment:**
    ```sh
    conda create --name main-ds python=3.9
    conda activate main-ds
    ```

2. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Setup Environment - Shell/Terminal

If you prefer to use Shell or Terminal, follow these instructions:

1. **Create and navigate to the project directory:**
    ```sh
    mkdir proyek_analisis_data
    cd proyek_analisis_data
    ```

2. **Install Pipenv and create a virtual environment:**
    ```sh
    pipenv install
    pipenv shell
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Run Streamlit App

Once your environment is set up and dependencies are installed, you can run the Streamlit app with the following command:

```sh
cd dashboard
streamlit run dashboard.py
