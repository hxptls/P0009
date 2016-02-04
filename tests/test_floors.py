from unittest import TestCase

from src import btbbc


class TestFloors(TestCase):
    def test_idontwanttothinkofthenameofthis(self):
        x1 = btbbc.Floors('http://tieba.baidu.com/p/4260990232')
        self.assertEqual(x1.valuable(), True)
        x2 = x1.get_floors()
        self.assertGreaterEqual(len(x2), 94)  # Feb 3, 2016
        self.assertEqual(x2[3].floor_index, 5)
        self.assertEqual(x2[93].floor_index, 130)  # Feb 3, 2016

    def test_hhhhhh(self):
        x1 = btbbc.Post('http://tieba.baidu.com/p/4260990232')
        x1.match()
        for rf in x1.real_floors:
            print(str(rf[0].floor_index) + ' FLOOR!')
            print(rf[0].content)
            print('Floor in floor!')
            if rf[1] is None:
                continue
            for c in rf[1].comments:
                print('#' + c.content)
                print('')

    def test_hhHH(self):
        x1 = btbbc.Post('http://tieba.baidu.com/p/4260990232')
        x1.match()
        x1.migration()
        x2 = x1.get_real_floors()
        for f in x2:
            print(str(f['floor'].floor_index) + ' FLOOR')
            print(f['floor'].content)
            if f['comments'] is not None:
                print('\tCOMMENTS')
                for c in f['comments']:
                    print('\t# ' + c.content)
