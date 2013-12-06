# -*- coding: UTF-8 -*-
import os
import types


def do_commit(obj, action="add"):
    from genuine_ap.database import db

    if action == "add":
        if isinstance(obj, types.ListType) or \
           isinstance(obj, types.TupleType):
            db.session.add_all(obj)
        else:
            db.session.add(obj)
    elif action == "delete":
        db.session.delete(obj)
    db.session.commit()
    return obj


def as_dict(fields, d):
    items = []
    for field in fields:
        if isinstance(field, types.StringType):
            items.append((field, d.get(field)))
        elif isinstance(field, types.TupleType):
            items.append((field[0], d.get(field[1])))
    return dict(items)

_d = None


def find_model(table_name):
    global _d
    if _d is None:
        _d = {}
        from genuine_ap import models
        for model in models.__dict__.values():
            if hasattr(model, '_sa_class_manager'):
                _d[model.__tablename__] = model
    return _d[table_name]


def assert_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdirs(dir_path)
