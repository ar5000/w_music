#----------------------------------------------------------------------------#
# DB CRUD for Instrument Model
#----------------------------------------------------------------------------#
# [READ]
# def show_all(cursor):
#     cursor.execute("SELECT * FROM instruments;")
#     pass

# def show_one(cursor, field):
#     cursor.execute("SELECT * FROM instruments WHERE ref_num=?", field)
#     pass

# # [CREATE]
# def add_one(cursor, fields):
#     # ref, name, category, url
#     cursor.execute("INSERT INTO instruments VALUES (?,?,?,?)", fields)
#     pass
# [UPDATE]
def update_one(cursor, fields):
    cursor.execute('''UPDATE instruments 
    SET name=?, 
        category=?, 
        image=?
    WHERE ref_num=?''', fields)
    pass
# [DELETE]
def delete_one(cursor, field):
    cursor.execute('''DELETE FROM instruments
    WHERE ref_num=?''', field)
    pass