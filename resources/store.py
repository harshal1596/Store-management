import uuid
from flask import request
from db import db
from models import StoreModel
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @jwt_required
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        # In case of pagination please refer below code
        # page = request.args.get("page", 1, type=int)
        # per_page = request.args.get("per_page", 5, type=int)
        # offset = (page-1)*per_page
        # store = StoreModel.query.offset(offset).limit(per_page).all()       Method-1
        # or
        # store = StoreModel.query.paginate(page=page, per_page=per_page, error_out=False)      Method-2
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    @jwt_required
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"Message": "Store deleted"}

@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="AN error occurred while inserting data.")
        return store
