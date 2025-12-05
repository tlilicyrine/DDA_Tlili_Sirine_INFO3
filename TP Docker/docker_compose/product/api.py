from flask import Flask
from flask_restful import Api, Resource

#Initialisation de l'application
app = Flask(__name__)
api = Api(app)

class Product(Resource):
    def get(self):
        return {
            'products':['Ipad pro 14', 'Iphone 13', 'Ordinateur bureautique']
        }

#Definition d'une route
api.add_resource(Product, '/')

#Execution de l'appilcation
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)