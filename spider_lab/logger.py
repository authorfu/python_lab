#!/usr/bin/env python
#-*- coding:utf-8 -*-

__all__ = ['logger', 'init']

import logging

logger = logging.getLogger('spider')

LOG_LEVELS = [logging.CRITICAL, logging.ERROR, logging.WARNING,
                    logging.INFO, logging.DEBUG]

FORMAT = logging.Formatter('%(asctime)s %(name)s[%(levelname)s]: %(message)s')

info = logger.info
debug = logger.debug
warning = logger.warning
error = logger.error
critical = logger.critical

def init(level, filename):
    if level > 5 or level < 1:
        raise ValueError('日志级别必须在1-5之间.')

    logger.setLevel(LOG_LEVELS[ level-1 ])
    
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(FORMAT)

    fh = logging.FileHandler(filename)
    fh.setFormatter(FORMAT)

    logger.addHandler(sh)
    logger.addHandler(fh)

def main():
    import sys
    
    init(int(sys.argv[1]),  sys.argv[2])
    info('info...')
    debug('debug')
    warning('warnging...')
    critical('critical..')
    error('error...')

if __name__ == '__main__':
    main()
