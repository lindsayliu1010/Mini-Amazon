from flask import current_app as app

class InventoryItem:
    def __init__(self, id, sid, pid, quantity, product_name):
        self.id = id
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.product_name = product_name

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, sid, pid, quantity
FROM Inventory
WHERE id = :id
''',
                              id=id)
        return InventoryItem(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_sid(sid):
        rows = app.db.execute('''
SELECT Inventory.id, sid, pid, quantity, Products.name
FROM Inventory, Products
WHERE sid = :sid 
AND Inventory.pid = Products.id
''',
                              sid=sid)
        return [InventoryItem(*row) for row in rows]

    @staticmethod
    def add_item(sid, pid, quantity):
        # adding new product to inventory
        try:
            rows = app.db.execute("""
INSERT INTO Inventory(sid, pid, quantity)
VALUES(:sid, :pid, :quantity)
RETURNING id
""",
                                  sid=sid,
                                  pid=pid,
                                  quantity = quantity)
            id = rows[0][0]
            return InventoryItem.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def get_quantity(sid, pid):
        # get quantity of existing product in seller's inventory
        try:
            rows = app.db.execute("""
SELECT quantity
FROM Inventory
WHERE sid = :sid
AND pid = :pid
""",
                                  sid=sid,
                                  pid=pid)
            #id = rows[0][0]
            quantity = rows[3]
            #return InventoryItem.get(id).quantity
            return quantity
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None
    
    @staticmethod
    def update_item(sid, pid, quantity):
        # updating quantity of existing product in inventory
        try:
            rows = app.db.execute("""
UPDATE Inventory
SET quantity = :quantity
WHERE sid = :sid
AND pid = :pid
""",
                                  sid=sid,
                                  pid=pid,
                                  quantity = quantity)
            id = rows[0][0]
            return InventoryItem.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None