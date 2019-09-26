## AWS Account Switcher

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

### Why?
`This script was written to enable read only users to assume a role to run cli commands that they normally wouldn't
 have permissions to do. 
 The script since then has developed into a auto key rotator and account switcher. 
 This was initially written by myself for the developers where I work, it was suggested that I open source it because
  'it's a nightmare switching accounts/roles manually!'. 
 `
