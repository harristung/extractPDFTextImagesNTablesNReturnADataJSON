# Extracting Text, Images & Tables in a PDF, Return to a JSON Format

I have try many existing PDF extraction method for my local llama RAG system, but none are to my requirement. As we need many valuable data is in the images and table in a PDF, I want to extract texts, images and tables within each page of the PDF for keeping the context of the PDF document. With this python script texts, images and tables are organized in a JSON format for further operations, such as text splitting, or create embeddings. 

## Description

An in-depth paragraph about your project and overview of use.

## Getting Started

Make sure you have Python3 installed in your system, then please create a virtual environment
```
python3 -m venv venv
```
Activate the virtual environment
```
source venv/bin/activate
```
### Installing
```
pip install -r requirements.txt
```
### Executing program

```
python3 main.py
```
Please change the props of the main functions as needed, it is at the bottom of the code in main.py
```
if __name__ == "__main__":
    # REPLACE THE FILE PATH WITH THE PATH TO THE PDF FILE YOU WANT TO EXTRACT DATA FROM AND THE DIRECTORY WHERE YOU WANT TO SAVE THE IMAGES, MAKE SURE THE DIRECTORY EXISTS AND HAVE THE CORRECT PERMISSIONS.
    main(_pdfFilePath = "sampleDocumentWithTable.pdf", _imageOutputDir = "images", _writeResultToAJSONFile=True, _writeResultToJSONFileName="jsonResultNow.json")
```

Copy the code on main.py to your project as needed

## Sample Output
The script will create a JSON file containing the extracted data. The structure of the JSON file will be as follows:
```
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
```
The Ouput JSON format will enable further operations, such as text splitting, or create embeddings later

## Authors

Contributors names and contact info
harristung@gmail.com

## Version History

* 0.1
    * Initial Release
##Help
props for extracting data from PDFs, change them as needed
# _pdfFilePath : str : Path to the PDF file.
# _imageOutputDir : str : Path to the directory where the images will be saved. MAKE SURE THE DIRECTORY EXISTS AND HAVE THE CORRECT PERMISSIONS.
# _fromPage : int : The page number from which the extraction will start.
# _endPage : int : The page number at which the extraction will end.
# _extractImage : bool : If True, images will be extracted.
# _extractText : bool : If True, text will be extracted.
# _extractTable : bool : If True, tables will be extracted.
# _imageSizeLowerLimitInKb : int : The minimum size of the image in KB to be saved.
# _extractTableStrategy : str : The strategy to use for extracting tables. Can be 'text' or 'lines'.
## License

This project is licensed under the MIT License - see the LICENSE.md file for details


# PDF Extraction Script

This script extracts images, text, and tables from a PDF file using `PyMuPDF` (also known as `fitz`) and `tqdm` for progress indication. The extracted data is saved in a JSON file.

tqdm is optional, please comment out all tqdm lines if you wish not to use it.

## Requirements

You can install the required packages using pip:

```sh

