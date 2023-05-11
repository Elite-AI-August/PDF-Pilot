# PDF-Pilot


PDF-Pilot is an AI-powered web application that allows users to upload PDFs, ask questions related to the content, and receive answers along with the relevant text highlighted in the PDF. 


## Features

- Upload a PDF file
- Ask questions related to the PDF content
- Get answers to your questions
- View the relevant text highlighted in the PDF


<img src="images/Pilot.gif" alt="PDF-Pilot-GIF" width="600px">


## Getting Started

Follow these steps to run the web application on your local machine.

### Prerequisites

- Python 3.7+
- Node.js 12+
- Yarn or npm

### Installation

1. Clone the repository
```
git clone https://github.com/admineral/PDF-Pilot

```

2. Change the directory
```bash
cd PDF-Pilot
```

3. Set up a virtual environment and install the Python dependencies (pip or pip3)
```
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

4. Install the JavaScript dependencies
```
cd PDF-Pilot
npm install
```

5. Set up API keys

   a. Sign up for an [AI21 Studio](https://ai21.com/studio) account to obtain an API key.

   b. Sign up for an [OpenAI](https://beta.openai.com/signup/) account to obtain an API key.

   c. Create a `.env` file in the root directory of the project and add your API keys:

```
AI21_API_KEY=your_ai21_api_key
OPENAI_API_KEY=your_openai_api_key
```



### Running the Application

1. Start the Flask server in the `src` directory of the project (python or python3)

```
cd src
python3 server.py
```

2. Start the React development server in the root directory:

```
cd client
npm start
```

3. Open a browser and navigate to `http://localhost:3000`. You should see the PDF-Pilot web application.


4. Upload a PDF, enter a question, and click "Submit" to see the AI-generated answer and the relevant text highlighted in the PDF.




## How to Run Locally

1. Edit the `main()` function in the HandoutAssistand.py (PDF-Pilot/src/HandoutAssistant.py) script to provide the path to your input PDF file and the desired output PDF file. Also, input the question you want the Handout Assistant to answer.

```python
pdf_path = "/path/to/your/input.pdf"
output_pdf = "/path/to/your/output.pdf"
question = "Your question here"
```

2. Run the script
```bash
python handout_assistant.py
```

3. The answer, relevant text, and page number will be displayed in the console. The highlighted PDF will be saved to the specified output path.




## How it Works

- PDF text extraction and AI21 context segmentation
- Context-aware question answering with OpenAI's GPT-3
- FAISS-based efficient similarity search
- Automatic highlighting of relevant text in the PDF


## How It Works in detail

1. **PDF text extraction**: Handout Assistant uses the PyMuPDF library (fitz) to extract text from the PDF document. The text is then stored in a data structure with the corresponding page numbers.

2. **Text segmentation**: The extracted text is segmented into meaningful chunks using AI21 Studio's text segmentation API. These segments are assigned unique IDs and linked to their respective page numbers.

3. **Building the FAISS index**: Handout Assistant creates a FAISS index using the segmented text and OpenAI embeddings. This index is used to search for relevant text segments efficiently.

4. **Question answering**: When a user asks a question, Handout Assistant retrieves the most relevant text segments from the FAISS index. It then generates a prompt for OpenAI's GPT-4 engine, which uses the provided information to answer the question.

5. **Highlighting and page number identification**: Once the answer is generated, Handout Assistant identifies the page number and relevant text segment in the PDF. The PyMuPDF library is then used to highlight the identified text segment in the output PDF file.

With Handout Assistant, you can quickly find answers to your questions within large PDF documents, without having to read through the entire content. The tool automatically highlights the relevant information, making it easy for you to locate the answers within the PDF.






Flowchart






<img src="images/Flowchart.png" alt="Flowchart" width="600px">


                                                            
