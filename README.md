# Web Scrapers

## Overview

This is a **scrapy** project with a spider scraping [DevBG](dev.bg) for all **Python** job offers available.

All data is stored in **sqlite3** database for consistency. The data stored consists of `position, company, location, posting date and link to the offer`.

**Deltafetched** is used to skip all previous data from current search.

After each scraping an email with all unsent offers from the las 2 days is sent.

The runtime of the scraper is automated with **cron**.

The scraper is meant to be hosted on a web server which I did with an EC2 server on AWS.

## Setup and Schedule on Linux

1. Clone the Repo

   ```sh
   git clone https://github.com/ivo-bass/scrapers.git
   ```

2. Create virtual environment

   ```sh
   cd scrapers

   python3 -m venv venv
   ```

3. Activate virtual environment

   ```sh
   source /venv/bin/activate
   ```

4. Install requirements

   ```sh
   pip install -r requirements.txt
   ```

5. Create config file for email sender credentials

   ```sh
    cd devBG/devBG

    mkdir config && cd config && touch __init__.py

    echo "
    EMAIL_USER = 'change_this_to_your_email_address'
    EMAIL_PASS = 'change_this_to_your_email_password'
    " > config.py

    cd ../../..
   ```

6. Install **`cron`** if not present

7. Set cron task

   - Open cron task scheduler

     ```sh
     crontab -e
     ```

   - Set runtime

     _You can generate time code [HERE](https://crontab.guru/)_

     ```cron
     * * * * * sh /path/to/script/autorun.sh >> autorun.log
     ```

   - Check if the task is set

     ```sh
     crontab -l
     ```

8. Enjoy!
