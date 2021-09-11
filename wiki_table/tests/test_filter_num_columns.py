import unittest
from wiki_table.filter_num_columns import filter_num_columns
from wiki_table.column import Column

class TestFilterNumColumns(unittest.TestCase):
    def test_not_number(self):
        content = [
            'Alfa Romeo Racing Orlen',
            'Scuderia AlphaTauri Honda',
            'Alpine F1 Team[11]',
            'Aston Martin Cognizant F1 Team[14]',
            'Scuderia Ferrari Mission Winnow[c]',
            'Uralkali Haas F1 Team[20]',
            'McLaren F1 Team',
            'Mercedes-AMG Petronas F1 Team',
            'Red Bull Racing Honda',
            'Williams Racing']
        columns = [Column('Entrant', content)]
        columns = filter_num_columns(columns)
        self.assertEqual(columns, [])

    def test_number_with_weird_postfix(self):
        content = [
            '1.46 m (4 ft 9+1⁄2 in)',
            '1.485 m (4 ft 10+1⁄2 in)',
            '1.485 m (4 ft 10+1⁄2 in)',
            '1.524 m (5 ft 0 in)',
            '1.552 m (5 ft 1+1⁄8 in)',
            '1.58 m (5 ft 2+1⁄4 in)',
            '1.58 m (5 ft 2+1⁄4 in)',
            '1.595 m (5 ft 2+3⁄4 in)',
            '1.605 m (5 ft 3+1⁄4 in)',
            '1.62 m (5 ft 3+3⁄4 in)',
            '1.65 m (5 ft 5 in)',
            '1.65 m (5 ft 5 in)',
            '1.66 m (5 ft 5+3⁄8 in)',
            '1.66 m (5 ft 5+3⁄8 in)']
        columns = [Column('Height', content)]
        columns = filter_num_columns(columns)
        content_num = [1.46, 1.485, 1.485, 1.524, 1.552, 1.58, 1.58, 
                        1.595, 1.605, 1.62, 1.65, 1.65, 1.66, 1.66]
        self.assertEqual(columns, Column('Height', content_num))

    def test_date(self):
        content = [
            '20 May 1922',
            '26 May 1923',
            '6 August 1923',
            '11 July 1925',
            '2 August 1926',
            '6 September 1926',
            '3 July 1928',
            '5 August 1928',
            '18 August 1929',
            '12 June 1932',
            '7 August 1932',
            '7 August 1932',
            '29 May 1939',
            '29 March 1941']
        columns = [Column('Height', content)]
        columns = filter_num_columns(columns)
        self.assertEqual(columns, [])

    def test_time(self):
        content = ['4:20']
        columns = [Column('time', content)]
        columns = filter_num_columns(columns)
        self.assertEqual(columns, [])

    def test_normal_number(self):
        content = ['7', '.88', '99', '10', '22', '14', '31', '5', '18', '16', '55', '9', '47', '3']
        columns = [Column('No.', content)]
        columns_after = filter_num_columns(columns)
        self.assertEqual(columns, columns_after)
