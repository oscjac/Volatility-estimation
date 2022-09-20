import unittest
from .ticker import API, Ticker

exists_false = True

class TickerFunctions(unittest.TestCase):
    def setUp(self) -> None:
        self.api = API()
        self.ibm = Ticker(self.api, "IBM")
        self.ibm.save_full()
        return super().setUp()
    
    @unittest.skipIf(exists_false, "Saving api calls")
    def test_ticker_does_not_exist(self):
        self.assertFalse(Ticker(self.api, "INXR").exists())

    @unittest.skipIf(exists_false, "Saving api calls")
    def test_exists(self):
        self.assertTrue(Ticker(self.api, "CCL").exists())
        
    @unittest.skipIf(exists_false, "Saving api calls")
    def test_no_name(self):
        self.assertFalse(Ticker(self.api, "").exists())
    
    @unittest.skipIf(exists_false, "Saving api calls")
    def test_many_matches(self):
        self.assertFalse(Ticker(self.api, "AXA").exists())
    
    @unittest.skipIf(exists_false, "Saving api calls")
    def test_best_matched(self):
        self.assertTrue(Ticker(self.api, "AA").exists())

    def test_single_get_price(self):
        output = self.ibm.get_prices(1)
        self.assertEqual(output[0][0], "2022-09-16")
        self.assertEqual(output[0][1], "127.2700")

if __name__=='__main__':
    unittest.main()