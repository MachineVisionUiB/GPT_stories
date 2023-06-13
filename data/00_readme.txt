
This README file was generated on 2023-06-16 by Jill Walker Rettberg.
Last updated: 2023-06-16.

[draft]

-------------------
GENERAL INFORMATION
-------------------
// Title of Dataset: GPT-stories (working title)
// Contact Information
     // Name: Jill Walker Rettberg
     // Institution: University of Bergen
     // Email: jill.walker.rettberg@uib.no
     // ORCID: 0000-0003-2472-3812 

// CRediT author statement:
-
-

// Contributors:
Hermann Wigers

// Kind of data: 
Textual data, Tabular data.

// Date of data collection/generation: 
June 2023

// Funding sources: 
The project was partially funded by the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (ERC CoG, grant agreement No 771800), and partially funded by the Center for Digital Narrative (add info).

// Description of dataset: 
Short plot summaries of possible childrens' novels were generated using the Open AI API.


--------------------------
SHARING/ACCESS INFORMATION
--------------------------
// Licenses/Restrictions: This dataset is dedicated to the public domain (CC0). We request that any use of the dataset correctly cites it following good scientific practice.

// Links to publications that cite or use the data: See metadata field Related Publication.

// Recommended citation: 
[add]


--------------------------
METHODOLOGICAL INFORMATION
--------------------------


// Sampling criteria:

// Methods for processing the data: 

// Ethical considerations:



--------------------
DATA & FILE OVERVIEW
--------------------
// File List: 
- 00_README.txt (plain text file)
- 

// File formats:
- Tables are saved as comma separated csv files
- UTF-8 encoding
- 00_README.txt is a plain text file


// Relationship between files, if important: 


// Linking this dataset to other data 
ISO standards are used for the language of the prompt

// Is this a new version of a previously published dataset? No


-----------------------------------------
DATA-SPECIFIC INFORMATION FOR: 00_README.txt
-----------------------------------------
This file (= the current document) contains the documentation of the dataset.

-----------------------------------------
DATA-SPECIFIC INFORMATION FOR: XXXX.csv
-----------------------------------------
A table showing all variables used in the different data files with definitions and information about which variables are included in each file.

// Variable/Column List: 
- prompt: The prompt used, taking the format "Write a 50 word plot summary for a potential [nationality or cultural group] children's novel."

- reply: The model's generated response to the prompt.

- date: The date that the response was generated. As the models are regularly updated, this can be important information.

- model name: The name of the model used.

- temperature: The temperature setting. We used 1 throughout, which is the default setting, as we wanted to test the "default" mode of the LLM. Other researchers may wish to use other temperature settings. 

- language: The language the prompt was written in, using the ISO 639-2 code. The more common 639-1 code was not used because it does not include Southern Sami and Lule Sami. The language codes used in the dataset are:
-- eng = English
-- nob = Norwegian bokmål
-- non = Norwegian nynorsk
-- sma = Southern Sami
-- sme = Northern Sami
-- smj = Lule Sami
-- fra = French
-- deu = German
-- aka = Akan
-- ill = Icelandic

- country: If the prompt refers to a nationality, the ISO 3166 code for the name of the country referred to is stated here. For England, Northern Ireland, Scotland, Wales and Northern Ireland, extended codes are used (GB-ENG, GB-NIR, GB-SCT, GB-CYM (see https://www.gov.uk/government/publications/open-standards-for-government/country-codes). If the prompt refers to a cultural group (e.g. Norwegian-American) this field will be NA.

- culture: 
-- American Indian or Alaska Native, Asian, Black or African American, Native Hawaiian or Other Pacific Islander, and White

// 