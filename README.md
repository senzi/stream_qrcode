# AI Assistant Chat Response with QR Codes

This Python script is designed to interact with an AI chat model, receive responses, and generate QR codes for each chunk of the response. It also creates a progress bar GIF animation and saves the full conversation to a text file.

## Features

- Interacts with the AI model and receives responses in chunks.
- Generates QR codes for each chunk of the response.
- Creates a progress bar GIF animation of the QR codes.
- Saves the full conversation to a text file.

## Prerequisites

- Python 3.x
- `openai` Python package
- `pyqrcode` Python package
- `Pillow` Python package (PIL Fork)
- `python-dotenv` package for environment variable management

You can install the required packages using pip:

```bash
pip install openai pyqrcode pillow python-dotenv
```

## Configuration

Before running the script, you need to set up the environment variable for the API key. Create a `.env` file in the same directory as the script with the following content:

```plaintext
MOONSHOT_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual API key.

## Usage

1. Open your terminal or command prompt.
2. Navigate to the directory containing the script.
3. Run the script using Python:

```bash
python app.py
```


## Output

- QR codes for each chunk of the AI's response will be saved in a directory named with the current timestamp.
- A progress bar GIF animation will be created and saved in the same directory.
- The full conversation will be saved to a text file named `response.txt` in the same directory.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.
