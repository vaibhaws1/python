# Created by: Vaibhaw Shende
# Updated Date: Apr-19-2018

train_path = "../resource/lib/publicdata/aclImdb/train/" # use terminal to ls files under this directory
test_path = "../resource/asnlib/public/imdb_te.csv" # test data for grade evaluation

TEST_MODE = False
import pandas  
import os
import numpy
import sklearn
    
def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    '''Implement this module to extract
    and combine text files under train_path directory into 
    imdb_tr.csv. Each text file in train_path should be stored 
    as a row in imdb_tr.csv. And imdb_tr.csv should have two 
    columns, "text" and label'''

    print(">> imdb_data_preprocess ..")
    
    # Read stopwords
    with open("stopwords.en.txt", 'r', encoding="ISO-8859-1") as f:
        content = f.readlines()
    stopwords = [x.strip() for x in content]
	
    combined_text_list = []
    row_number = 0

    # Read pos 
    for filename in os.listdir(inpath+"pos"):
        sentence = open(inpath+"pos/"+filename, 'r', encoding="ISO-8859-1").read()
        sentence = strip_text_of_stopwords (sentence, stopwords)
        combined_text_list.append([row_number,sentence,'1'])
        row_number += 1

    # Read neg
    for filename in os.listdir(inpath+"neg"):
        sentence = open(inpath+"neg/"+filename, 'r', encoding="ISO-8859-1").read()
        sentence = strip_text_of_stopwords (sentence, stopwords)
        combined_text_list.append([row_number,sentence,'0'])
        row_number += 1
    
	# Mix data
    if mix:
        numpy.random.shuffle(combined_text_list)
		
    # Write combined_text_list to file
    df = pandas.DataFrame(data = combined_text_list, 
                         columns=['row_Number', 'text', 'polarity'])
    df.to_csv(outpath+name, index=False, header=True)
    print(">> clean text written to :", (outpath+name), " lines =", row_number)
	
    pass
  
def strip_text_of_stopwords (sentence, stopwords):
	words = sentence.split()
	stripped_words = []
	for word in words:
		if word not in stopwords:
			stripped_words.append(word)
	new_sentence = ' '.join(stripped_words)
	return new_sentence

def get_clean_data(filename, getTrainingData = True):
    data = pandas.read_csv(filename,header=0, encoding = 'ISO-8859-1')
    
    if getTrainingData:
        X = data['text']
        Y = data['polarity']
        return X, Y
    else:
        X = data['text']
        return X	

def unigram_process(data):
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer()
    vectorizer = vectorizer.fit(data)
    return vectorizer	

def bigram_process(data):
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(ngram_range=(1,2))
    vectorizer = vectorizer.fit(data)
    return vectorizer

def tfidf_process(data):
    from sklearn.feature_extraction.text import TfidfTransformer 
    transformer = TfidfTransformer()
    transformer = transformer.fit(data)
    return transformer
	
def SGD_Classifier(X, Y, Xtest):
    from sklearn.linear_model import SGDClassifier 
    classifier = SGDClassifier(loss="hinge", penalty="l1", n_iter=20)
    classifier.fit(X, Y)
    Ytest = classifier.predict(Xtest)
    return Ytest

def write_output(data, filename):
    file = open(filename, 'w')
    for polarity in data:
        file.writelines(str(polarity)+'\n')
    file.close()
    pass 
    
#if TEST_MODE: imdb_data_preprocess(inpath="./",outpath="./",name="imdb_tr.csv", mix=True)

if __name__ == "__main__":

    if TEST_MODE: train_path = "./" 
    if TEST_MODE: test_path = "./imdb_te.csv"

    import sklearn
    print ("Initiating __main__")
    imdb_data_preprocess(inpath=train_path, mix=True)
    [Xtrain_text, Ytrain] = get_clean_data ("imdb_tr.csv", True)
    Xtest_text = get_clean_data (test_path, False)

    '''train a SGD classifier using unigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''
    print ("unigram: train a SGD classifier using unigram representation..")
    unigram_vectorizer = unigram_process(Xtrain_text)
    Xtrain_uni = unigram_vectorizer.transform(Xtrain_text)
    print ("unigram: predict sentiments on imdb_te.csv..")
    Xtest_uni = unigram_vectorizer.transform(Xtest_text)
    Ytest_uni = SGD_Classifier (Xtrain_uni, Ytrain, Xtest_uni)
    print ("unigram: write output to unigram.output.txt")
    write_output(Ytest_uni, "unigram.output.txt")
    
    '''train a SGD classifier using bigram representation,
    predict sentiments on imdb_te.csv, and write output to
    bigram.output.txt'''
    print ("bigram: train a SGD classifier using bigram representation..")
    bi_vectorizer = bigram_process(Xtrain_text)
    Xtrain_bi = bi_vectorizer.transform(Xtrain_text)
    print ("bigram: predict sentiments on imdb_te.csv..")
    Xtest_bi = bi_vectorizer.transform(Xtest_text)
    Ytest_bi = SGD_Classifier (Xtrain_bi, Ytrain, Xtest_bi)
    print ("bigram: write output to bigram.output.txt")
    write_output(Ytest_bi, "bigram.output.txt")
    
    '''train a SGD classifier using unigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to unigramtfidf.output.txt'''
    print ("unigramtfidf: train a SGD classifier using unigram representation with tf-idf..")
    uni_tfidf_transformer = tfidf_process(Xtrain_uni)
    Xtrain_tf_uni = uni_tfidf_transformer.transform(Xtrain_uni)
    print ("unigramtfidf: predict sentiments on imdb_te.csv..")
    Xtest_tf_uni = uni_tfidf_transformer.transform(Xtest_uni)
    Ytest_tf_uni = SGD_Classifier (Xtrain_tf_uni, Ytrain, Xtest_tf_uni)
    print ("unigramtfidf: write output to unigramtfidf.output.txt")
    write_output(Ytest_tf_uni, "unigramtfidf.output.txt")
    
    '''train a SGD classifier using bigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to bigramtfidf.output.txt'''
    print ("bigramtfidf: train a SGD classifier using bigram representation with tf-idf..")
    bi_tfidf_transformer = tfidf_process(Xtrain_bi)
    Xtrain_tf_bi = bi_tfidf_transformer.transform(Xtrain_bi)
    print ("bigramtfidf: predict sentiments on imdb_te.csv..")
    Xtest_tf_bi = bi_tfidf_transformer.transform(Xtest_bi)
    Ytest_tf_bi = SGD_Classifier (Xtrain_tf_bi, Ytrain, Xtest_tf_bi)
    print ("bigramtfidf: write output to bigramtfidf.output.txt")
    write_output(Ytest_tf_bi, "bigramtfidf.output.txt")
    
    pass

