# Change log
This change log will act as a record of all changes to the aws role refresh.

## -> 26-09-19
### Added
- Initial build of the python script

## -> 27-09-19
- Added key quota check for the rotation, it will now take into account that if there are 2 keys it won't try auto
 rotating until the user has removed the oldest one.
- Added a duration(in seconds) option to allow users to specify how long they want to assume the role for, default will
 be 1 hour
 unless overwritten. This will also depend on whether you have specified the role can be assumed for that amount of
  time in AWS.