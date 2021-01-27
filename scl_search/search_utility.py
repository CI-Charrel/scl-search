from configurations.config import ContentDB
from configurations.contentdb_trans import ContentDBManager
from configurations.app_utils import logger
from configurations.config import localappscl
import json
import clr
import os
import inspect

basefolder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
libpath = os.path.join(basefolder,"LuceneSearchLayer.NetCore1.1.dll")

clr.AddReference(libpath)


from LuceneSearchLayer import LuceneSearchWrapper
from SearchLayerBase import JsonIndexData
from SearchLayerBase import JsonSearchQueryRestrictions
from SearchLayerBase import JsonAutocompleteQueryRestictions
from System import *


class SEARCH:
    Supported_Extension = [".mp3", ".wma", ".aac", ".ogg", ".flac", ".wav", ".m4a", ".pdf", ".epub", ".mobi", ".azw3",
                           ".mkv", ".mp4", ".flv", ".avi", ".3gp", ".f4v", ".mpg", ".mpeg", ".mov", ".m4v", ".wmv",
                           ".webm"]
    StopWordList = ["The", "Main", "mp3", "docx", "csv", "txt", "a", "able", "about", "above", "abroad", "according",
                    "accordingly", "across", "actually", "adj", "after", "afterwards", "again", "against", "ago",
                    "ahead"]


    def __init__(self):
        self.my_instance = LuceneSearchWrapper()
        self.content = ContentDBManager()
        self.localfolder = localappscl
        self.localfolderIndex = os.path.join(self.localfolder, "Index")

        if not os.path.exists(self.localfolderIndex):
            logger.info("Index folder is not located in tmp location")

    def setup(self):
        retLT = False
        try:
            isCreate = False
            if not os.path.exists(self.localfolderIndex):
                os.mkdir(self.localfolderIndex)
                isCreate = True

            mainfolder_db = ContentDB
            index_data = JsonIndexData()
            index_data.ConnectionString = mainfolder_db
            index_data.Path = self.localfolder
            index_data.JsonExtensions = json.dumps(self.Supported_Extension)
            index_data.JsonStopWords = json.dumps(self.StopWordList)
            index_data.IndexPath = "Index"
            index_data.ContentDetailsId = 0
            index_data.Limit = 200

            if isCreate:
                self.my_instance.CreateIndex(index_data)
            else:
                self.my_instance.UpdateIndex(index_data, True)

            retLT = True

        except Exception as err:
            logger.info(err)

        return retLT


    def getindexdocument(self):
        retLT = False
        try:
            print("Get Index Documents: Index content details Id")
            results = self.my_instance.GetIndexDocuments(self.localfolderIndex)
            for result in results:
                print(result.ContentDetailId)

            retLT = True
        except Exception as err:
            pass

        return retLT

    def fulltextsearch(self, keyword , supressprint = False):
        result_dict = {}
        try:
            retLT = [self.localfolder]
            if retLT:
                ## search
                search_query = JsonSearchQueryRestrictions()
                search_query.SearchedText = keyword
                search_query.IndexPath = "Index"
                search_query.MaxResults = 20
                listFolders = retLT # [rec[1] for rec in retLT if os.path.exists(rec[1])]

                search_query.JsonSelectedIndexedFolders = json.dumps(listFolders)
                search_query.JsonExtensions = json.dumps(self.Supported_Extension)
                search_query.JsonStopWords = json.dumps(self.StopWordList)
                search_query.WeightMainTitle = 8
                results = self.my_instance.Search(search_query)

                if supressprint:
                    for result in results:
                        print("Result content details id and score for {} is {}".format(result.ContentDetailId, result.Score))

                cdLT = [[result.ContentDetailId] for result in results]
                result_dict = self.content.getsearch_results(cdLT)


        except Exception as err:
            logger.info(err)

        return result_dict

    def autocompletion(self, keyword, supressprint = False):
        retLT = []
        try:
            query_autocomplete = JsonAutocompleteQueryRestictions()
            query_autocomplete.SearchedText = keyword
            query_autocomplete.IndexFolder = self.localfolderIndex
            query_autocomplete.TopResults = 20
            query_autocomplete.JsonStopWords = json.dumps(self.StopWordList)
            results = self.my_instance.GetAutoCompleteResults(query_autocomplete)

            if supressprint:
                for result in results:
                    print("Autocomplete results are {}".format(result.AutocompleteSuggestion))

            retLT = [result.AutocompleteSuggestion for result in results]

        except Exception as err:
            logger.info(err)

        return retLT




if __name__ == "__main__":

    ss = SEARCH()

    issces = ss.setup()

    isdocument = ss.getindexdocument()

    rec = ss.fulltextsearch("bandicam")
    for xx in rec:
        print(rec[xx])

    aa = ss.autocompletion("bandicam")
