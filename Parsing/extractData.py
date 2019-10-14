import nltk
import xml.etree.ElementTree as ET
from lxml.etree import strip_tags, strip_elements, parse
import os
from os import listdir
nltk.download('punkt')


def extract_ch_json(doc_path,out_path, doc_type, doc_id):
    """Return JSON from Grobid TEI
    This function tries to group sections of Grobid-generated TEI as chapters.
    """
    if doc_type == 'thesis':
        return extract_ch_json_thesis(doc_path, doc_type, doc_id)

    try:
        doc = parse(doc_path)
    except Exception as e:
        print('%s: %s' % (type(e).__name__, e))
        return 0

    # initial dict for information storage
    out_dict = {'id': doc_id, 'type': doc_type, 'title': '', 'chapters': []}

    # get document title
    titles = doc.xpath('/html/body/tei:tei/tei:teiheader/tei:filedesc/tei:titlestmt/tei:title',
                       namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})

    divs = doc.xpath('/html/body/tei:tei/tei:text/tei:back/tei:div/tei:listbibl/tei:biblstruct',
                     namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
    
   
    for bib in divs: 
  
        analytic = bib.findall('tei:analytic', namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
        for x in analytic:
            title = x.findall('tei:title',namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
            author = x.findall('tei:author/tei:persname',namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
            # for z in author:
            #     fname = z.findall('tei:author',namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
            for mnmn in author:
                forename = mnmn.findall('tei:forename',namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                surname = mnmn.findall('tei:surname',namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
                for klabel in forename:
                    file = open(out_path+"William_ref.txt","a+")
                    file.write(klabel.text+", "+"forename"+"\n")
                for klabel in surname: 
                    file = open(out_path+"William_ref.txt","a+")
                    file.write(klabel.text+", "+"surname"+"\n")
            for y in title:  
                
                # if os.path.exists(out_path+"William_ref.txt"):
                #     os.remove(out_path+"William_ref.txt")   
                file = open(out_path+"William_ref.txt","a+")
          
                file.write(y.text+", "+"title"+"\n")
                #print(y.text)
                file.close
    return out_dict


if __name__ == '__main__':
    """Extract sentences from Grobid TEI XML
    
    For each chapter, print the chapter title. Then print each sentence on a new line. 
    """

    docPath = '/Users/bipashabanerjee/Documents/CS/sem3/6604/grobid/dissertation/Williams_MR_D_2011.pdf.xml'
    outPath = '/Users/bipashabanerjee/Documents/CS/sem3/6604/grobid/dissertation/'
    ch_json = extract_ch_json(docPath,outPath, 'dissertation', 17292)
    if os.path.exists(outPath+"William_ref.txt"):
                    os.remove(outPath+"William_ref.txt")
  
        