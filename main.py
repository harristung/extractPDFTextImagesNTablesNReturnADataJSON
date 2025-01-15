import fitz
from tqdm import tqdm # pip install tqdm
import os
from typing import List

# A Function extracting images, text and tables from a PDF file and return a JSON object containing the extracted data

def main(_pdfFilePath : str, _imageOutputDir : str, _fromPage : int = 0, _endPage : int = None, _imageSizeLowerLimitInKb : int = 100, _tableStrategy : str = 'text') -> List[dict]:
    print("Opening PDF File")
    doc = fitz.open(_pdfFilePath)
    tqdm('Length of the document', len(doc))

    #remove pages outside the fromPage and endPage
    
    endPage = len(doc) if not _endPage else _endPage
    documentJSON = []
    
    tqdm("Extracting Images")
    for i in tqdm(range(len(doc)), desc="pages"):
        if i < _fromPage or i > endPage:
            print('skipping page', i)
            continue
        
        pageImages = []

        for idx, img in enumerate(tqdm(doc.get_page_images(i), desc="page_images")):
            xref = img[0]
            image = doc.extract_image(xref)
            pix = fitz.Pixmap(doc, xref)
            imagePath = f"{_imageOutputDir}/page_{i}_image_{idx}.png"
            pix.save(imagePath)
            image_size_kb = os.path.getsize(imagePath) / 1024
            if int(image_size_kb) < _imageSizeLowerLimitInKb:
                os.remove(imagePath)
            else:
                pageImages.append(imagePath)
        
        documentJSON.append({f"page_{i}": {'images' : pageImages}})
        
    print('documentJSON : ', documentJSON)
    
    tqdm.write("Extracting Text Now...")
    
    for page in tqdm(doc, desc="pages_text"):
        pageText = []
        if page.number < _fromPage or page.number > endPage:
            continue
        text = page.get_text()
        text = text.replace("\n ", "\n")
        text = text.replace("\n  ", "\n")
        text = text.replace("\n\n", "\n")
        documentJSON[page.number][f"page_{page.number}"]['text'] = text
        
    tqdm.write("Extracting Tables Now...")
    
    for page in tqdm(doc, desc="pages_table"):
        if page.number < _fromPage or page.number > endPage:
            continue
        tabs = page.find_tables(strategy= _tableStrategy)
        if tabs.tables:
            
            documentJSON[page.number][f"page_{page.number}"]['table'] = tabs[0].to_pandas().to_dict()
    
    tqdm.write("Finshed Extracting")
    
    return documentJSON
    
if __name__ == "__main__":
    main("ojav20200300000_68230992.pdf", "images")