from subprocess import Popen
from threading import Thread

def server():
    p = Popen("C:\\corenlp\\run.bat")
    p.wait()

def run_server():
    thread = Thread(target=server)
    thread.daemon = True
    thread.start()