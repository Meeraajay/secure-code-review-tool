
import subprocess

def unsafe_evaluation(user_input):
    eval(user_input)


def unsafe_command(command):
    subprocess.run(command, shell=True)
