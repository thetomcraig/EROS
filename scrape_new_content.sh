cd ${HOME}/Dropbox/TomCraig/Logs/EROS

file_name=${HOSTNAME}_database_output_$(date +"%F").txt
touch $file_name

echo $(date) >> $file_name
echo ","  >> $file_name

${HOME}/.virtualenvs/EROS/bin/python manage.py scrape twitter_users:all facebook_users:none >> $file_name

