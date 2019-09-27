# Change log
This change log will act as a record of all changes to the aws role refresh.

## -> 26-09-19
### Added
- Initial build of the python script

## -> 27-09-19
- Added key quota check for the rotation, it will now take into account that if there are 2 keys it won't try auto
 rotating until the user has removed the oldest one.