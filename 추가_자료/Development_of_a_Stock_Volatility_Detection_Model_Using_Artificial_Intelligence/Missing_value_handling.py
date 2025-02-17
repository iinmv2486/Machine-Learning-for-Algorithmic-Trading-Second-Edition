import pandas as pd

def process_time_series_data(file_path):
    """
    Load a time series dataset, display information, and handle missing values
    using time-weighted interpolation.

    Parameters:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The cleaned and interpolated DataFrame.
    """
    # Load the dataset
    df = pd.read_csv(file_path)

    # Display basic information
    print("Dataset Information:")
    print(df.info())
    print("\nMissing Values per Column:")
    print(df.isnull().sum())

    # Convert Date column to datetime and set as index if present
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
    else:
        raise ValueError("The dataset does not contain a 'Date' column.")

    # Convert percentage columns if any
    for col in df.select_dtypes(include=['object']).columns:
        if '%' in df[col].astype(str).iloc[0]:  # Check if the first value contains '%'
            df[col] = df[col].str.replace('%', '').astype(float)

    # Drop completely empty columns
    df.dropna(axis=1, how='all', inplace=True)

    # Apply time-weighted interpolation for missing values
    df = df.interpolate(method='time')

    # Reset index for output
    df.reset_index(inplace=True)

    # Save the cleaned data to a CSV file
    output_file = "./추가_자료/Development_of_a_Stock_Volatility_Detection_Model_Using_Artificial_Intelligence/processed_data/CBOE Volatility Index Historical Data.csv"
    df.to_csv(output_file, index=False)
    print(f"\nProcessed data saved to: {output_file}")

    return df

# Example usage
file_path = "./추가_자료/Development_of_a_Stock_Volatility_Detection_Model_Using_Artificial_Intelligence/data/CBOE Volatility Index Historical Data.csv"  # Replace with your actual file path
cleaned_df = process_time_series_data(file_path)
