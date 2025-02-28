# Capital Gains Auto Calculator

This project is a web application for calculating capital gains from various brokers. It supports file uploads and processes the data to calculate short-term and long-term capital gains.

## Features

- Supports file uploads from Zerodha, Groww, and Samco.
- Calculates short-term and long-term capital gains.
- Displays results in a user-friendly format.
- Caches processed data to improve performance.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/capital-gains-calculator.git
    cd capital-gains-calculator
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    streamlit run src/main.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Upload your Excel files and view the calculated capital gains.

## Project Structure

- `src/main.py`: Main application file.
- `src/zerodha.py`: Contains functions to process Zerodha files.
- `src/groww.py`: Contains functions to process Groww files.
- `src/samco.py`: Contains functions to process Samco files.
- `src/utils.py`: Utility functions used across the project.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer

Calculations are for educational purposes only. Please consult a professional CA for tax filing.