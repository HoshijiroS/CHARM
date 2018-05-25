import datetime
from CHARM.settings import LOG_DIR

CURRENT_LOG = []


def log(speaker, text):
    CURRENT_LOG.append((datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), speaker, text))


def save_log():
    file = open(LOG_DIR + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".txt", "w+")

    for x in CURRENT_LOG:
        file.write("[" + x[0] + "] " + x[1] + ": " + x[2] + "\n")

    file.close()