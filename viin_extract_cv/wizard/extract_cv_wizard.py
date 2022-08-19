from odoo import models, fields
from .tool.deloy import MugDetection
from pdf2image import convert_from_path
from odoo.exceptions import ValidationError
import os


detector = MugDetection()

class EtractCV(models.TransientModel):
    
    _name = 'extract.cv.wizard'
    _description = 'Extract CV Wizard'
    pdf_file = fields.Binary(string='File for upload')
    
    def extract(self):
        self.env.cr.execute("select * from ir_attachment where res_model='%s' AND res_id=%s" % (self._name, self.id))
        # attachment = self.env['ir.attachment'].search([('res_id','=',r_id)])
        attachment = self.env.cr.dictfetchone()
        if attachment is None:
            raise ValidationError('CV chưa được truyền vào')
        else:
            dicts={}
            attachment = self.env['ir.attachment'].browse(attachment['id'])
            url = attachment._filestore() + '/'+attachment.store_fname
            images = convert_from_path(url,dpi=500,poppler_path=r'/opt/homebrew/Cellar/poppler/22.06.0_2/bin')
            for i in range(len(images)):
                images[i].save(f'CV'+ str(i) +'.jpg','JPEG')
                dict,face = detector.convert_to_record(f'CV'+ str(i) +'.jpg')
                dicts.update(dict)
                os.remove(f'CV'+ str(i) +'.jpg')
            try:
                applicant = self.env['hr.applicant'].create({
                    'name': dicts.get('name'),
                    'partner_name': dicts.get('name'),
                    'email_from': dicts.get('email'),
                    'partner_phone': dicts.get('phone'),
                    'stage_id': self.env.ref('hr_recruitment.stage_job1').id,
                    'job_id': self._context.get('active_id')
                    })
                attachment.write({
                    'res_id': applicant.id,
                    'res_model': applicant._name,
                    'res_field': False,
                    })
            except:
                raise ValidationError('Loại CV Chưa được hỗ trợ')
                