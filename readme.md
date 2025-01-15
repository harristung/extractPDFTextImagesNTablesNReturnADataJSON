I have try many PDF extraction method for my local ollama llama3.2 RAG system, but none are to my requirement. As we need many valuable data is in the images and table in a PDF, I want to extract texts, images and tables within each page of the PDF for keeping the context of the PDF. With this python script texts, images and tables are organized in a JSON format for further operations, such as create embeddings. 

# PDF Extraction Script

This script extracts images, text, and tables from a PDF file using `PyMuPDF` (also known as `fitz`) and `tqdm` for progress indication. The extracted data is saved in a JSON file.

tqdm is optional, please comment out all tqdm lines if you wish not to use it.

## Requirements

You can install the required packages using pip:

```sh
pip install -r requirements.txt


The script will create a JSON file containing the extracted data. The structure of the JSON file will be as follows:
[
    {
        "page_0": {
            "images": ["path/to/image1.png", "path/to/image2.png"],
            "text": "Extracted text from page 0",
            "table": {
                "column1": ["value1", "value2"],
                "column2": ["value3", "value4"]
            }
        }
    },
    {
        "page_1": {
            "images": ["path/to/image3.png"],
            "text": "Extracted text from page 1"
        }
    }
]