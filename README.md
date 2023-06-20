# GPT-stories
Analysing cultural stereotypes in the stories GPT tells.

## Hypothesis
GPT-4 has an Anglo-American bias that is recreated in the kinds of stories it tells. 

## Data
The dataset is available in this repository as [`data/GPT_stories.csv`](https://github.com/MachineVisionUiB/GPT-stories/blob/main/data/GPT_stories.csv).

We have used the OpenAI API to generate around 4000 short plot summaries of stories from different nationalities or ethnic/cultural groups. Most are in English and focus on countries where English is extensively used. We included some other languages (official languages in Norway, French, Icelandic, Akan and Chinese) as counterpoints. 

Note that these are _not_ stories that are _actually_ representative of any nationalities, ethnicities and cultural groups. Rather the generated stories are the result of statistical patterns in GPT-3.5's training data that the model has identified and replicated. We would expect this to be stereotypical both because of limitations in the training data and because large language models like GPT-3.5 are designed to find patterns (which could also be called biases) and to generate content that replicates the patterns (biases) in the training data. (See also Jill's blog post [ChatGPT is multilingual but monocultural, and it’s learning your values](https://jilltxt.net/right-now-chatgpt-is-multilingual-but-monocultural-but-its-learning-your-values/))

This research is a kind of _audit_ of GPT-3.5 that aims to expand our understanding of AI bias. 

## Status 
As of June 20, 2023, we have the first version of the dataset, and will begin analysis. Also need to check the dataset, might need cleaning - e.g. line breaks should be encoded differently?

## Research questions and next steps for analysis (June 20, 2023)
- Are the stories generated from the default prompt (no nationality or ethnicity specified) different from stories with a specific nationality or ethnicity? Try sentiment analysis, word frequency (just word clouds?), word embeddings - what else? What might explain differences? Hypothesis: "White" and "American" stories are basically the same as the default stories.
- Are there differences between stories generated with English and non-English prompts? Problem: can we computationally compare stories in different languages or do we need humans to read them?
- Can we analyse the "lessons learned" without handcoding categories? E.g. is teamwork emphasised in American stories, while nature is emphasised in Australian stories and heritage and identity are always emphasised in "ethnic" stories?
- The stories in Sámi and Akan (and Icelandic?) are radically different from the others. Obviously this is due to less training data - but can we deduce anything more from the nature of these stories? Should have readers of those languages look at it of course, but could also do a machine translation into English?
  
## Description of the dataset
### Basic structure
`Write a 50 word plot summary for a potential [nationality or cultural group] children's novel.`

The dataset includes 100 generated stories using this prompt with NO nationality or cultural group ("`Write a 50 word plot summary for a potential children's novel`."), and  so we can compare to this as a default. 

Finally, compile all the sets of 100 stories into a combined file titled `GPTstories.csv` and upload it to the `/data` folder.

### Codebook (variables and explanations for `data/GPT_stories.csv`):
  - `prompt`: The prompt used, taking the format "Write a 50 word plot summary for a potential [nationality or cultural group] children's novel."
  - `reply`: The model's generated response to the prompt.
  - `date`: The date that the response was generated. As the models are regularly updated, this can be important information.
  - `model name`: We used GPT-3.5. The exact model name is stated.
  - `temperature`: The temperature setting. We used 1 throughout, which is the default setting, as we wanted to test the "default" mode of the LLM. Other researchers may wish to use other temperature settings. 
  - `language`: The language the prompt was written in, using the ISO 639-2 code. The more common 639-1 code was not used because it does not include Southern Sami and Lule Sami. (Note: ask a librarian whether the [EU standard is better](https://op.europa.eu/en/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/eurovoc) - identical codes?) The language codes used in the dataset are (if we find translators for the Sami languages):
      - eng = English
      - nob = Norwegian bokmål
      - non = Norwegian nynorsk
      - sma = Southern Sami (missing - need to find a translator)
      - sme = Northern Sami
      - smj = Lule Sami
      - fra = French
      - deu = German
      - aka = Akan
      - isl = Icelandic 
  - `country`: If the prompt refers to a nationality, the [ISO 3166](https://en.wikipedia.org/wiki/ISO_3166-2) code for the name of the country referred to is stated here. For England, Northern Ireland, Scotland, Wales, extended codes are used (GB-ENG, GB-NIR, GB-SCT, GB-CYM following [UK guidelines](https://www.gov.uk/government/publications/open-standards-for-government/country-codes)). If the prompt refers to a cultural group (e.g. African-American) this field will be NA.] See #5 for which countries to include.
      - India - 1,393,409,038
      - United States - 332,915,073
      - Pakistan - 225,199,937
      - Nigeria - 211,400,708
      - Philippines - 111,046,913
      - United Kingdom - 68,207,116
      - Tanzania - 61,498,437
      - South Africa - 60,041,994
      - Kenya - 54,985,698
      - Canada - 38,067,903
      - Australia - 25,788,215
      - Liberia - 5,180,203
      - Ireland - 4,982,907
      - New Zealand - 4,860,643
      - Jamaica - 2,973,463
      - Trinidad and Tobago - 1,403,375
      - Guyana - 790,326
      - Scotland
      - Wales
      - England
      - Northern-Ireland
  - `culture`: [e.g. American Indian - NA if a country rather than a culture]. Use the following cultures (see #6 for the rationale for this sampling strategy) 
      - Native American 
      - Asian-American
      - African-American
      - Native Hawaiian
      - White American
      - Hispanic
      - Roma
      - Afro-European
      - European Muslim
      - White European
      - Akan
      - Sámi
      - Indigenous Australian

### Different language versions:

|  prompt | language  | country  | culture |
|---|---|---|---|
| Skriv et sammendrag på 50 ord av en tenkt barnebok. | nob | NA | NA |
| Skriv et sammendrag på 50 ord av en tenkt norsk barnebok. | nob | NO | NA |
| Skriv eit samandrag på 50 ord av ei tenkt barnebok. | non | NA | NA |
| Skriv eit samandrag på 50 ord av ei tenkt norsk barnebok. | non | NO | NA |
| Écrivez une proposition de synopsis de 50 mots pour un livre pour enfants.| fra | NA | NA |
| Écrivez une proposition de synopsis de 50 mots pour un livre français pour enfants.| fra | FR | NA |
| Tjála tjoahkkájgæsos 50 báhko usjudit mánájromádna  | smj  | NA | NA |
| Tjála tjoahkkájgæsos 50 báhko usjudit sáme mánájromádna | smj  | NA | Sami |
| Skrifaðu 50 orða samantekt af ímyndaðri skáldsögu fyrir börn.  |  isl | NA  | NA |
| Skrifaðu 50 orða samantekt af ímyndaðri íslenskri skáldsögu fyrir börn. | isl  | IS | NA | 
|   |   |   |. |

