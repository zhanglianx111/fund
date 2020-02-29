# !/usr/bin/python
# -*- coding:utf-8 -*-

import toml
import logging
import rank_avg

config = toml.load('config.toml')


logger = logging.getLogger("main")
logger.setLevel(level = config['log']['level'])

handler = logging.FileHandler("log.txt")
handler.setLevel(config['log']['level'])
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(config['log']['level'])
console.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(console)


if __name__ == '__main__':
	rank_avg.run()


	