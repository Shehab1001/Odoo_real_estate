from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo import fields


class TestProperty(TransactionCase):

    def setUp(self):
        super().setUp()

        self.Property = self.env['property']

        self.property_01_record = self.Property.create({
            'ref': 'new',
            'name': 'Property 01',
            'description': 'Property 1000 description',
            'postcode': '1010',
            'expected_price': 100000.0,
            'selling_price': 120000.0,
            'bedrooms': 3,
        })

    def test_property_create(self):
        """Test record creation"""
        self.assertTrue(self.property_01_record.id)
        self.assertEqual(self.property_01_record.name, 'Property 01')
        self.assertEqual(self.property_01_record.postcode, '1010')
        self.assertEqual(self.property_01_record.description, 'Property 1000 description')

    def test_compute_diff(self):
        """Test computed field diff = selling_price - expected_price"""
        self.assertEqual(self.property_01_record.diff, 20000.0)

    def test_bedrooms_constraint(self):
        """bedrooms = 0 should raise ValidationError"""
        with self.assertRaises(ValidationError):
            self.Property.create({
                'ref': 'new',
                'name': 'Property 02',
                'postcode': '2020',
                'bedrooms': 0,
            })

    def test_check_expected_selling_date_late(self):
        """If expected selling date is in the past, is_late should become True"""
        self.property_01_record.expected_selling_date = fields.Date.today().replace(day=1)
        # safer version if today may already be first day:
        if self.property_01_record.expected_selling_date >= fields.Date.today():
            self.property_01_record.expected_selling_date = fields.Date.subtract(fields.Date.today(), days=1)

        self.property_01_record.check_expected_selling_date()
        self.assertTrue(self.property_01_record.is_late)

    def test_check_expected_selling_date_not_late(self):
        """If expected selling date is today or in future, is_late should become False"""
        future_date = fields.Date.add(fields.Date.today(), days=5)
        self.property_01_record.expected_selling_date = future_date

        self.property_01_record.check_expected_selling_date()
        self.assertFalse(self.property_01_record.is_late)

    def test_set_to_pending(self):
        """Test state change to pending"""
        self.property_01_record.set_to_pending()
        self.assertEqual(self.property_01_record.state, 'pending')

    def test_set_to_sold(self):
        """Test state change to sold"""
        self.property_01_record.set_to_sold()
        self.assertEqual(self.property_01_record.state, 'sold')

    def test_set_to_draft(self):
        """Test state change to draft"""
        self.property_01_record.set_to_pending()
        self.property_01_record.set_to_draft()
        self.assertEqual(self.property_01_record.state, 'draft')

    def test_action_closed(self):
        """Test state change to closed"""
        self.property_01_record.action_closed()
        self.assertEqual(self.property_01_record.state, 'closed')

    def test_onchange_expected_price_negative(self):
        """Test onchange warning when expected price is negative"""
        new_property = self.Property.new({
            'name': 'Property 03',
            'postcode': '3030',
            'expected_price': -5000,
            'bedrooms': 2,
        })

        result = new_property._onchange_price()
        self.assertTrue(result)
        self.assertIn('warning', result)
        self.assertEqual(
            result['warning']['message'],
            'Expected Price Must not be Negative Number'
        )