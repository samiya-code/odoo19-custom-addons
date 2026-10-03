from odoo import api, fields, models


class Asset(models.Model):
    _name = 'oh.asset'
    _description = 'Company Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Asset Name',
        required=True,
        tracking=True,
    )

    asset_code = fields.Char(
        string='Asset Code',
        required=True,
        copy=False,
        readonly=True,
        default='New',
        tracking=True,
    )

    category_id = fields.Many2one(
        'oh.asset.category',
        string='Category',
        required=True,
        tracking=True,
    )

    serial_number = fields.Char(
        string='Serial Number',
        tracking=True,
    )

    state = fields.Selection(
        [
            ('available', 'Available'),
            ('assigned', 'Assigned'),
            ('maintenance', 'Under Maintenance'),
            ('retired', 'Retired'),
        ],
        string='Status',
        default='available',
        required=True,
        tracking=True,
    )

    assigned_to = fields.Many2one(
        'res.users',
        string='Assigned To',
        tracking=True,
    )

    location = fields.Char(
        string='Location',
        tracking=True,
    )

    purchase_date = fields.Date(
        string='Purchase Date',
    )

    purchase_price = fields.Float(
        string='Purchase Price',
    )

    description = fields.Text(
        string='Description',
    )

    notes = fields.Text(
        string='Internal Notes',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )

    assignment_count = fields.Integer(
        string='Assignments',
        compute='_compute_assignment_count',
    )

    _sql_constraints = [
        (
            'asset_code_unique',
            'unique(asset_code)',
            'Asset Code must be unique.',
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('asset_code', 'New') == 'New':
                vals['asset_code'] = self.env[
                    'ir.sequence'
                ].next_by_code('oh.asset') or 'New'

        return super().create(vals_list)

    def _compute_assignment_count(self):
        Assignment = self.env['oh.asset.assignment']

        for asset in self:
            asset.assignment_count = Assignment.search_count([
                ('asset_id', '=', asset.id)
            ])

    @api.onchange('assigned_to')
    def _onchange_assigned_to(self):
        for asset in self:
            if asset.assigned_to:
                asset.state = 'assigned'
            elif asset.state == 'assigned':
                asset.state = 'available'