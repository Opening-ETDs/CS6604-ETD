import nltk
import xml.etree.ElementTree as ET
from lxml.etree import strip_tags, strip_elements, parse
import os
from os import listdir
nltk.download('punkt')

def extract_ch_json(doc_path,out_path, doc_type):
    """Return JSON from Grobid TEI
    This function tries to group sections of Grobid-generated TEI as chapters.
    """
    if doc_type == 'thesis':
        return extract_ch_json_thesis(doc_path, doc_type)

    

    docLabels = []
    dir_exists = os.path.isdir(doc_path)
    
    if dir_exists:
        docLabels = [f for f in listdir(doc_path) if not f.startswith('.') and not f.startswith('_') and  f.endswith('.xml')]
        for id, f1 in enumerate(docLabels):
            #print(f1)
         
            doc = parse(doc_path+f1)
       
            divs = doc.xpath("/tei:TEI/tei:text/tei:back/tei:div[@type='references']/tei:listBibl/tei:biblStruct",
                     namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
            filename = (f1.split('.')[0])
            #print(filename)
            i=0

            for bib in divs:  
                monogr = bib.findall('tei:monogr', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                analytic = bib.findall('tei:analytic', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                
                for data in monogr:
                    title = data.findall("tei:title[@type='main']",namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                    for y in title:  
                        i = i+1
                        file = open(out_path+filename+"_title.txt","a+")
                  
                        file.write(y.text+", "+"title"+"\n")
                        file.close()  
                for author in monogr:
                    author_data = author.findall('tei:author/tei:persName', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                    for a in author_data:

                        firstname=a.findall("tei:forename", namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                        surname=a.findall("tei:surname",namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                        for y2 in firstname:  
                      
                            file = open(out_path+filename+"_title.txt","a+")
                            file.write(y2.text+", "+"first-name"+"\n")
                            file.close() 
                        for y3 in surname:
                            file = open(out_path+filename+"_title.txt","a+")
                            file.write(y3.text+", "+"surname"+"\n")
                            file.close() 

                for moreData in analytic:
                    title_more = moreData.findall("tei:title[@type='main']",namespaces={'tei': 'http://www.tei-c.org/ns/1.0'}) 
                    for y1 in title_more:  
                        i = i+1
                        file = open(out_path+filename+"_title.txt","a+")
                      
                        file.write(y1.text+", "+"title"+"\n")       
                        file.close()
            
                



if __name__ == '__main__':
    print("file")
    """Extract sentences from Grobid TEI XML
    
    For each chapter, print the chapter title. Then print each sentence on a new line. 
    """

    doc_path = "/Users/bipashabanerjee/Documents/CS/sem3/6604/grobid/dataProcess/"
    out_path = "/Users/bipashabanerjee/Documents/CS/sem3/6604/grobid/dataProcess/new_diss/"
    ch_json = extract_ch_json(doc_path,out_path, 'dissertation')
