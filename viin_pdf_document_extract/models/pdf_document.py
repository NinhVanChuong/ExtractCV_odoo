from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PdfDocument(models.Model):
    _name = 'pdf.document'
    _description = 'PDF Document File'

    name = fields.Char(string='PDF File Name', required=True, default="pdf")
    pdf_file = fields.Binary(string='PDF File')
    data_ids = fields.One2many('pdf.document.data', 'pdf_id', string='PDF Document Data')
    note = fields.Text(string='Note', compute='_compute_note')
    onchange_test = fields.Text(string='Onchange')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    constraints_test = fields.Text(string="Constraints SQL")
    
    @api.depends('data_ids.pdf_data')
    def _compute_note(self):
        for record in self:
            record.note = record.data_ids[:1].pdf_data
    
    @api.onchange('name')
    def _onchange_note(self):
        if self.name:
            self.onchange_test=self.name.upper()
            
    @api.constrains('start_date','end_date')
    def check_date(self):
        mess = _('The start_day bigger end_day')
        if self.filtered(lambda r: r.start_date and r.end_date and r.start_date>r.end_date):
            raise ValidationError(mess)
        
    _sql_constraints=[('name_constrains','unique(name,constraints_test)',"name not unique")]