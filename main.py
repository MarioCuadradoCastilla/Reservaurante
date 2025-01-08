from Views import Inicio
from Controllers import DataBaseController
db = DataBaseController()

if __name__ == '__main__':

    db.create_tables_if_not_exists()
    try:
        Inicio.main(db)
    finally:
        db.close_connection()

