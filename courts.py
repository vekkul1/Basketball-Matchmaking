import db

def init():
    data = [(1, 'Uimastadionin koripallokenttä', 'Hammarskjöldintie 5, 00250 Helsinki'), (2, 'Merisataman koripallokenttä', 'Merikatu 29, 00150 Helsinki'), (3, 'Hermannin koripallokenttä', 'Hämeentie 105, 00550 Helsinki'), (4, 'Pikkukosken koripallokenttä', 'Pikkukoskentie 23, 00650 Helsinki'), (5, 'Namika Areena', 'Pilkekuja 10, 00660 Helsinki'), (6, 'Kasinonrannan koripallokenttä', 'Särkiniementie, 00200 Helsinki'), (7, 'Pihlajamäen koripallokenttä', 'Lucina Hagmanin polku 5, 00710 Helsinki'), (8, 'Pukinmäen koripallokenttä', 'Kenttätie 8, 00720 Helsinki'), (9, 'Puistolan koripallokenttä', 'Koudantie 2, 00760 Helsinki'), (10, 'Kannelmäen koripallokenttä', 'Soittajanpolku 9, 00420 Helsinki'), (11, 'Pakilan rantatien koripallokenttä', 'Pakilan rantatie 2, 00680 Helsinki'), (12, 'Puotilan koripallokenttä', 'Puotilan Metrokatu 2, 00900 Helsinki')]
    sql = """
        INSERT INTO locations (name, address)
        VALUES (?, ?)
    """
    for i in data:
        db.execute(sql, [i[1], i[2]])

def get_courts():
    sql = """SELECT id, name, address
            FROM locations"""
    return db.query(sql)