import fitz
from tqdm import tqdm #IMPORTANT PLEASE DO A "pip install tqdm" before running the code
import os
import json
from typing import List

# A Function extracting images, text and tables from a PDF file using pdfplumber and return a JSON object containing the extracted data

# _pdfFilePath : str : Path to the PDF file.
# _imageOutputDir : str : Path to the directory where the images will be saved. MAKE SURE THE DIRECTORY EXISTS AND HAVE THE CORRECT PERMISSIONS.
# _fromPage : int : The page number from which the extraction will start.
# _endPage : int : The page number at which the extraction will end.
# _extractImage : bool : If True, images will be extracted.
# _extractText : bool : If True, text will be extracted.
# _extractTable : bool : If True, tables will be extracted.
# _imageSizeLowerLimitInKb : int : The minimum size of the image in KB to be saved.
# _extractTableStrategy : str : The strategy to use for extracting tables. Can be 'text' or 'lines'.

# you can comment out all tqdm.write and tqdm statements to remove the progress bar and only return the extracted data.

def main(_pdfFilePath : str, _imageOutputDir : str, _fromPage : int = 1, _endPage : int = None, _extractImage : bool = True, _extractText : bool = True, _extractTable : bool = True, _imageSizeLowerLimitInKb : int = 100, _extractTableStrategy : str = 'lines', _writeResultToAJSONFile : bool = False, _writeResultToJSONFileName : str = "jsonResult.json") -> List[dict]:
    
    tqdm.write("Opening PDF File")
    doc = fitz.open(_pdfFilePath)

    #Because the doc is a zero based index, we need to subtract 1 from the endPage and fromPage to get the correct page number
    
    endPage = len(doc) - 1 if not _endPage else _endPage - 1
    fromPage = _fromPage - 1
    
    documentJSON = []
    
    if _extractImage:
        tqdm.write("Extracting Images Now...")
        for i in tqdm(range(len(doc)), desc="pages"):
            if i < fromPage or i > endPage:
                tqdm('skipping page', i)
                continue
            
            pageImages = []

            for idx, img in enumerate(tqdm(doc.get_page_images(i), desc="page_images")):
                xref = img[0]
                image = doc.extract_image(xref)
                pix = fitz.Pixmap(doc, xref)
                imagePath = f"{_imageOutputDir}/page_{i}_image_{idx}.png"
                pix.save(imagePath)
                image_size_kb = os.path.getsize(imagePath) / 1024
                # Filtering Out images with size less than _imageSizeLowerLimitInKb to filter out useless images
                if int(image_size_kb) < _imageSizeLowerLimitInKb:
                    os.remove(imagePath)
                else:
                    pageImages.append(imagePath)
            
            documentJSON.append({f"page_{i}": {'images' : pageImages}})
            
    if _extractText:
        tqdm.write("Extracting Text Now...")
        for page in tqdm(doc, desc="pages_text"):
            pageText = []
            if page.number < fromPage or page.number > endPage:
                continue
            text = page.get_text()
            # Remove extra spaces and new lines, you can customize this as you want
            text = text.replace("\n ", "\n")
            text = text.replace("\n  ", "\n")
            text = text.replace("\n\n", "\n")
            documentJSON[page.number][f"page_{page.number}"]['text'] = text
            
    if _extractTable:
        tqdm.write("Extracting Tables Now...")
        for page in tqdm(doc, desc="pages_table"):
            if page.number < fromPage or page.number > endPage:
                continue
            tabs = page.find_tables(strategy= _extractTableStrategy)
            if tabs.tables:
                documentJSON[page.number][f"page_{page.number}"]['table'] = tabs[0].to_pandas().to_dict()
    
    tqdm.write("Finished Extracting")
    
    if _writeResultToAJSONFile:
        with open(_writeResultToJSONFileName, 'w', encoding='utf-8') as f:
            json.dump(documentJSON, f, ensure_ascii=False, indent=4)
            
    return documentJSON
    
if __name__ == "__main__":
    # REPLACE THE FILE PATH WITH THE PATH TO THE PDF FILE YOU WANT TO EXTRACT DATA FROM AND THE DIRECTORY WHERE YOU WANT TO SAVE THE IMAGES, MAKE SURE THE DIRECTORY EXISTS AND HAVE THE CORRECT PERMISSIONS.
    main(_pdfFilePath = "sampleDocumentWithTable.pdf", _imageOutputDir = "images", _writeResultToAJSONFile=True, _writeResultToJSONFileName="jsonResultNow.json")
    
# Now you can copy the main function to your project and use it to extract data from PDF files.
# _extractTableStrategy can be 'text' or 'lines'. 'text' is faster but 'lines' is more accurate. Please see document of pdfplumber for more information. https://github.com/jsvine/pdfplumber?tab=readme-ov-file#extracting-tables