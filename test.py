import unittest
import pandas as pd


class MockAccountTest(unittest.TestCase):

    def test_DF_Maker(self):
        period = 20
        weight = 5
        columns = ['u_{0}_{1}'.format(period, weight)]
        df = pd.DataFrame(columns=columns)

        self.assertEqual(df.columns, 'u_20_5')

    def test_list(self):
        list1 = [1, 2, 3, 4]
        self.assertEqual(sum(list), 10)


if __name__ == '__main__':
    unittest.main()
