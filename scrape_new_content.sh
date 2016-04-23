logs_path=${HOME}/Dropbox/TomCraig/Logs/EROS
cd $logs_path

file_name=${HOSTNAME}_database_output_$(date +"%F").txt
if [[ ! $file_name ]]; then touch $file_name; fi

cd ${HOME}/Dropbox/TomCraig/Projects/EROS/
${HOME}/.virtualenvs/EROS/bin/python manage.py scrape twitter_users:all facebook_users:none >> $logs_path/$file_name

