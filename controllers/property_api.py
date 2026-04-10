import json
from odoo import http
from odoo.http import request


class PropertyApi(http.Controller):

    # --------CREATE Operation-----------
    @http.route("/v1/property", methods=["POST"],type="http", auth="none", csrf=False)
    def post_endpoint(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get("name"):
            return request.make_json_response("Name is required!", status=400)

        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message":"Property Created Successfully",
                    "id": res.id,
                    "name": res.name,
                }, status=201)

        except Exception as error:
            return request.make_json_response({
                "message":error
            }, status=400)

        # @http.route("/v1/property/json", methods=["POST"], type="http", auth="none", csrf=False)
        # def post_endpoint(self):
        #     args = request.httprequest.data.decode()
        #     vals = json.loads(args)
        #     print(vals)
        #     if vals:
        #         return request.make_json_response("Property displayed Successfully", status=200)





    # ------- UPDATE operation ------------
    @http.route("/v1/property/<int:property_id>", methods=["PUT"],type="http", auth="none", csrf=False)
    def put_endpoint(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({"message":"Property Not Found!"}, status=404)

            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)

            return request.make_json_response({
                "message":"Property Updated Successfully",

            }, status=200)

        except Exception as error:
            return request.make_json_response({
                "message":error
            }, status=400)


    # --------READ Operation-----------
    @http.route("/v1/property/<int:property_id>", methods=["GET"],type="http", auth="none", csrf=False)
    def read_endpoint(self, property_id):
            try:
                property_id = request.env['property'].sudo().search([('id', '=', property_id)])
                if not property_id:
                    return request.make_json_response({"message":"Property Not Found!"}, status=404)

                return request.make_json_response({
                    "id":property_id.id,
                    "name":property_id.name,
                    "ref": property_id.ref,
                    "description":property_id.description,
                    "postcode":property_id.postcode,
                    "date_availability":property_id.date_availability,
                    "expected_selling_date":property_id.expected_selling_date,
                    "is_late":property_id.is_late,
                    "expected_price":property_id.expected_price,
                    "selling_price":property_id.selling_price,
                    "diff":property_id.diff,
                    "bedrooms":property_id.bedrooms,
                    "living_area":property_id.living_area,
                    "garage":property_id.garage,
                    "garden_orientation":property_id.garden_orientation,
                    "owner_id":property_id.owner_id.name,
                    "owner_address":property_id.owner_address
                }, status=200)


            except Exception as error:
                return request.make_json_response({
                    "message":error
                }, status=400)








