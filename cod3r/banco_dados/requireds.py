def has_connector():
    try:
        from mysql.connector import connector
    except ModuleNotFoundError:
        print('MySQL Conector not found')
    else:
        print('MySQL connector ready')
