from odoo import fields, models

class PdfDocumentDataInherit(models.Model):
    _inherit = 'pdf.document.data'
    
    state = fields.Selection(selection_add=[('a','A')], ondelete={'a':'cascade'})