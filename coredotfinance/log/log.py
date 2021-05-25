import os
import logging

logger = logging.getLogger("log")
logger.setLevel(logging.DEBUG)

# make log directory once.
if os.path.isfile("coredotfinance/log"):
    os.mkdir("coredotfinance/log")

log_file = "coredotfinance/log/userlogfile.log"
if not os.path.isfile(log_file):
    with open(log_file, "w") as f:
        f.write("")

fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class Log:
    @staticmethod
    def info(func):
        def wrapper(name=None, start=None, end=None):
            logger.info(f"\tname :\t{name}\tstart :\t{start}\tend :\t{end}")
            if name is None:
                name = "all"
            return func(name, start, end)

        return wrapper
