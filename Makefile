PNG= Flesh_reading_ease.png Gunning_fog_index.png Lexical_variety.png \
Number_of_words.png SMOG_index.png

dist: $(PNG)
	cp $(PNG) /dds/pubs/web/blog/20170120/

$(PNG): readability_charts.py
	python readability_charts.py speeches/*
