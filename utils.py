import subprocess

ROBOT_ID = 'SAMPLE_ROBOT_ID'

USERS = {
    'SMAPLE_USERID': 'UserName'
}


def say(text, lang_version=0):
    if lang_version == 0:
        subprocess.call(['say', str(text), '-v', 'Karen', '-r 150'])
    elif lang_version == 1:
        subprocess.call(['say', str(text), '-v', 'Ting-Ting', '-r 150'])
    elif lang_version == 2:
        subprocess.call(['say', text, '-v', 'Kyoko', '-r 150'])
