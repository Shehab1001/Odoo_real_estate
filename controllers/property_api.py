import json
from signal import valid_signals

from odoo import http
from odoo.http import request
class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"],type="http", auth="none", csrf=False)
    def post_endpoint(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        print(res)
        if res:
            return request.make_json_response("Property Created Successfully", status=200)