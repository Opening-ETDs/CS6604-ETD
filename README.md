# Classification and extraction of information from ETD Documents

Identifying methods to accurately extract information (citation, tables, figures, etc.) from ETDs and to appropriately classify them into the ProQuest subject category classification system.

## Abstract

In recent years, advances in natural language processing, machine learning, and neural networks have led to powerful tools for digital libraries, allowing library collections to be discovered, used, and reused in exciting new ways. However, these new tools and techniques are not well-adapted to long documents such as electronic theses and dissertations (ETDs). The report describes three areas of study into improving access to ETDs. Our first goal is to use machine learning to automatically assign subject categories to these documents. Our second goal is to employ a neural network approach to parsing bibliographic data from reference strings. Our third goal is to use deep learning to identify and extract figures and their captions from ETDs.

**Approach**:

*   Our approach to parsing citations from ETDs is to research and utilize state-of-the-art nlp tools that 1) already aim to accomplish the same goal 2) give information that can be used as features to “define” the context of citations (dependency and semantic parsers/word embeddings).
*   Our approach for figure, table and caption extraction will involve researching and evaluating the performance of current state-of-the-art tools that achieve the same goal on our dataset of ETDs. Further, we will also try to improve the model by identifying the instances where the current state-of-the-art model fails.  
    
*   Our approach for classification will involve dropping the top most level of ProQuest subject categories while keeping the next two levels. We will train a neural network architecture using metadata of the ETDs, abstract information as well as attempting to see if adding full text data helps in the classification task.

**Related Projects:**

*   Big Data Text Summarization (Fall 2018): 
  *   [http://hdl.handle.net/10919/86420](http://hdl.handle.net/10919/86420) 
  *   [http://hdl.handle.net/10919/86418](http://hdl.handle.net/10919/86418) 
  *   [http://hdl.handle.net/10919/86406](http://hdl.handle.net/10919/86406)
*   Ashish Baghudana's text summarization project
*   [Neural-ParsCit](https://github.com/WING-NUS/Neural-ParsCit)

**Description**: A lot of techniques that exist for processing digital documents do not extend well to book length documents such as theses and dissertations. Thus, there is a need to develop techniques that are capable of extracting information from book length documents.

Our project will consist of three areas:

*   **Citation Parsing**: As part of the project, we will aim to accurately extract citations from ETDs using various NLP tools. Furthermore, we aim to identify particular pieces of information within the citations such as the author names. Ideally, we hope to use and adapted [Neural-ParsCit](https://github.com/WING-NUS/Neural-ParsCit) to accomplish these tasks.
*   **Figure and caption extraction:** As part of the project, we aim to accurately extract the figures, tables and the corresponding captions from our collections of ETD. Ideally we hope to use and adapt [DeepFigures](https://github.com/allenai/deepfigures-open/) to accomplish to this task.
*   **Categorization:** As part of the project, we aim to perform multi-class classification of ETD documents using the [ProQuest](https://media2.proquest.com/documents/subject-categories-academic.pdf) subject categories as the target classification system.

**Data**: Virginia Tech collection of ETDs, downloaded from [ETDs: Virginia Tech Electronic Theses and Dissertations](http://hdl.handle.net/10919/5534)

**Tools**:

*   [Grobid](https://github.com/kermitt2/grobid)
*   [ScienceParse](https://github.com/allenai/science-parse)
*   [DeepFigures](https://github.com/allenai/deepfigures-open)
*   [PDFFigures2](https://github.com/allenai/pdffigures2)


## Contents

This repository is made up of several Python scripts and Jupyter notebooks organized in separate
directories.

*   `parsing` --- code and data related to reference parsing  
*   `classification` -- code and data related for document classification  
*   `extraction` --- code and data related to figure extraction  


## Project Team
 
*   John Aromando ([@JAromando](https://github.com/JAromando))  
*   Bipasha Banerjee ([@Bipasha-banerjee](https://github.com/Bipasha-banerjee))  
*   Bill Ingram ([@waingram](https://github.com/waingram))  
*   Palakh Jude ([@palakhjude](https://github.com/palakhjude))  
*   Sampanna Kahu ([@sampannakahu](https://github.com/sampannakahu))  
