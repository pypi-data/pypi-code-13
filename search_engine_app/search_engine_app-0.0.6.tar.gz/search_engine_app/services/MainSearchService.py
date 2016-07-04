import search_engine_app
from  search_engine_app.services.LoaderService import LoaderService

class MainSearchService:


    @staticmethod
    def setMockupMode(mockupFile):
        LoaderService.setMockupMode(mockupFile)


    @staticmethod
    def searchOnGoogleFromFile(file_reference):
        try:
            good_reponse = None
            wrong_responses = None
            wrong_queries = None
            if file_reference:
                linesOfFile = file_reference.readlines()
            if isinstance(linesOfFile, list) and len(linesOfFile) > 0:
                (good_reponse,wrong_responses,wrong_queries) = LoaderService.retrieveContentFromListOfQueries(linesOfFile)
        except Exception as e:
            pass

        return good_reponse,wrong_responses,wrong_queries
