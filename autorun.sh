#! /bin/sh

echo "
_______________________
"

date

echo "
Starting scraper
"

# TO USE THE SCRIPT FROM DIFFERENT LOCATION
# SET THE PROJECT PATH
project_path=$(pwd)

cd "$project_path"

source "$project_path/venv/bin/activate"

cd "$project_path/devBG/devBG"

scrapy crawl job

echo "
_______________________
"
