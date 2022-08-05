from odoo import models,fields

class PdfDocmuentEx(models.TransientModel):
    _name = "pdf.document.ex"
    _description = "PDF Document Ex"
    
    data_infor = fields.Many2one('pdf.document', string="Data infor")
    
    def action_pdf(self):
        print(self.env['pdf.document.data'].search([('pdf_id','!=',False)]))