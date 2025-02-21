# Main.py

## Data Processing and Visualization Script Documentation
This Python script processes, analyzes, and visualizes data from CSV and Excel files. It focuses on handling specific data related to fields and wells, managing date-time information, detecting duplicates, and visualizing time series data.

## Key Features
- **File Parsing**: Reads CSV and Excel files, extracting relevant data based on predefined patterns.
- **Date-Time Management**: Processes and formats date-time information, handling various formats.
- **Data Cleaning**: Identifies and handles duplicates, gaps, and inconsistencies in the data.
- **Visualization**: Generates visual timelines of data, highlighting key events and gaps.
- **Output Generation**: Saves processed data and findings into text files and Excel workbooks.

## Core Functions

### `get_field_well(file_name)`
- Extracts field and well names from a file name using regular expressions.
- Supports both CSV and Excel file formats.

### `read_file_contents(file_name)`
- Reads contents from a specified file, handling different data structures and inconsistencies.
- Returns a list of processed data rows.

### `sort_by_time(content_dictionary)`
- Sorts data in the provided dictionary by time for each key.

### `check_duplicates(content_dictionary)`
- Identifies and handles duplicate entries in the data.
- Returns updated data, a dictionary of duplicate dates, and a list of problematic files.

### `check_time_format(value)`
- Validates and formats date-time strings into `datetime` objects.

### `time_difference(content_dictionary)`
- Inserts markers in the data to highlight significant time gaps.

### `insert_failures(content_dictionary, file_name)`
- Integrates failure event data from a specified Excel file into the main data dictionary.

### `plot_timeline(content_dictionary)`
- Visualizes data timelines for each key in the dictionary, marking failures and time gaps.

### `main()`
- Orchestrates the execution of the script, including reading files from a specified path, processing data, and generating outputs.

## Usage
1. **Configure `ROOT_PATH`**: Set the `ROOT_PATH` in `settings.py` to the directory containing your CSV and Excel files.
2. **Run the Script**: Execute the script to process and visualize the data.
3. **Review Outputs**: Check the generated text files and Excel workbooks for insights and visualizations.

## Dependencies
- Python 3.x
- `pandas` for data manipulation
- `xlrd` for reading Excel files
- `openpyxl` for writing Excel files
- `matplotlib` for plotting
- `datetime` for handling date and time data

## Notes
- The script is specifically tailored for datasets with particular field and well information.
- Visualization results are saved as `.png` files, and processed data is saved in `.xlsx` and `.txt` formats.
- The script includes provisions for handling various data irregularities, such as missing values and inconsistent date formats.



# data_prep.py
## Excel File Data Processing and Analysis Script Documentation

## Overview
This script is designed to read, process, and analyze data from Excel files in a specified directory. It focuses on identifying healthy and failure data points, splitting data based on gaps, rounding off time intervals, and eventually creating feature-label pairs for machine learning or data analysis purposes.

## Key Features
- **Excel File Reading**: Processes all Excel files in a given directory, extracting data and organizing it by well names.
- **Failure and Healthy Data Splitting**: Segregates data into healthy and failure datasets based on specific criteria.
- **Gap Handling**: Identifies and handles data gaps in both healthy and failure datasets.
- **Time Interval Rounding**: Adjusts time intervals to a standard duration for consistency.
- **Feature-Label Pair Generation**: Creates pairs of features and labels for use in machine learning models.

## Core Functions

### `read_excel_files_in_directory(directory_path)`
- Reads all Excel files in a specified directory.
- Returns a dictionary with well names as keys and data as values.

### `split_healthy_failure(data_well)`
- Splits data into healthy and failure categories based on certain conditions.
- Identifies gaps and failures within the data and returns respective dictionaries.

### `split_to_gaps(failure_dict, healthy_dict, gap_index, failure_index)`
- Splits data further based on identified gaps, creating subsets of data for each gap interval.

### `round_intervals(healthy_dict_split)`
- Rounds time intervals to a standard duration for consistency across data points.

### `convert_freq(healthy_dict_split)`
- Converts the frequency of data points to create a uniform dataset, facilitating easier analysis.

### `make_window(feature_labels, list_of_lists, num_features, num_labels, num_stride)`
- Generates feature-label pairs from the dataset for use in predictive modeling.

### `label_failure(data_well)`
- Labels data points as failure based on specific conditions in the dataset.

### `main()`
- Orchestrates the execution of the script, including reading files, processing data, and generating outputs.

## Usage
1. **Set Directory Path**: Specify the directory path containing the Excel files in the `main` function.
2. **Run the Script**: Execute the script to process the data and perform analysis.
3. **Review Outputs**: Check the outputs, which include healthy and failure datasets, feature-label pairs, and gap analysis.

## Dependencies
- Python 3.x
- `openpyxl` for reading Excel files
- `joblib` for saving processed data
- `datetime` for handling date and time data

## Notes
- The script is tailored for datasets with specific structures, particularly related to time-series data in wells.
- Outputs are saved in joblib format for later use in machine learning applications.
- The script handles various data inconsistencies and prepares the dataset for further analysis or modeling.

This documentation provides an overview of the script's functionality and usage. For detailed understanding, refer to comments within the code.



# notebook.ipynb
## LSTM-Based Predictive Maintenance Documentation

## Overview
This document outlines a method for predictive maintenance using a Long Short-Term Memory (LSTM) network. The LSTM network is trained exclusively on data representing healthy conditions of a system or machinery. The trained model is then used to predict future values under healthy conditions. Anomalies are detected when the model's outputs significantly deviate from expected values, indicating potential failures.

## Methodology

### LSTM Network Training
- **Data Preparation**: Data representing the system's healthy state is collected and prepared for training. This data should capture the normal operating conditions of the system without any anomalies or failures.
- **Model Training**: The LSTM network is trained on this healthy data. The goal of the training process is for the LSTM to learn and understand the pattern of the system's normal behavior.
- **Model Architecture**: The LSTM model should be designed to capture temporal dependencies and patterns in the time series data indicative of the system's healthy state.

### Anomaly Detection
- **Predictive Monitoring**: In deployment, the LSTM model predicts future values based on incoming data streams.
- **Anomaly Identification**: When the system deviates from its normal operating conditions, the model's predictions will start to diverge significantly from the actual data values. These deviations are interpreted as anomalies.
- **Failure Prediction**: A substantial and consistent deviation from the model’s predictions is indicative of a potential failure. The onset of these deviations acts as an early warning sign, allowing for preemptive maintenance actions.

## Implementation Considerations

1. **Data Quality**: Ensure that the training data is of high quality and represents a comprehensive range of normal operating conditions.

2. **Model Parameters**: Tune the LSTM model parameters, including the number of layers, hidden units, and learning rate, to optimize prediction accuracy.

3. **Anomaly Thresholds**: Establish thresholds for deviation between predicted and actual values to accurately and reliably detect anomalies.

4. **Continuous Monitoring**: Implement a system for continuous monitoring and real-time analysis to quickly respond to detected anomalies.

5. **Model Re-training**: Regularly update and re-train the model with new data to maintain its accuracy and relevance, especially if the system undergoes changes over time.

## Use Case Application
This method is particularly useful in industrial settings where predictive maintenance can lead to significant cost savings, improved safety, and increased operational efficiency. It can be applied to various types of machinery and systems that generate time series data.

The LSTM-based predictive maintenance approach offers a proactive strategy for identifying potential system failures. By training the model on healthy data, the system can effectively recognize deviations that signal impending issues, allowing for timely interventions before actual failures occur.


## Credits
Inspired by Davide Pagano,
A predictive maintenance model using Long Short-Term Memory Neural Networks and Bayesian inference,
Decision Analytics Journal
https://doi.org/10.1016/j.dajour.2023.100174.
