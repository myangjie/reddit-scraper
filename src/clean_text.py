import os, sys
from pathlib import Path
import json
import regex as re
from langdetect import detect, DetectorFactory
parentdir = Path(__file__).resolve().parents[1]
curdir = Path(__file__).resolve()
outdir = os.path.join(parentdir, "out")
datadir = os.path.join(parentdir, "data")
DetectorFactory.seed = 0

# clean the context of the comments or submission
def parse_text(content):
    
    #["~","`","@","#","$","%","^","&","*","(",")","_","-","+","=","{","}","[","]","|","\",":",";","<",",",">","/"]
    
    punc = ["~","`", "'","@","#","$","%","^","&","*","(",")","_","-","+","=","{","}","[","]","|",'"\"',":",
            ";","<",",",">","/", "/n", "/t", "&gt", "&amp", "&lt", "&le", "&gt"]
    
    
    # remove any possible web-link and images
    content = re.sub(r'http\S+', '', content)

    # remove some unicode annotations like \u201c
    string_encode = content.encode("ascii", "ignore")
    content = string_encode.decode()

    # reduce multiple stops to only one
    content = re.sub('\.\.+', '.', content)
    content = re.sub('\!+', '.', content)
    content = re.sub('\?+', '.', content)

    # replace some characters
    
    for p in punc:
        content = content.replace(p, "")

    #remove whitespaces

    final_content = " ".join(content.split())

    return final_content.lower()

def clean_data(file):

    cleaned_data = {"data": []}
    
    for text in file["data"]:
        
        if "bot" in text["author"]:
            continue
            
        try:

            try: 
                if (detect(text["selftext"]) != "en") or (detect(text["title"]) != "en"):
                    continue
            except:
                continue
            
            #submissions
            parsed_selftext = parse_text(text["selftext"])
            parsed_title = parse_text(text["title"])
        
            selftext_content = ' '.join(parsed_selftext.split())
            
            title_content = ' '.join(parsed_title.split())
            
            text["selftext"] = selftext_content
            text["title"] = title_content
            
            
        except KeyError:
            
            try:
                if (detect(text["body"]) != "en"):
                    continue
            except:
                continue
                
            #comments
            parsed_bodytext = parse_text(text["body"])
            body_content = ' '.join(parsed_bodytext.split())
            
            text["body"] = body_content
        
        cleaned_data["data"].append(text)
        
    return cleaned_data



