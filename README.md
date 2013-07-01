google-jawa
===========

Export the contents of a Google Reader account to JSON


Usage
-----

Install the `google-jawa` package, and then point it at the Google
account that you want to archive. The program will prompt you for your
password and begin downloading the contents of the reader account

    $ pip install google_jawa
    $ google-jawa -d <backup_directory> <google username>


Output Format
-------------

Every output file contains one JSON object per line.
