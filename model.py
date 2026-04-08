import os
import nltk
import threading
import natsort
import linked_list

class Boolean_model:
    def __get_stop_words(self):
        """read the stop words from the text file"""
        file = open(file=".\\Stopword-List.txt")
        self.__stop_words = file.read().split() #creating a list of words from the string of text
        file.close()
    
    def __parse_document(self, file_path, documents, doc_index):
        """function to parse a single document."""
        file = open(file=file_path)
        content = file.read()
        file.close()
        porter = nltk.PorterStemmer()
        content = content.lower()
        content = nltk.word_tokenize(content)
        cleaned_words = []
        for word in content:
            #remove special characters except hyphens and slashes
            word = "".join(char for char in word if char.isalpha() or char in {"-", "/"})
            #remove words that contain numbers
            if any(char.isdigit() for char in word):
                continue
            #ensure word is not empty
            if word:
                #split words on hyphen and slash
                split_words = word.replace("-", " ").replace("/", " ").split()
                for split_word in split_words:
                    stemmed_word = porter.stem(split_word)
                    if stemmed_word and stemmed_word not in self.__stop_words:
                        cleaned_words.append(stemmed_word)
        documents[doc_index] = cleaned_words
        
    def __create_positional_index(self, documents):
        """create inverted index"""
        #creating and sorting posting list
        posting = []
        posting = [(word, doc_id + 1, pos_id + 1) for doc_id, words in enumerate(documents) for pos_id, word in enumerate(words)]
        posting.sort(key=lambda tuple: tuple[0])
        
        #creating inverted index from sorted posting
        for word, doc, pos in posting:
            if(word not in self.__positional_index):
                l = linked_list.Linked_list()
                self.__positional_index[word] = l
                self.__positional_index[word].insert(doc)
                self.__positional_index[word].get_head().add_position(pos)
            else:
                current = self.__positional_index[word].get_head()
                while(current != None):
                    if(current.data == doc):
                        current.add_position(pos)
                        break
                    current = current.next
                if(current == None):
                    self.__positional_index[word].insert(doc)
                    self.__positional_index[word].get_tail().add_position(pos)
        
    def __read_documents(self):
        """reads all the documents and then creates inverted-index and positional-index"""
        files = [".\\Abstracts\\"+str(document) for document in os.listdir(path=".\\Abstracts\\") if document.endswith(".txt")]
        files = natsort.natsorted(files)
        documents = [None] * len(files)
        threads = []
        for i in range(len(files)):
            thread = threading.Thread(target=self.__parse_document, args=(files[i], documents, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
            
        self.__positional_index = {}
        self.__create_positional_index(documents)
        
    def __init__(self):
        """initializer for the boolean model"""
        self.__get_stop_words()
        self.__read_documents()
    
    def __and_operation(self, word1_p, word2_p, nesting=False):
        """applies and operation on 2 posting lists"""
        if(nesting):
            result = linked_list.Linked_list()
        else:
            result = []
        while(word1_p != None and word2_p != None):
            if(word1_p.data == word2_p.data):
                if(nesting):
                    result.insert(word1_p.data)
                else:
                    result.append(word1_p.data)
                word1_p = word1_p.next
                word2_p = word2_p.next
            elif(word1_p.data < word2_p.data):
                word1_p = word1_p.next
            else:
                word2_p = word2_p.next
        return result
    
    def __andnot_operation(self, word1_p, word2_p, nesting=False):
        """applies andnot operation on 2 posting lists"""
        if(nesting):
            result = linked_list.Linked_list()
        else:
            result = []
        while(word1_p != None and word2_p != None):
            if(word1_p.data == word2_p.data):
                word1_p = word1_p.next
                word2_p = word2_p.next
            elif(word1_p.data < word2_p.data):
                if(nesting):
                    result.insert(word1_p.data)
                else:
                    result.append(word1_p.data)
                word1_p = word1_p.next
            else:
                word2_p = word2_p.next
        return result
    
    def __or_operation(self, word1_p, word2_p, nesting=False):
        """applies or operation on 2 posting lists"""
        if(nesting):
            result = linked_list.Linked_list()
        else:
            result = []
        while(word1_p != None and word2_p != None):
            if(word1_p.data == word2_p.data):
                if(nesting):
                    result.insert(word1_p.data)
                else:
                    result.append(word1_p.data)
                word1_p = word1_p.next
                word2_p = word2_p.next
            elif(word1_p.data < word2_p.data):
                if(nesting):
                    result.insert(word1_p.data)
                else:
                    result.append(word1_p.data)
                word1_p = word1_p.next
            else:
                if(nesting):
                    result.insert(word2_p.data)
                else:
                    result.append(word2_p.data)
                word2_p = word2_p.next
        while(word1_p != None):
            if(nesting):
                result.insert(word1_p.data)
            else:
                result.append(word1_p.data)
            word1_p = word1_p.next
        while(word2_p != None):
            if(nesting):
                result.insert(word2_p.data)
            else:
                result.append(word2_p.data)
            word2_p = word2_p.next
        return result
    
    def __positional_intersect(self, word1_p, word2_p, k):
        """returns the positional intersect of two words with the distance k between them."""
        result = []
        while(word1_p != None and word2_p != None):
            if(word1_p.data == word2_p.data):
                word1_pos_list = word1_p.get_positions()
                word2_pos_list = word2_p.get_positions()
                i , j = 0, 0
                while((i < len(word1_pos_list)) and (j < len(word2_pos_list))):
                    if(abs(word1_pos_list[i] - word2_pos_list[j]) <= k):
                        result.append(word1_p.data)
                        break
                    elif(word1_pos_list[i] < word2_pos_list[j]):
                        i += 1
                    else:
                        j += 1
                word1_p = word1_p.next
                word2_p = word2_p.next         
            elif(word1_p.data < word2_p.data):
                word1_p = word1_p.next
            else:
                word2_p = word2_p.next
        return result
    
    def run_query(self, query):
        query = query.lower()
        porter = nltk.PorterStemmer()
        if("/" not in query): #query for inverted index
            query = nltk.word_tokenize(query)
            if(len(query) == 5): #if the query is three word joined by an operator.
                query_words = [query[0], query[2], query[4]] #extracting words from query
                #filtering out words and stemming them
                query_words[0] = "".join(char for char in query_words[0] if char.isalpha())
                query_words[1] = "".join(char for char in query_words[1] if char.isalpha())
                query_words[2] = "".join(char for char in query_words[2] if char.isalpha())
                query_words = [porter.stem(word) for word in query_words]
                #checking for invalid operators
                if((query[1] not in ["and", "andnot", "or"]) and (query[3] not in ["and", "andnot", "or"])):
                    return "Invalid Query Operator"
                w1 = self.__positional_index[query_words[0]]
                w2 = self.__positional_index[query_words[1]]
                w3 = self.__positional_index[query_words[2]]
                #checking operators and applying optimal query routine.
                if(query[1] == "and" and query[3] == "and"):
                    if((w1.size() + w2.size()) < (w2.size() + w3.size())):
                        return self.__and_operation(self.__and_operation(w1.get_head(), w2.get_head(), True).get_head(), w3.get_head())
                    else:
                        return self.__and_operation(w1.get_head(), self.__and_operation(w2.get_head(), w3.get_head(), True).get_head())
                if(query[1] == "and" and query[3] == "or"):
                    if((w1.size() + w2.size()) < (w2.size() + w3.size())):
                        return self.__or_operation(self.__and_operation(w1.get_head(), w2.get_head(), True).get_head(), w3.get_head())
                    else:
                        return self.__and_operation(w1.get_head(), self.__or_operation(w2.get_head(), w3.get_head(), True).get_head())
                if(query[1] == "and" and query[3] == "andnot"):
                    if((w1.size() + w2.size()) < (w2.size() + w3.size())):
                        return self.__andnot_operation(self.__and_operation(w1.get_head(), w2.get_head(), True).get_head(), w3.get_head())
                    else:
                        return self.__and_operation(w1.get_head(), self.__andnot_operation(w2.get_head(), w3.get_head(), True).get_head())
                if(query[1] == "or" and query[3] == "or"):
                    if((w1.size() + w2.size()) < (w2.size() + w3.size())):
                        return self.__or_operation(self.__or_operation(w1.get_head(), w2.get_head(), True).get_head(), w3.get_head())
                    else:
                        return self.__or_operation(w1.get_head(), self.__or_operation(w2.get_head(), w3.get_head(), True).get_head())
                if(query[1] == "or" and query[3] == "and"):
                    if((w1.size() + w2.size()) < (w2.size() + w3.size())):
                        return self.__and_operation(self.__or_operation(w1.get_head(), w2.get_head(), True).get_head(), w3.get_head())
                    else:
                        return self.__or_operation(w1.get_head(), self.__and_operation(w2.get_head(), w3.get_head(), True).get_head())
                if(query[1] == "or" and query[3] == "andnot"):
                    if((w1.size() + w2.size()) < (w2.size() + w3.size())):
                        return self.__andnot_operation(self.__or_operation(w1.get_head(), w2.get_head(), True).get_head(), w3.get_head())
                    else:
                        return self.__or_operation(w1.get_head(), self.__andnot_operation(w2.get_head(), w3.get_head(), True).get_head())
                if(query[1] == "andnot" and query[3] == "andnot"):
                    if((w1.size() + w2.size()) < (w2.size() + w3.size())):
                        return self.__andnot_operation(self.__andnot_operation(w1.get_head(), w2.get_head(), True).get_head(), w3.get_head())
                    else:
                        return self.__andnot_operation(w1.get_head(), self.__andnot_operation(w2.get_head(), w3.get_head(), True).get_head())
                if(query[1] == "andnot" and query[3] == "and"):
                    if((w1.size() + w2.size()) < (w2.size() + w3.size())):
                        return self.__and_operation(self.__andnot_operation(w1.get_head(), w2.get_head(), True).get_head(), w3.get_head())
                    else:
                        return self.__andnot_operation(w1.get_head(), self.__and_operation(w2.get_head(), w3.get_head(), True).get_head())
                if(query[1] == "andnot" and query[3] == "or"):
                    if((w1.size() + w2.size()) < (w2.size() + w3.size())):
                        return self.__or_operation(self.__andnot_operation(w1.get_head(), w2.get_head(), True).get_head(), w3.get_head())
                    else:
                        return self.__andnot_operation(w1.get_head(), self.__or_operation(w2.get_head(), w3.get_head(), True).get_head())
            elif(len(query) == 3): #if the query is two word joined by an operator.
                query_words = [query[0], query[2]] #extracting words from query
                #filtering out words and stemming them
                query_words[0] = "".join(char for char in query_words[0] if char.isalpha())
                query_words[1] = "".join(char for char in query_words[1] if char.isalpha())
                query_words = [porter.stem(word) for word in query_words]
                #checking for invalid operators
                if(query[1] not in ["and", "andnot", "or"]):
                    return "Invalid Query Operator"
                #returning query according to the operator
                if(query[1] == "and"):
                    return self.__and_operation(self.__positional_index[query_words[0]].get_head(), self.__positional_index[query_words[1]].get_head())
                elif(query[1] == "andnot"):
                    return self.__andnot_operation(self.__positional_index[query_words[0]].get_head(), self.__positional_index[query_words[1]].get_head())
                elif(query[1] == "or"):
                    return self.__or_operation(self.__positional_index[query_words[0]].get_head(), self.__positional_index[query_words[1]].get_head())
            elif(len(query) == 1): #if the query is a single word.
                #filtering and stemming word
                query = "".join(char for char in query if char.isalpha())
                query = porter.stem(query)
                current = self.__positional_index[query].get_head()
                result = []
                while(current != None):
                    result.append(current.data)
                    current = current.next
                return result
        else: #query for positional index
            query = nltk.word_tokenize(query)
            query[2] = int(query[2].replace('/', ''))
            query_words = [query[0], query[1]]
            query_words[0] = "".join(char for char in query_words[0] if char.isalpha())
            query_words[1] = "".join(char for char in query_words[1] if char.isalpha())
            query_words = [porter.stem(word) for word in query_words]
            if((len(query) != 3) or (query[2] not in [1, 2, 3, 4, 5, 6, 7, 8, 9])):
                return "Invalid Query"
            return self.__positional_intersect(self.__positional_index[query_words[0]].get_head(), self.__positional_index[query_words[1]].get_head(), query[2])