from odoo import models, fields

class ActiveReport(models.Model):
    _name = 'pdf.document.active.report'
    _description = 'PDF Document Analysis'
    # _auto = False #không tạo bảng dưới cơ sở dữ liệu
    _rec_name = 'date_start' # hiển thị trường id thay cho trường name
    
    date_start = fields.Date('Start Date')
    date_closed = fields.Date('Closed Date')
    pdf_document_id = fields.Many2one('pdf.document', 'Document PDF')
    
    
    