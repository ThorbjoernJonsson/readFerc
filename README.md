# readFerc
Downloads pdf files from the Ferc webpage.

This file uses the scrapy package to read files with specific criteria from the Ferc webpage.

1st time set up:
1) Create a folder on your computer called bricket-scraper
2) In the folder bricket-scraper create a new folder called downloaded_emails
3) Save the two files, ferc_scraper.py and keep_running.py in the bricket_scraper folder.
4) Open a command window and install the following packages.
5) pip install scrapy
6) pip install urllib3
7) pip install datetime
8) pip install schedule


Daily running:
1) Open the command window in the bricket-scraper folder.
2) Run by typing scrapy runspider ferc_sraper.py
