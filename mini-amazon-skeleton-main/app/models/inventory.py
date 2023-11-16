from flask import current_app as app

class InventoryItem:
    def __init__(self, id, sid, pid, quantity, product_name):
        self.id = id
        self.sid = sid
        self.pid = pid
        self.quantity = quantity
        self.product_name = product_name

#     @staticmethod
#     def get(id):
#         rows = app.db.execute('''
# SELECT id, sid, pid, quantity
# FROM Inventory
# WHERE id = :id
# ''',
#                               id=id)
#         return InventoryItem(*(rows[0])) if rows else None

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
    def add_new_item(sid, pid, quantity):
        # adding new product id to inventory
        try:
            rows = app.db.execute("""
INSERT INTO Inventory(sid, pid, quantity)
VALUES(:sid, :pid, :quantity)
""",
                                  sid=sid,
                                  pid=pid,
                                  quantity = quantity)
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def get_qty(sid, pid):
        try:
            rows = app.db.execute("""
SELECT quantity
FROM Inventory
WHERE sid = :sid
AND pid = :pid
""",
                                  sid=sid,
                                  pid=pid)
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None
             
    @staticmethod
    def update_quantity(sid, pid, quantity):
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
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def delete_item(sid, pid):
        try:
            rows = app.db.execute("""
DELETE FROM Inventory
WHERE sid = :sid
AND pid = :pid
""",
                                  sid=sid,
                                  pid=pid)
            return rows if rows else None
        except Exception as e:
            print(str(e))
            return None
        
        
    @staticmethod
    def update_inventory(sid, pid, quantity):
        # get quantity of existing product in seller's inventory
        qty = InventoryItem.get_qty(sid, pid)
        if len(qty) == 0: 
            # pid not currently in sid's inventory
            rows = InventoryItem.add_new_item(sid, pid, quantity)
        elif (quantity + qty[0][0] <= 0):
            rows = InventoryItem.delete_item(sid, pid)
        else: 
            # update quantity of existing pid
            new_quantity = quantity + qty[0][0]
            rows = InventoryItem.update_quantity(sid, pid, new_quantity)
        return rows if rows else None