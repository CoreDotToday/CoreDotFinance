import logging


logger = logging.getLogger('log')
logger.setLevel(logging.DEBUG)

# sh = logging.StreamHandler()
# sh.setLevel(logging.INFO)

fh = logging.FileHandler('coredotfinance/log/userlogfile.log')
fh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# sh.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(fh)
# logger.addHandler(sh)


class Log:
    @staticmethod
    def info(func):
        def wrapper(name=None, start=None, end=None):
            logger.info(f'\tname :\t{name}\tstart :\t{start}\tend :\t{end}')
            if name is None:
                name = 'all'
            return func(name, start, end)
        return wrapper
