logs_path=${HOME}/Dropbox/TomCraig/Logs/EROS
cd $logs_path
file_name=$(hostname)_database_output_$(date +"%y-%m-%d-%H-%M-%S").txt
touch $file_name

cd ${HOME}/Dropbox/TomCraig/Projects/EROS/
${HOME}/.virtualenvs/EROS/bin/python manage.py scrape --twitter_users existing >> $logs_path/$file_name
