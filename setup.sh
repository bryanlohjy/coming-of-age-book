for p in $(xargs < directory_list.txt);
do
	mkdir -p ${p}
done
bash download.sh