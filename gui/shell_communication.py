import subprocess
import os

class Execute(object):
    def __init__(self, *args_1, cwd=os.getcwd(), **args_2):
        if 'encoding' in args_2:
            self.encoding = args_2.pop('encoding')
        else:
            self.encoding = 'utf-8'
        self.popen = subprocess.Popen(
            *args_1,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, 
            encoding=self.encoding,
            cwd=cwd, 
            **args_2)
    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def send(self, message, recieve=True, incr=False):
        message = message.rstrip('\n')
        if not incr and '\n' in message:
            raise ValueError("message in \\n!")
        self.popen.stdin.write(message + '\n')
        self.popen.stdin.flush()
        if recieve:
            return self.recieve()
        return None

    def recieve(self):
        self.popen.stdout.flush()
        return self.popen.stdout.readline()

    def return_code(self):
        return self.popen.returncode

    def close(self):
        self.popen.stdin.close()
        
    def wait(self):
        self.popen.wait()
