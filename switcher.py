import os
import json
from getpass import getpass
from datetime import date

username = ""
account_decision = ""
profile_json = {}
profile_object = {}
homedir = os.path.expanduser('~')
aws_credentials_master = homedir + "/.aws/credentials"
template = {'profile': '[default]', 'output = ': 'json', 'region = ': 'eu-west-1'}


# For logging outputs
def log(level, message):
    print("[{}]: {}".format(level.upper(), message))


def get_json():
    with open('./profiles.json', 'r') as json_file:
        global profile_object
        profile_object = json.load(json_file)
        return profile_object


def get_profile_info(key=""):
    return_data = []
    data = get_json()
    if key != "":
        for profile in data['profiles']:
            return_data.append(profile[key])
    else:
        for profile in data['profiles']:
            return_data.append(profile)
    return return_data


def ask_the_question():
    question = 'Which account are you trying to access?'
    count = 1
    for account in get_profile_info("type"):
        question += ("\n\t [" + str(count) + "] " + account)
        count += 1
    question += "\n\n[INPUT]: "
    return question


def bash(cmd):
    return os.popen(cmd).read()


def write_standard_account(account_int):
    global username
    try:
        tmp_template = {}
        profiles = get_json()['profiles']
        global profile_json
        profile_json = (profiles[int(account_int) - 1])
        username = profile_json['username']
        tmp_template["aws_access_key_id = "] = profile_json["aws_access_key_id"]
        tmp_template["aws_secret_access_key = "] = profile_json["aws_secret_access_key"]
        template.update(tmp_template)
        with open(aws_credentials_master, 'w') as aws_cred_file:
            for k, v in template.items():
                if k == 'profile':
                    aws_cred_file.write(v + '\n')
                else:
                    aws_cred_file.write(k + v + '\n')
        log("INFO", "Switched to {}".format(profile_json['type']))
    except IndexError:
        log("ERROR", "INDEX OUT OF BOUND")


def get_key_meta_data():
    return json.loads(bash('aws iam list-access-keys --user-name {}'.format(username)))['AccessKeyMetadata'][0]


def check_key_quota():
    data = json.loads(bash('aws iam list-access-keys --user-name {}'.format(username)))
    return len(data['AccessKeyMetadata'])


def format_date(date_to_format):
    return date(int(date_to_format[0:4]), int(date_to_format[5:7]), int(date_to_format[8:10]))


def rotate_keys():
    today = format_date(str(date.today()))
    create_date = format_date(get_key_meta_data()['CreateDate'])
    delta = today - create_date
    log('INFO', 'Key Age: {} days old'.format(str(delta.days)))

    if check_key_quota() > 1:
        log('INFO', 'You have 2 keys attached to your account, please remove 1 to allow key rotation.')
        return

    if delta.days > 30:
        dated_key = profile_json['aws_access_key_id']
        log('INFO', 'Keys are old - Auto Rotation occurring')

        with open("profiles.json", "w") as config:
            new_key = json.loads(bash('aws iam create-access-key --user-name {}'.format(username)))['AccessKey']
            profile_json['aws_access_key_id'] = new_key['AccessKeyId']
            profile_json['aws_secret_access_key'] = new_key['SecretAccessKey']
            profile_object['profiles'][int(account_decision) - 1] = profile_json
            config.write(json.dumps(profile_object))

        # DEACTIVATE OLD KEY
        bash('aws iam delete-access-key --access-key-id {} --user-name {}'.format(dated_key, username))

        # Write the new keys to the credentials file
        write_standard_account(int(account_decision))


def mfa():
    command = 'aws sts get-session-token --serial-number '
    command += profile_json['mfa']
    command += ' --token-code '
    command += getpass('[INPUT] - MFA Code: (Hidden) ')

    return command


def assume_role():
    role = profile_json['role']
    log('INFO', 'Assuming the role: {}\n'.format(role))

    command = "aws sts assume-role"
    command += " --role-arn arn:aws:iam::{}:role/{}".format(profile_json['account_number'], role)
    command += " --role-session-name AWS-CLI-Session"
    if profile_json['duration'] == "":
        command += " --duration-seconds 3600"
    else:
        command += " --duration-seconds {}".format(profile_json['duration'])
    command += " --serial-number {} --token-code ".format(profile_json['mfa'])
    command += getpass('[INPUT] - MFA Code: (Hidden) ')

    return command


def write_session(command):
    credentials = {'profile': '[default]', 'output = ': 'json', 'region = ': 'eu-west-1'}
    json_creds = json.loads(bash(command))

    cred_info = json_creds['Credentials']

    credentials['aws_access_key_id = '] = cred_info['AccessKeyId']
    credentials['aws_session_token = '] = cred_info['SessionToken']
    credentials['aws_secret_access_key = '] = cred_info['SecretAccessKey']

    with open(aws_credentials_master, 'w') as aws_cred_file:
        for k, v in credentials.items():
            if k == 'profile':
                aws_cred_file.write(v + '\n')
            else:
                aws_cred_file.write(k + v + '\n')


if __name__ == '__main__':
    account_decision = input(ask_the_question())
    write_standard_account(account_decision)
    rotate_keys()
    question = '[INFO]: Would you like to assume the {} role?\n[1] YES\n[2] NO\n[INPUT]: '

    if profile_json['role'] != "":
        decider = input(question.format(profile_json['role']))
        if str(decider) == "1":
            write_session(assume_role())
        else:
            log('INFO', "Logging in with {}'s mfa.".format(username))
            write_session(mfa())
    else:
        log('INFO', "No role found in profiles.json, logging in with {}'s mfa.".format(username))
        write_session(mfa())
    log('INFO', "Script executed successfully!")
