import nltk
import xml.etree.ElementTree as ET
from lxml.etree import strip_tags, strip_elements, parse

nltk.download('punkt')


def extract_ch_json(doc_path, doc_type, doc_id):
    """Return JSON from Grobid TEI
    This function tries to group sections of Grobid-generated TEI as chapters.
    """
    if doc_type == 'dissertation':
        return extract_ch_json_dissertation(doc_path, doc_type, doc_id)

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

    divs = doc.xpath('/html/body/tei:tei/tei:text/tei:back/tei:div/tei:listbibl',
                     namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
    
    
    print(divs)
  

    return out_dict


if __name__ == '__main__':
    """Extract sentences from Grobid TEI XML
    
    For each chapter, print the chapter title. Then print each sentence on a new line. 
    """

    docPath = '/Users/bipashabanerjee/Documents/CS/sem3/6604/grobid/dissertation/Williams_MR_D_2011.pdf.xml'
    ch_json = extract_ch_json(docPath, 'thesis', 17292)

    for title in ch_json['title']:
        print()
        print(chapter['title'])
        
