import argparse
import os, sys
from pathlib import Path
from pmaw import PushshiftAPI
api = PushshiftAPI()
import datetime as dt
import json
import pandas as pd
from clean_text import *
parentdir = Path(__file__).resolve().parents[1]
outdir = os.path.join(parentdir, "out")
cachedir = os.path.join(parentdir, "cache")

def scrape_submissions(keyword, size, aft, bef, sub="all"):
    
    if sub == "all":
        
        posts = api.search_submissions(q=keyword, after = int(aft), before = int(bef), limit=size, 
                                       mem_safe=True, safe_exit=True, cache_dir = cachedir)
    else:
        posts = api.search_submissions(q=keyword, subreddit = sub, after = int(aft), before = int(bef), limit=size, 
                                       mem_safe=True, safe_exit=True, cache_dir = cachedir)
    # get all responses
    post_list = [post for post in posts]
    
    final = []
    for submission in post_list:
        try:
            cleaned_data = {
                        "subreddit_name": submission["subreddit"],
                        "author": submission["author"],
                        "author_fullname": submission["author_fullname"],
                        "id": submission["id"],
                        "score": submission["score"],
                        "selftext": submission["selftext"],
                        "subreddit_id": submission["subreddit_id"],
                        "subreddit_subscribers": submission["subreddit_subscribers"],
                        "created_utc": submission["created_utc"],
                        "num_comments": submission["num_comments"],
                        "title": submission["title"]
                    }
            if "upvote_ratio" in submission:
                    cleaned_data["upvote_ratio"] = submission["upvote_ratio"]
        
        except KeyError:
            pass
        
        try:
            final.append(cleaned_data)
        
        except Exception:
            print("There is something wrong with your search query.")

    after_date = dt.datetime.fromtimestamp(aft).strftime('%Y%m%d')
    before_date = dt.datetime.fromtimestamp(bef).strftime('%Y%m%d')

    if sub=="all":
        filename = keyword + "_" + str(after_date) + "_" + \
               str(before_date) + "_submissions" + ".json"
    else:
        filename = keyword + "_" + str(after_date) + "_" + \
               str(before_date) + "_submissions" + "_"+ sub + ".json"
    
    final_out = {"data":final}

    clean_out = clean_data(final_out)
    
    #raw
    outpath_r = os.path.join(outdir, "raw", "submissions", keyword)

    isExist = os.path.exists(outpath_r)

    if not isExist:
      
      os.makedirs(outpath_r) 

    with open(os.path.join(outpath_r, filename), 'w') as f:
        json.dump(final_out, f)

    #clean
    outpath_c =  os.path.join(outdir,  "clean", "submissions", keyword)

    isExistc = os.path.exists(outpath_c)

    if not isExistc:
      
      os.makedirs(outpath_c) 

    with open(os.path.join(outpath_c, filename), 'w') as fc:
        json.dump(clean_out, fc)

def scrape_comments(keyword, size, aft, bef, sub="all"):
    
    if sub == "all":
        comments = api.search_comments(q=keyword, after = int(aft), before = int(bef), limit=size, 
                                       mem_safe=True, safe_exit=True, cache_dir = cachedir)
    else:
        comments = api.search_comments(q=keyword, subreddit = sub, after = int(aft), before = int(bef), limit=size, 
                                       mem_safe=True, safe_exit=True, cache_dir = cachedir)
    # get all responses
    comment_list = [c for c in comments]
    
    final = []
    for comment in comment_list:
        try:
            cleaned_data = {
                    "subreddit_name": comment["subreddit"],
                    "author": comment["author"],
                    "id": comment["id"],
                    "author_fullname": comment["author_fullname"],
                    "score": comment["score"],
                    "body": comment["body"],
                    "subreddit_id": comment["subreddit_id"],
                    "created_utc": comment["created_utc"]
                }
            # save them into our json object
            if "upvote_ratio" in comment:
                cleaned_data["upvote_ratio"] = comment["upvote_ratio"]
    
        except KeyError:
            pass
        
        try:
            final.append(cleaned_data)
        
        except Exception:
            print("There is something wrong with your search query.")
    
    after_date = dt.datetime.fromtimestamp(aft).strftime('%Y%m%d')
    before_date = dt.datetime.fromtimestamp(bef).strftime('%Y%m%d')

    if sub=="all":
        filename = keyword + "_" + str(after_date) + "_" + \
               str(before_date) + "_submissions" + ".json"
    else:
        filename = keyword + "_" + str(after_date) + "_" + \
               str(before_date) + "_submissions" + "_"+ sub + ".json"
    
    final_out = {"data":final}

    clean_out = clean_data(final_out)

    #raw
    outpath_r =  os.path.join(outdir,  "raw", "comments", keyword)

    isExist = os.path.exists(outpath_r)

    if not isExist:
      
      os.makedirs(outpath_r) 

    with open(os.path.join(outpath_r, filename), 'w') as f:
        json.dump(final_out, f)

    #clean
    outpath_c =  os.path.join(outdir,  "clean", "comments", keyword)

    isExistc = os.path.exists(outpath_c)

    if not isExist:
      
      os.makedirs(outpath_c) 

    with open(os.path.join(outpath_c, filename), 'w') as fc:
        json.dump(clean_out, fc)
        

def main():
    #python3 reddit_scraper.py -a <after> -b <before> -l <limit> -s <subreddit> 
    parser = argparse.ArgumentParser(description= "Scrape Reddit given a CSV of keywords")

    #arguments
    #parser.add_argument("-k", "--keyw", required=True, help ='The csv file of keywords')
    parser.add_argument("-a", "--after", required=True, help = 'Get all queries after this date. Format: YYYYMMDD')
    parser.add_argument("-b", "--before", required=True, help = 'Get all queries before this date. Format: YYYYMMDD')
    parser.add_argument("-l", "--limit", required=True, help = 'Amount of queries to return.')
    parser.add_argument("-s", "--sub", help = "Subredit to search, optional. Default: all")
    
    args = parser.parse_args()
    #keyws = args.keyw
    after = args.after 
    before = args.before
    limit = int(args.limit)
    subr = args.sub 

    #get keywords
    keyws = os.path.join(parentdir, "data", "keywords.csv")
    
    df = pd.read_csv(keyws, header=None)
    keywords = list(df.iloc[:,1])

    #get date
    yyyy_a = int(after[0:4])
    mm_a = int(after[4:6])
    dd_a = int(after[6:9])

    yyyy_b = int(before[0:4])
    mm_b = int(before[4:6])
    dd_b = int(before[6:9])

    start_date = dt.datetime(yyyy_a, mm_a, dd_a).timestamp()
    end_date = dt.datetime(yyyy_b, mm_b, dd_b).timestamp()

    if end_date<start_date:
        sys.exit("Your end date is before your start date.")

    #cache
    isExistc = os.path.exists(cachedir)

    if not isExistc:
      
      os.makedirs(cachedir)

    #loop through keywords

    for word in keywords:
        if subr is not None:
            scrape_submissions(word, limit, start_date, end_date, subr)
            scrape_comments(word, limit, start_date, end_date, subr)
        else:
            scrape_submissions(word, limit, start_date, end_date)
            scrape_comments(word, limit, start_date, end_date)
        
if __name__ == "__main__":

    main()
