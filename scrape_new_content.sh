logs_path=${HOME}/Dropbox/TomCraig/Logs/EROS
cd $logs_path

#Remove 'latest' from the last log file
latest=$(find . -name "$(hostname)*-latest*")
echo "Removing $latest"

mv -i $latest `echo $latest | sed -e 's/-latest//g'`

#Make new log file
file_name=$(hostname)-database-output-latest-$(date +"%y-%m-%d-%H-%M-%S").txt
touch $file_name

#Write to the file
cd ${HOME}/Dropbox/TomCraig/Projects/EROS/
${HOME}/.virtualenvs/EROS/bin/python manage.py scrape --twitter_users existing --apply_markov_chains all >> $logs_path/$file_name
