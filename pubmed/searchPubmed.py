from pymed import PubMed


# Create a PubMed object that GraphQL can use to query
# Note that the parameters are not required but kindly requested by PubMed Central
# https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
pubmed = PubMed(tool="MyTool", email="rdulepet@gmail.com")

# Create a GraphQL query in plain text
#query = "occupational health[Title]"
query = """(((medulloblastoma[Title/Abstract]) OR (medullomyoblastoma [Title/Abstract]) OR (sarcoma of cerebellar[Title/Abstract]) AND (("2015"[Date - Publication] : "3000"[Date - Publication]))) ) AND (clinical trial[pt] OR randomized controlled trial[pt])"""
print(query)


# Execute the query against the API
results = pubmed.query(query)

# Loop over the retrieved articles
for article in results:

    # Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle)
    print(type(article))

    # Print a JSON representation of the object
    print(article.toJSON())