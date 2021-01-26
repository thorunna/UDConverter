
# example usage:
# count_dir_words.sh additions2019/althingi/bo/2013/

directory=$1

for file in $directory/*; do
  word_num=$(sed '/#/d' $file | sed '/^$/d' | wc -l)
  filename=${file##*/}
  # echo -e "$filename\t$word_num"
  echo $word_num
done