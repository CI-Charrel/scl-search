
import json
import clr
clr.AddReference(r'D:\Project\Delivery_24.08.2019\SearchLibraryWithAutocomplete\LuceneSearchLayer.NetCore1.1.dll')


from LuceneSearchLayer import LuceneSearchWrapper
from SearchLayerBase import IndexData
from SearchLayerBase import JsonIndexData
from SearchLayerBase import SearchQueryRestrictions
from SearchLayerBase import JsonSearchQueryRestrictions
from SearchLayerBase import JsonAutocompleteQueryRestictions
from System import *

# Create the index
Supported_Extension = [".mp3", ".wma", ".aac", ".ogg", ".flac", ".wav", ".m4a",".pdf",".epub",".mobi",".azw3",".mkv", ".mp4", ".flv", ".avi", ".3gp", ".f4v", ".mpg", ".mpeg", ".mov", ".m4v", ".wmv", ".webm"]
StopWordList = ["The", "Main", "mp3", "docx", "csv", "txt", "a", "able", "about", "above", "abroad", "according", "accordingly", "across", "actually", "adj", "after", "afterwards", "again", "against", "ago", "ahead"]

mainfolder_db = "D:\Project\ContentDb.db"

my_instance = LuceneSearchWrapper()

index_data = JsonIndexData()
index_data.ConnectionString = mainfolder_db
index_data.Path = "D:"
index_data.JsonExtensions= json.dumps(Supported_Extension)
index_data.JsonStopWords = json.dumps(StopWordList)
index_data.IndexPath = "Index"
index_data.ContentDetailsId =0
index_data.Limit= 200
print("Update Index")
my_instance.UpdateIndex(index_data, True)

#print(CreateIndex)

#my_instance.CreateIndex(index_data)

#Get Index Documents
print("Get Index Documents: Index content details Id")
results = my_instance.GetIndexDocuments("D:\Index")
for result in results:
    print(result.ContentDetailId)


#search
search_query = JsonSearchQueryRestrictions()
search_query.SearchedText = "MainTitle"
search_query.IndexPath = "Index"
search_query.MaxResults = 20
listFolders = ["D:\HMY","D:"]

search_query.JsonSelectedIndexedFolders =json.dumps(listFolders) 
search_query.JsonExtensions= json.dumps(Supported_Extension)
search_query.JsonStopWords = json.dumps(StopWordList)
search_query.WeightMainTitle = 8

print("Results for searching text {}".format(search_query.SearchedText) )
results = my_instance.Search(search_query)
for result in results:
	print("Result content details id and score for {} is {}".format(result.ContentDetailId, result.Score))

		
search_query.SearchedText = "Main"
print("Results for searching text that is a stop word {}".format(search_query.SearchedText) )
results = my_instance.Search(search_query)
for result in results:
	
		print("Result content details id and score for {} is {}".format(result.ContentDetailId, result.Score))


 #autocomplete
query_autocomplete = JsonAutocompleteQueryRestictions()
query_autocomplete.SearchedText = "for"
query_autocomplete.IndexFolder = "D:\Index"
query_autocomplete.TopResults = 20
query_autocomplete.JsonStopWords = json.dumps(StopWordList)
print("Results for autocomplete text {}".format(query_autocomplete.SearchedText) )
results = my_instance.GetAutoCompleteResults(query_autocomplete)
for result in results:
	print("Autocomplete results are {}".format(result.AutocompleteSuggestion))

