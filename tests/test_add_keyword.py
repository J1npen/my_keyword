import unittest
from unittest.mock import MagicMock, call, patch

from src.my_keyword.keyword_logic import add_keyword


class AddKeywordTests(unittest.TestCase):
    @patch('src.my_keyword.keyword_logic.query_site')
    @patch('src.my_keyword.keyword_logic.connect_database')
    def test_add_keyword_without_name(self, mock_connect_database, mock_query_site):
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect_database.return_value = mock_conn

        with patch('builtins.input', side_effect=['   ']), patch('builtins.print') as mock_print:
            add_keyword()

        mock_print.assert_any_call('未添加数据！')
        mock_query_site.assert_not_called()
        mock_cursor.execute.assert_not_called()
        mock_conn.commit.assert_not_called()

    @patch('src.my_keyword.keyword_logic.query_site')
    @patch('src.my_keyword.keyword_logic.connect_database')
    def test_add_keyword_with_new_site(self, mock_connect_database, mock_query_site):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'id': 10}]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect_database.return_value = mock_conn

        inputs = [
            'new keyword',   # keyword_name
            'NewSite',       # site name (non-numeric)
            'https://example.com',  # site url
            '5',             # rating
            '',              # image_path => None
            'some remark',   # remark
        ]

        with patch('builtins.input', side_effect=inputs):
            add_keyword()

        expected_calls = [
            call('\nINSERT site(site_name, url)\nVALUE\n(%s,%s)\n', ('NewSite', 'https://example.com')),
            call('SELECT id FROM site WHERE site_name = %s', 'NewSite'),
            call('\nINSERT keyword(keyword_name, site_id, rating, image_path, remark)\nVALUE\n(%s,%s,%s,%s,%s)\n', (
                'new keyword', 10, '5', None, 'some remark'
            )),
        ]
        self.assertEqual(mock_cursor.execute.call_args_list, expected_calls)
        mock_conn.commit.assert_called_once()
        mock_query_site.assert_called_once()


if __name__ == '__main__':
    unittest.main()
