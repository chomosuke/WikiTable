import unittest
from tests.real_world_wiki_page import f1_2021, woman_high_jump
from html_to_columns import html_to_columns

class TestHtmlToColumns(unittest.TestCase):
    def test_woman_high_jump(self):
        columns = html_to_columns(woman_high_jump)
        self.assertEqual(len(columns), 4)
        self.assertEqual(columns[0].name, 'Height')
        self.assertEqual(columns[0].content[0], '1.46 m (4 ft 9+1⁄2 in)')
        self.assertEqual(columns[1].name, 'Athlete')
        self.assertEqual(columns[1].content[0], 'Nancy Voorhees (USA)')
        self.assertEqual(columns[2].name, 'Date')
        self.assertEqual(columns[2].content[0], '20 May 1922')
        self.assertEqual(columns[3].name, 'Place')
        self.assertEqual(columns[3].content[0], 'Simsbury[1]')
        for column in columns:
            self.assertEqual(len(column.content), 56)

    def test_f1_2021(self):
        columns = html_to_columns(f1_2021)
        # will not include th that are 'clearly index'
        # but will include th at some other row

        self.assertEqual(len(columns), 83)
        self.assertEqual(columns[0].name, 'Entrant')
        self.assertEqual(columns[4].name, 'No.')
        self.assertEqual(len(columns[4].content), 21)
        self.assertEqual(columns[4].content[0], '7')
        self.assertEqual(len(columns[5].content), 21)
        self.assertEqual(columns[5].content[0], 'Kimi Räikkönen[b]')

        # test missing data removed
        self.assertEqual(len(columns[15].content), 13)

        # also test successfully excluded footer or not
        self.assertEqual(len(columns[54].content), 21)
        self.assertEqual(columns[54].content[0], '224.5')

        # columns[57] (Constructor) has content with colspan 2,
        # this must be delt with correctly.
        self.assertEqual(columns[58].content[1], '3F')

        # to test if successfully excluded footer or not.
        self.assertEqual(len(columns[0].content), 10)

        # to test if multi-column empty cell is mistakely taken as footer
        self.assertEqual(len(columns[20].content), 2)
