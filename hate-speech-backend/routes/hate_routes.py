from flask import Blueprint, request, jsonify, current_app

from controllers.hate_controller import HateController

hate_bp = Blueprint('hate', __name__)
hate_controller = HateController()

@hate_bp.route('/hate', methods=['POST'])
def hate_build():
    return hate_controller.hate_build()