import re
import os
import spacy
import pymupdf as fitz
import json

## This signals that the process has started
print("Resume parser initiated")

## This part opens the file. 
doc = fitz.open(r"Sample Resumes\ethancarlos.pdf")

## This part stores the gleaned text into a placeholder variable.
raw_text = ""
for page in doc:
    raw_text += page.get_text()

## This part loads the NLP processor thru spacy
nlp = spacy.load("en_core_web_sm")

## This part dictates some of the entity rules to override Spacy's NLP
ruler = nlp.add_pipe("entity_ruler", before="ner", config={"phrase_matcher_attr": "LOWER"})

ruler.from_disk(r"Sample Resumes\skills.jsonl")

## This part processes the raw_text into entities
final_doc = nlp(raw_text)

## This returns all the entities extracted by the system.
resume_data = {}
for ent in final_doc.ents:
    label = ent.label_
    value = ent.text.strip()

    ## This checks if the label is already in resume_data
    ## If not, it will create that label.
    if label not in resume_data:
        resume_data[label] = []
    
    ## This checks if the value is inside a certain category already.
    ## If noot, it will add that value into the category.
    if value not in resume_data[label]:
        resume_data[label].append(value)

## This part saves the data itno a json file

with open("results.json","w",encoding="utf-8") as results:
    json.dump(resume_data, results, indent=4, ensure_ascii=False)


print("ALL DONE!")

