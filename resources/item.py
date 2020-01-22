
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity
)

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This fields is required!'
    )

    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Every Item must have a store id'
    )

    @jwt_required
    def get(self, name):

        item = ItemModel.find_item_by_name(name)
        if item:
            # return {'item': {'name': item[0], 'price': item[1]}}, 200
            return item.json()
        return {'message': 'item not found'}, 404

    def post(self, name):

        if ItemModel.find_item_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()

        # item = {'name': name, 'price': data['price']}

        # **data = data['price'], data['store_id']
        item = ItemModel(name, **data)
        try:
            # ItemModel.add_Item(item)
            item.save_to_db()
        except:
            return {'message': 'Error While Adding item'}, 500
        # print(item.json())
        return item.json(), 201
        # return {'message': 'item added successfully'}, 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilages required'}, 401

        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'item deleted successfully'}

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)
        # updated_item = {'name': name, 'price': data['price']}

        if item is None:
            item = ItemModel(name, **data)
            # try:
            #    #  ItemModel.add_Item(updated_item)
            #      updated_item.add_Item()

            # except:
            #     return {"message": "Error while adding an Item"}, 500
        else:
            item.price = data['price']
            # try:
            # ItemModel.update_item(updated_item)
            # updated_item.update_item()

            # except:
            #     return {"message": "Error while updating an Item"}, 500
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        # use find_all instead of query.all()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200  # 200 is default return status

        return {'items': [item['name'] for item in items],
                'message': 'More Data Available if you login'
                }, 200
        # return {'items': [item.json() for item in ItemModel.query.all()]}, 200
        # another solution using map()
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}, 200

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM item"

        # result = cursor.execute(query)

        # items = []
        # for row in result:
        #     # print(row)
        #     items.append({'name': row[0], 'price': row[1]})

        # return (
        #     {'items': items}
        # ), 200
