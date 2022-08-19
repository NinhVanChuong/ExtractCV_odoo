from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ApplicantJob(models.Model):
    _inherit = 'hr.job'
             
    def extract_wizard(self):
        return self.env.ref('viin_extract_cv.extract_cv_wizard_action').sudo().read()[0]
    
    