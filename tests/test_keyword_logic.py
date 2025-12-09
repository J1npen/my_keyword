from src.my_keyword.keyword_logic import map_keyword_id_name, map_site_id_name

def test_map_keyword_id_name_normal():
    assert map_keyword_id_name('1') == 'Yummy'

def test_map_keyword_id_name_empty():
    assert map_keyword_id_name('') == False

def test_map_keyword_id_name_out():
    assert map_keyword_id_name('9999') == False

def test_map_site_id_name_normal():
    assert map_site_id_name('1') == 'telegram' or 'Telegram'

def test_map_site_id_name_empty():
    assert map_site_id_name('') == False

def test_map_site_id_name_out():
    assert map_site_id_name('9999') == False