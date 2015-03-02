## Lennon reviews Mendel

* Errors are thrown on line 92 `km.predict(vectorizer.fit_transform(questions))` (as you already pointed out in the slides).
* My machine doesn't recognize several characters in the data, for instance see `questions[14]`
* I'm assuming that these values become np.nan arrays under the hood and vectorizer.fit throws the error, "np.nan is an invalid document, expected byte or unicode string."
* Can you pre-process the questions data so that all non-Latin characters are removed?  
* The LDA portion of the code looks interesting.  I was able to run it using your test sentence, but be sure to import CountVectorizer `from sklearn.feature_extraction.text import CountVectorizer
` before trying to run line 116 `vect = CountVectorizer(stop_words='english', ngram_range=[1,3])` 


* The answer to Hawks or Wings is clearly "Hawks."