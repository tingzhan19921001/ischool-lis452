
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
import re
import lxml.html

def retrieve_news():
    f = open('news.txt','w',encoding='UTF8')
    
    # In the search URL below, the 'mh' key says how many results to return per page. Default is 100.
    url = input('Give me the news and let me summarize for you:')
    
    # Fetch the url web page, and convert the response into an HTML document tree:
    tree = lxml.html.parse(url)
    
    title = tree.xpath('//title/text()')
    print('Page title: ', title[0])
    
    body = tree.xpath('//p/text()')
    print(len(body))
    #body = body.split()
    
    str_body = ''.join(body)
    
    #print(type(str_body))
    #str_body = ''.join(str(e) for e in body)
    byte_body = str_body.encode('UTF8')
    new_body = byte_body.decode(encoding='UTF-8')
    f.write(new_body)
    
    f.close()
    
    
retrieve_news()


stopwords = set(stopwords.words('english')+list(punctuation))
#stopwords here contain high-frequency daily words in ourlife, such as I, am, are, do, and the like,
#these words should not be considered as the keywords, neither should punctuation.

#print(stopwords)


def byFreq(pair):
    return pair[1]  # to return the tuple with the position index = 1

def word_score():
    
    #raw_text = open('news.txt' ,'r',encoding='ISO-8859-1').read()
    raw_text = open('news.txt' ,'r',encoding='UTF8').read()
    text = raw_text.lower() #to make all the words in files lowerclass
    #for ch in '!"\'#$%&()\'*+,-./:;<=>?@[\\]^_`{|}~': # to get rid of punctuations
        #text = text.replace(ch, ' ') #we already have stopwords which include punctuations
    words = text.split()
    print('Originally there are {} words in the text'.format(len(words)))
    new_list=[x for x in words if x not in stopwords]

    print('After removing stopwords,{} words are left'.format(len(new_list)))



    counts = defaultdict(int)
    #print(new_list)

    for w in new_list:
        counts[w] += 1

    items = list(counts.items())
    #items.sort()
    items.sort(key = byFreq, reverse = True)
    #print(items[:5])

    print('There are {} distinct words'.format(len(items)))
    distinct_words = int(len(items))

    sentences = sent_tokenize(raw_text)
    #print(len(sentences))

    word_in_sentence =[word_tokenize(s) for s in sentences]

    list_word_value=[]
    for i in range(len(items)):
        single_word, frequency = items[i]
        single_word, important_value = items[i][0], frequency/len(new_list)
        list_word_value.append((single_word,important_value))

    dict_of_word_value = dict(list_word_value)
    #print(dict_of_word_value.get('first'))

    single_sentence_value = []
    dict_sentence = {}
    for i in range(len(sentences)):
        sentences_value = 0
        for word in word_in_sentence[i]:
            if word.lower() in new_list:
                word=word.lower()
                sentences_value = float(sentences_value) + dict_of_word_value.get(word)
        # multiple the real value by 10000 for future calculation
                #calculation of sentence value is wrong, reconsider it.
        #print(sentences[i],'\n',sentences_value/items[i][1]*10000)
        #print(i,sentences[i])
        dict_sentence.update({sentence : sentences[i]}) #to append each sentence with it value, making them a dictionary
        
    print(dict_sentence[0])
        
    #if len(sentences)



word_score()
