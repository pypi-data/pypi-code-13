from py_stringmatching import utils
from six.moves import xrange
from py_stringmatching.tokenizer.definition_tokenizer import DefinitionTokenizer


class QgramTokenizer(DefinitionTokenizer):
    """Returns tokens that are sequences of q consecutive characters.
    
    A qgram of an input string s is a substring t (of s) which is a sequence of q consecutive characters. Qgrams are also known as
    ngrams or kgrams. 

    Args:
        qval (int): A value for q, that is, the qgram's length (defaults to 2).
        return_set (boolean): A flag to indicate whether to return a set of
                              tokens or a bag of tokens (defaults to False).
                              
    Attributes:
        qval (int): An attribute to store the q value.
        return_set (boolean): An attribute to store the flag return_set.
    """
    
    def __init__(self, qval=2, return_set=False):
        if qval < 1:
            raise AssertionError("qval cannot be less than 1") 
        self.qval = qval
        super(QgramTokenizer, self).__init__(return_set)

    def tokenize(self, input_string):
        """Tokenizes input string into qgrams.

        Args:
            input_string (str): The string to be tokenized. 

        Returns:
            A Python list, which is a set or a bag of qgrams, depending on whether return_set flag is True or False. 

        Raises:
            TypeError : If the input is not a string

        Examples:
            >>> qg2_tok = QgramTokenizer()
            >>> qg2_tok.tokenize('database')
            ['da','at','ta','ab','ba','as','se']
            >>> qg2_tok.tokenize('a')
            []
            >>> qg3_tok = QgramTokenizer(3) 
            >>> qg3_tok.tokenize('database')
            ['dat', 'ata', 'tab', 'aba', 'bas', 'ase']
                      
            As these examples show, the current qgram tokenizer does not consider the case of appending #s at the 
            start and the end of the input string. This is left for future work. 
        """
        utils.tok_check_for_none(input_string)
        utils.tok_check_for_string_input(input_string)

        qgram_list = []

        if len(input_string) < self.qval:
            return qgram_list

        qgram_list = [input_string[i:i + self.qval] for i in 
                          xrange(len(input_string) - (self.qval - 1))]
        qgram_list = list(filter(None, qgram_list))

        if self.return_set:
            return utils.convert_bag_to_set(qgram_list)            

        return qgram_list

    def get_qval(self):
        """Gets the value of the qval attribute, which is the length of qgrams. 

        Returns:
            The value of the qval attribute. 
        """
        return self.qval

    def set_qval(self, qval):
        """Sets the value of the qval attribute. 

        Args:
            qval (int): A value for q (the length of qgrams). 

        Raises:
            AssertionError : If qval is less than 1.
        """
        if qval < 1:
            raise AssertionError("qval cannot be less than 1")
        self.qval = qval
        return True
