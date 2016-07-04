import search_engine_app
from  search_engine_app.services.ThreadPoolService import ThreadPoolService
from  search_engine_app.utils.Trace import Trace
from  search_engine_app.services.GoogleSearchService import GoogleSearch

class LoaderService :

    _RESPONSE_INDEX = 'response'
    _URL_INDEX = 'query'


    @staticmethod
    def setMockupMode(mockupFile):
        GoogleSearch.setMockupMode(mockupFile)


    def cache_by_arguments(aFunc):
        def cachedFunc(*args):
            if not hasattr(aFunc, '_cache'):
                aFunc._cache = {}
            if args in aFunc._cache:
                return aFunc._cache[args]
            newVal = aFunc(*args)
            aFunc._cache[args] = newVal
            return newVal

        return cachedFunc


    @staticmethod
    def _retrieveContent(query):
        try:
            response_raw = None
            Trace.thread_trace("\t\t\tSTART _retrieveContentFromURL")
            proxy = None
            Trace.thread_trace("\t\t\tREQUEST\t\t:\t\t\t{0}".format(query))
            google_search = GoogleSearch()
            response_raw = google_search.search(query)
            Trace.thread_trace("\t\t\tRESPONSE\t\n : SUCCESS:\t\t{0}".format(response_raw))
            response_object = {LoaderService._URL_INDEX:query, LoaderService._RESPONSE_INDEX:response_raw}
        except Exception as e:
            Trace.thread_trace("\t\t\tRESPONSE\t\n : ERROR:\t\t{0} Exception {1}".format(response_raw,str(e)))
            response_object  = {'url':query, 'response':False}
        Trace.thread_trace("\t\t\tEND _retrieveContentFromURL")
        return response_object

    @staticmethod
    def _preProcessQueries(list_of_queries):
        good_querie  = []
        wrong_queries =[]
        for query in list_of_queries:
            if len(query)<200:
                if not isinstance(query, str):
                    try:
                       query = query.decode('utf-8')
                    except Exception as e:
                        pass
                query = query.strip()
                if query:
                    good_querie.append(query)
            else:
                wrong_queries.append("This query is too long. (use < 200):'{0}'".format(wrong_queries))

        return good_querie,wrong_queries

    @staticmethod
    def _postProcessResponses(list_of_urls_reponses):
        wrong_responses = []
        good_reponse = []
        for response_object in list_of_urls_reponses:
            response = response_object[LoaderService._RESPONSE_INDEX]
            if response != False:
                good_reponse.append(response_object)
            else:
                responseURL = response_object[LoaderService._URL_INDEX]
                wrong_responses.append(responseURL)
        return good_reponse, wrong_responses


    @staticmethod
    def retrieveContentFromListOfQueries(list_of_queries):
        if not isinstance(list_of_queries, list) or len(list_of_queries) == 0:
            raise TypeError('arguments_array should be not empty list')
        (good_querie,wrong_queries) = LoaderService._preProcessQueries(list_of_queries)
        responses = ThreadPoolService.processTasksWithArguments(1, good_querie, LoaderService._retrieveContent)
        (good_reponse,wrong_responses) = LoaderService._postProcessResponses(responses)
        return good_reponse,wrong_responses,wrong_queries











