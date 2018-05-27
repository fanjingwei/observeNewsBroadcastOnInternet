import unittest
from observe import *

class ObserveTest(unittest.TestCase):
	def testHotWord(self):
		string = observeSina("区块链",5)
		with open("区块链.sina",'w') as f:
			f.write(string)

if __name__ == '__main__':
	unittest.main()