from odoo import http

class TestApi(http.Controller):

    @http.route("/api/test", methods=["GET"],  type="http", auth="public", csrf=False)
    def test_endpoint(self):
        return "inside test endpoint method"