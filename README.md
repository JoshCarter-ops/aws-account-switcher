## AWS Account Switcher

```WARNING
Make a backup of your .aws/credentials folder before using this utility!
Also the default rotation time is 30 days!
```

Repository to allow you to switch to various AWS Accounts, rotate your access keys and assume roles on the command line without the need of exporting those pesky bash env vars!

### Components
* switcher.py
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
 
`SIDE-NOTE: Durarion is in seconds...3600 for an hour is the default`

### profiles.json example
`
{
  "profiles": [
    {
      "type": "personal",
      "role": "role",
      "account_number": "0011223344",
      "username": "someone@example.com",
      "aws_access_key_id": "PERSONALACCESSKEY",
      "aws_secret_access_key": "PERSONALSECRETACCESSKEY",
      "mfa": "arn:aws:iam::0011223344:mfa/someone@example.com",
      "duration": ""
    },
    {
      "type": "work",
      "role": "role",
      "account_number": "0011223355",
      "username": "someone@work.com",
      "aws_access_key_id": "WORKACCESSKEY",
      "aws_secret_access_key": "WORKSECRETACCESSKEY",
      "mfa": "arn:aws:iam::0011223355:mfa/someone@example.com",
      "duration": ""
    }
  ]
}
`
