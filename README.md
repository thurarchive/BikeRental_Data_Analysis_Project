# Dicoding Data Analysis Project ✨

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
streamlit run dashboard.py
