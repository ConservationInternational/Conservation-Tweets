while read VAR; do
	python wordcloud_cli.py --text "$VAR""_words.csv" --imagefile "$VAR""_cloud.png" --stopwords stopwords.txt --width 1000 --height 1000 --background white
done <PMI_files.txt
