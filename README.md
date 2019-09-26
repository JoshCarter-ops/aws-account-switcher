##AWS Account Switcher

`WARNING => Make a backup of your .aws/credentials folder before using this utility!
 Also the default rotation time is 30 days!`

Repository to allow you to switch to various AWS Accounts, rotate your access keys and assume roles on the command line without the need of exporting those pesky bash env vars!

### Components
* switcher.py
* profiles_example.json
* profiles.json

#### What to do? 
1. Create a profiles.json in the project for yourself (copy/rename the profiles_example.json)
2. Update the values for the accounts you wish to switch to (home, work, nonprod, prod etc.)
3. Run using `python3 switcher.py`