from odoo import api, fields, models


class AssetAssignment(models.Model):
    _name = 'oh.asset.assignment'
    _description = 'Asset Assignment'
    _order = 'assignment_date desc'

    asset_id = fields.Many2one(
        'oh.asset',
        string='Asset',
        required=True,
        ondelete='cascade',
    )

    assigned_to = fields.Many2one(
        'res.users',
        string='Assigned To',
        required=True,
    )

    assignment_date = fields.Date(
        string='Assignment Date',
        required=True,
        default=fields.Date.context_today,
    )

    return_date = fields.Date(
        string='Return Date',
    )

    location = fields.Char(
        string='Location',
    )

    notes = fields.Text(
        string='Notes',
    )

    state = fields.Selection(
        [
            ('active', 'Active'),
            ('returned', 'Returned'),
        ],
        string='Status',
        default='active',
        required=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for record in records:
            record.asset_id.write({
                'assigned_to': record.assigned_to.id,
                'state': 'assigned',
                'location': record.location,
            })

        return records

    def action_return(self):
        for record in self:
            record.write({
                'state': 'returned',
                'return_date': fields.Date.context_today(self),
            })

            record.asset_id.write({
                'assigned_to': False,
                'state': 'available',
            })