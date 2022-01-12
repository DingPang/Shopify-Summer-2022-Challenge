def get_first(cursor):
    result = None
    for e in cursor:
        result = e
        break
    return result

GET_STORAGES_LAST_ID = '''
    SELECT MAX(S_Id)
    FROM Storages;
'''
GET_ITEM_LAST_ID = '''
    SELECT MAX(Part_Id)
    FROM Parts
    WHERE S_Id = %s;
'''


REMOVE_ONE_STORAGE = '''
    DELETE FROM Storages
    WHERE S_Id = %s
    RETURNING *;
'''

REMOVE_ONE_ITEM = '''
    DELETE FROM Parts
    WHERE Part_Id = %s AND S_Id = %s
    RETURNING *;
'''

EDIT_STORAGE = '''
    UPDATE Storages
    SET Name = %s, Street1 = %s, Street2 = %s, City = %s, State = %s, ZIP = %s
    WHERE S_Id = %s
    RETURNING *;
'''

EDIT_ITEM = '''
    UPDATE Parts
    SET Name = %s, Stock = %s
    WHERE S_Id = %s AND Part_Id = %s
    RETURNING *;
'''

INSERT_ADDRESS = '''
    INSERT INTO Storages (S_Id, Name, Street1, Street2, City, State, ZIP) VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING *;
'''

INSERT_ITEM = '''
    INSERT INTO Parts(S_Id, Part_Id, Name, Stock) VALUES (%s, %s, %s, %s)
    RETURNING *;
'''

GET_ALL_STORAGES = '''
    SELECT S_Id, Name, Street1, Street2, City, State, ZIP
    FROM Storages S
    ORODER BY S_Id;
'''

GET_ONE_STORAGE = '''
    SELECT Part_Id, Name, Stock
    FROM Parts P
    WHERE P.S_Id = %s
    ORODER BY Part_Id;
'''

GET_ALL = '''
    SELECT S.S_Id, S.Name, S.Street1, S.Street2, S.City, S.State, S.ZIP, P.Part_Id, P.Name, P.Stock
    FROM Parts P
    JOIN Storages S
    ON P.S_Id = S.S_Id
    O;
'''

##################




