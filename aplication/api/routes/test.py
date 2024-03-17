from aplication.api.middlewares import middleware
from flask import request, jsonify, render_template,make_response
from infrastructure.exceptions import ApiError
import re,json
class TestRoutes:
    def __init__(self, app):
        self.app = app
        
        @self.app.route('/test', methods=['GET'])
        def test():
            return jsonify({"test":"Without Middleware"}),200