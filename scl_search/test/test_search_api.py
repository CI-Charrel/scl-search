
from scl_search.search_utility import SEARCH
from configurations.filedb_trans import FileDBManager
import unittest

class TestSearchAPI(unittest.TestCase):

    instance = SEARCH()
    db = FileDBManager()

    def test_aa_setup(self):
        retTF = self.instance.setup()
        self.assertEqual(retTF, True)


    def test_bb_index_mainfolder(self):
        retTF = self.instance.index_mainfolder()
        self.assertEqual(retTF, True)


    def test_cc_getindexdocument(self):
        retTF = self.instance.getindexdocument()
        self.assertEqual(retTF, True)


    def test_dd_autocompletion(self):
        retLT = self.instance.autocompletion("bandicam")
        isgd = False
        if len(retLT) > 0:
            isgd = True

        self.assertEqual(isgd, True)


    def test_ee_fulltextsearch(self):
        retDT = self.instance.fulltextsearch("bandicam")
        isgd = False
        if len(retDT) > 0:
            isgd = True
        self.assertEqual(isgd, True)

