import nltk


class TextPaginator(object):
    def __init__(self, text: str,
                 message_threshold=140,
                 page_length_limit=320):
        self._pages = list()
        self._tokenizer = nltk.data.load('nltk:tokenizers/punkt/polish.pickle')
        self._sentences = self._tokenizer.tokenize(text)
        self._page_length_limit = page_length_limit
        self._message_threshold = message_threshold

        self._paginate()

    def get_page(self, page: int):
        return self._pages[page - 1]

    @property
    def pages_count(self):
        return len(self._pages)

    @property
    def sentences_count(self):
        return len(self._sentences)

    @property
    def page_length_limit(self):
        return self._page_length_limit

    @property
    def message_threshold(self):
        return self._message_threshold

    @property
    def sentences(self):
        return self._sentences

    def _paginate(self):
        page_content = ''
        for index, sentence in enumerate(self.sentences):
            if len(page_content + sentence) <= self.page_length_limit:
                if len(page_content):
                    sentence = ' ' + sentence
                page_content += sentence
            elif len(page_content) > self.message_threshold and len(sentence) <= self.page_length_limit:
                self._pages.append(page_content)
                page_content = sentence
            else:
                sentence_split_index = 0
                while True:
                    end_index_in_sentence = self.page_length_limit - len(page_content) + sentence_split_index
                    page_content += sentence[sentence_split_index: end_index_in_sentence]
                    sentence_split_index = end_index_in_sentence
                    if len(page_content) == self.page_length_limit:
                        self._pages.append(page_content)
                        page_content = ''
                    else:
                        break
            if index == self.sentences_count - 1 and page_content:
                self._pages.append(page_content)
