from odoo import fields, models


class AssetCategory(models.Model):
    _name = 'oh.asset.category'
    _description = 'Asset Category'
    _order = 'name'

    name = fields.Char(
        string='Category Name',
        required=True,
    )

    description = fields.Text(
        string='Description',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
    )

    asset_count = fields.Integer(
        string='Assets',
        compute='_compute_asset_count',
    )

    def _compute_asset_count(self):
        Asset = self.env['oh.asset']

        for category in self:
            category.asset_count = Asset.search_count([
                ('category_id', '=', category.id)
            ])