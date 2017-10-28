# cat download_list.txt | cut -d$'\n' -f1 
while read in;
do 
	stringarray=($in)
	path=${stringarray[0]}
	url=${stringarray[1]}
	if (( ${#path} > 0 )) && (( ${#url} > 0 ))
		then wget $url -P $path
	fi
done < download_list.txt
# for p in $(xargs < download_list.txt);
# do 
# 	echo $p
# 	# wget --adjust-extension $p
# done