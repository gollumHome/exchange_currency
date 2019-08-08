# coding: utf-8


class AtoSubmit:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        pass

    def __exit__(self, exc_typ, exc_val, tb):
        if exc_typ:
            self.db.session.rollback()
        else:
            self.db.session.commit()

