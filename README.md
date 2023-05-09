# Welcome to PDF-Pilot!


PDF-Pilot is an AI-powered web application that allows users to upload PDFs, ask questions related to the content, and receive answers along with the relevant text highlighted in the PDF. 
The application uses natural language processing models and techniques to process the PDF content and generate answers to user queries.
This makes it a valuable tool for businesses and organizations that work with many handouts and often spend a lot of time going through them.

## Features

- Upload a PDF file
- Ask questions related to the PDF content
- Get answers to your questions
- View the relevant text highlighted in the PDF


<img src="images/Pilot.gif" alt="PDF-Pilot-GIF" width="300px">


## Getting Started

Follow these steps to run the HandoutAssistant web application on your local machine.

### Prerequisites

- Python 3.7+
- Node.js 12+
- Yarn or npm

### Installation

1. Clone the repository
```
git clone https://github.com/yourusername/HandoutAssistant.git
cd HandoutAssistant
```

2. Set up a virtual environment and install the Python dependencies
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Install the JavaScript dependencies
```
cd client
yarn install
```

4. Set up API keys

   a. Sign up for an [AI21 Studio](https://ai21.com/studio) account to obtain an API key.

   b. Sign up for an [OpenAI](https://beta.openai.com/signup/) account to obtain an API key.

   c. Create a `.env` file in the root directory of the project and add your API keys:

```
AI21_API_KEY=your_ai21_api_key
OPENAI_API_KEY=your_openai_api_key
```

### Running the Application

1. Start the Flask server in the root directory of the project:

```
flask run --port 5001
```

2. Start the React development server in the `client` directory:

```
cd client
yarn start
```

3. Open a browser and navigate to `http://localhost:3000`. You should see the HandoutAssistant web application.

4. Upload a PDF, enter a question, and click "Submit" to see the AI-generated answer and the relevant text highlighted in the PDF.

## How it Works

HandoutAssistant utilizes several natural language processing models and techniques to process the PDF content and generate answers to user queries. The main components of the application are:

- NLP: A wrapper around the Hugging Face Transformers library for question-answering tasks.
- PDFHandler: A utility class for reading text from PDF files and highlighting relevant text.
- AI21Segmentation: A utility class for segmenting large text files into smaller segments using the AI21 Studio API.
- OpenAIAPI: A utility class for generating answers to questions using the OpenAI API.
- HandoutAssistant: A class that coordinates the processing of PDFs, segmenting text, and generating answers to user queries.

The application first processes the PDF content and segments it into smaller sections. When a user submits a question, the HandoutAssistant class identifies relevant segments and generates a prompt for the OpenAI API. The API then provides an answer to the question, along with the ID of the most relevant segment. The application highlights the relevant text in the PDF and displays the answer to the user.

## Contributing

Feel free to contribute to this project by submitting a pull request or creating an issue. Please follow the existing coding style and include tests when necessary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.







Flowchart






<img src="images/Flowchart.png" alt="Flowchart" width="600px">


                                                            
