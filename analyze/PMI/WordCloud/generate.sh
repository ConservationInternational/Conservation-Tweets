#!/bin/bash
for VAR in "$@"
do
	echo "reading words for ""$VAR"
	python makewords.py "$VAR"
	echo "generating word cloud for ""$VAR"
	wordcloud_cli.py --text "$VAR""_words.txt" --imagefile "$VAR""_cloud.png" --stopwords stopwords.txt --width 1000 --height 1000 --background white
	echo "done!"
done
