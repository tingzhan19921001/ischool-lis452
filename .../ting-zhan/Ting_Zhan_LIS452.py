# Github link: https://github.com/tingzhan19921001/ischool-lis452/blob/master/Ting_Zhan_LIS452.py
# suggested news link to test: http://www.chinadaily.com.cn/business/2017-05/11/content_29300055.htm
# suggested news link to test: http://www.chinadaily.com.cn/business/tech/2017-05/11/content_29303225.htm
# suggested news link to test: http://www.chinadaily.com.cn/business/2017-05/11/content_29296091.htm
# please copy the any of the links above and give it to the tool.
# The results in the screenshot illustrated in the report comes out of the third link, just for your information.


from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
import re
import lxml.html
import operator # to sort by keys

def retrieve_news():
    
    f = open('news.txt','w',encoding='UTF8')
    
    # to give the news link 
    url = input('Give me the news and let me summarize for you:')
    
    # Fetch the url web page, and convert the response into an HTML document tree:
    tree = lxml.html.parse(url)
    
    # to get the news title
    title = tree.xpath('//title/text()')
    print('News title: ', title[0])
    
    # to get the news body
    body = tree.xpath('//p/text()')
    #print(len(body))
    #body = body.split()
    
    #to change the body news into a form of string
    str_body = ''.join(body)
    
    #print(type(str_body))
    #str_body = ''.join(str(e) for e in body)
    byte_body = str_body.encode('UTF8')
    # encode, decoode method to solve the unicodeerror
    new_body = byte_body.decode(encoding='UTF-8')
    #write the body into the file for future use
    f.write(new_body)
    
    f.close()
    
    
retrieve_news()
# by far, a text file name 'news.txt' which contains the news  has been created. Save it for future use


stopwords = set(stopwords.words('english')+list(punctuation))
#stopwords here contain high-frequency daily words in ourlife, such as I, am, are, do, and the like,
#these words should not be considered as the keywords, neither should punctuation.

#print(stopwords)


def byFreq(pair):
    return pair[1]  # to return the tuple with the position index = 1

def main():
    
    #raw_text = open('news.txt' ,'r',encoding='ISO-8859-1').read()
    # news.txt is what the retrieve_new() create
    raw_text = open('news.txt' ,'r',encoding='UTF8').read()
    text = raw_text.lower() #to make all the words in files lowerclass
    #for ch in '!"\'#$%&()\'*+,-./:;<=>?@[\\]^_`{|}~': # to get rid of punctuations
        #text = text.replace(ch, ' ') #we already have stopwords which include punctuations
    words = text.split()
    print('Originally there are {} words in the text.\n'.format(len(words)))
    # to remove the stopwords and thereby create a new list that contain all the words from the text except stopwords
    new_list=[x for x in words if x not in stopwords]

    print('After removing stopwords,{} words are left.\n'.format(len(new_list)))



    counts = defaultdict(int)
    #print(new_list)

    for w in new_list:
        # each time add 1 more
        counts[w] += 1
    # items is a list,each item contains the word itself and the frequency of that word 
    items = list(counts.items())
    #print(items)
    #items.sort()
    items.sort(key = byFreq, reverse = True)
    #print(items[:5])

    print('There are {} distinct words.\n'.format(len(items)))
    # to see how many distinct words in the text given
    distinct_words = int(len(items))
    
    #tokenize the sentence
    sentences = sent_tokenize(raw_text)
    #print(len(sentences))
    
    #tokenize the words in one sentence
    word_in_sentence =[word_tokenize(s) for s in sentences]

    list_word_value=[]
    for i in range(len(items)):
        single_word, frequency = items[i]
        # to give an equation to calculate the word's importance, so that we could rank the word's value
        single_word, important_value = items[i][0], frequency/len(new_list)
        # to build up a new list that contain the word and its importance value
        list_word_value.append((single_word,important_value))
    
    # to change it into a dictionary
    dict_of_word_value = dict(list_word_value)
    #print(dict_of_word_value.get('first'))
    print('There are {} sentences in this news!\n'.format(len(sentences)))
    #single_sentence_value = []
    
    # build up a new dictionary whose key is the sentence itself and whose value is the sentence value.
    dict_sentence = {}
    for i in range(len(sentences)):
        sentences_value = 0
        # from here, we start calculating the sentence value by adding every single word's value
        for word in word_in_sentence[i]:
            if word.lower() in new_list:
                word=word.lower()
                # add each word's value together
                sentences_value = float(sentences_value) + dict_of_word_value.get(word)
        # multiple the real value by 10000 for future calculation
                #calculation of sentence value is wrong, reconsider it.
        #print(sentences[i],'\n',sentences_value/items[i][1]*10000)
        #print(i,sentences[i])
        
        #to append the sentence: sentence_value to the dictionary
        dict_sentence.update({sentences_value : sentences[i]}) #to append each sentence with it value, making them a dictionary
        
    #print(dict_sentence)
    
    sentence_items = dict_sentence.items()
    #sentence_items.sort()
    
    # operator.itemgetter(0) to get key and then to sort by key, the key is each sentence value
    # operator.itemgetter(1) is to get value
    sorted_sentence_items = sorted(dict_sentence.items(), key=operator.itemgetter(0),reverse=True)
    #print(type(sentence_items))
    #print(type(sorted_sentence_items))
    
    #print(sentence_items.get())
    a = 0
    print('News abstract:')
    for i in range(len(sentences)):
        # every 10 sentence more, add one more sentence to the abstract
        if (i % 10) == 0:
            #print(a)
            print(sorted_sentence_items[a][1])
            # increase by one unit each time
            a += 1
    #print(sorted_sentence_items[2][1])
    
if __name__ == '__main__':
    main()
