PNG= Lexical_variety.png Number_of_words.png Polarity.png \
	SMOG_index.png Subjectivity.png

dist: $(PNG)
	cp $(PNG) /dds/pubs/web/blog/20170120/

$(PNG): readability_charts.py
	python readability_charts.py speeches/*
