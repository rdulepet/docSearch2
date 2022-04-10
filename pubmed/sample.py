from pymed import PubMed
import json
from copy import deepcopy
import pandas


pubmed = PubMed(tool="MyTool", email="riya_dulepet@brown.edu")
query = """(((medulloblastoma[Title/Abstract]) OR (medullomyoblastoma [Title/Abstract]) OR (sarcoma of cerebellar[Title/Abstract]) AND (("2015"[Date - Publication] : "3000"[Date - Publication]))) ) AND (clinical trial[pt] OR randomized controlled trial[pt])"""
results = pubmed.query(query)

abstracts = []
authors = {}
conclusions = []
journals = []
keywords = []
methods = []
pubDates = []
pubIds = []
results = []
titles = []
for article in results: 
    jsonObj = article.toJSON()
    print(jsonObj)
    abstracts.append(jsonObj["abstract"])
    #print(jsonObj["authors"])
    for author in jsonObj["authors"]:
        fullName = author["firstname"] + " " + author["lastname"] + " , " + author["initials"]
        #print(fullName)
        authors[fullName] = author["affiliation"]
    conclusions.append(jsonObj["conclusions"])
    journals.append(jsonObj["journals"])
    keywords.append(jsonObj["keywords"])
    methods.append(jsonObj["methods"])
    pubDates.append(jsonObj["publication_date"])
    pubIds.append(jsonObj["pubmed_id"])
    results.append(jsonObj["results"])
    titles.append(jsonObj["title"])

#print(authors)









"""
authorInstitute = {}
authorFrequency = {}
instituteFrequency = {}
errorList = []

for article in results:
    jsonObj = json.loads(article.toJSON())
   # print(jsonObj)
    
    for author in jsonObj["authors"]: 
        try: 
            fullAuthorName = author["firstname"] + " " + author["lastname"]
            institute = author["affiliation"]
            if fullAuthorName not in authorInstitute: 
                authorInstitute[fullAuthorName] = institute
            if fullAuthorName not in authorFrequency: 
                authorFrequency[fullAuthorName] = 1
                instituteFrequency[institute] = 1
            else: 
                authorFrequency[fullAuthorName] += 1
                instituteFrequency[institute] += 1
        except: 
             errorList.append(author)

        #print(fullAuthorName, author["affiliation"])
    

sortedAuthorFrequency = sorted(authorFrequency.items(), key=lambda x: x[1], reverse=True)
#print(sortedAuthorFrequency[:30])


    

sortedInstituteFrequency = sorted(instituteFrequency.items(), key=lambda x: x[1], reverse=True)
print(sortedInstituteFrequency[:5])

"""