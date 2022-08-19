from odoo import models, fields
from odoo.tools.image import image_to_base64
from ..wizard.extract_cv_wizard import detector
from pdf2image import convert_from_path
from odoo.exceptions import ValidationError
import os
import cv2
from PIL import Image
from datetime import datetime
from dateutil.parser import parse

# detector = MugDetection()

class Applicant(models.Model):
    
    _inherit = "hr.applicant"
    
    def create_new_employee_from_cv(self, attachment):
        """ Create employee from applicant"""
        dicts={}
        face = None
        url = attachment._filestore() + '/'+attachment.store_fname
        images = convert_from_path(url,dpi=500,poppler_path=r'/opt/homebrew/Cellar/poppler/22.06.0_2/bin')
        for i in range(len(images)):
            images[i].save(f'CV'+ str(i) +'.jpg','JPEG')
            dict,face1 = detector.convert_to_record(f'CV'+ str(i) +'.jpg')
            dicts.update(dict)
            os.remove(f'CV'+ str(i) +'.jpg')
            if type(face1) != type(None):
                face = face1
                
        if type(face) != type(None):
            cv2.imwrite('face.png',face)
            with Image.open(os.path.join('./', 'face.png'), 'r') as img:
                        base64_img = image_to_base64(img, 'PNG')
            os.remove('face.png')
        else:
            base64_img = ''
            
        gender = dicts.get('gener')
        gender = gender.lower()
        if gender == 'nam' or gender =='male':
            gender = 'male'
        else:
            gender = 'female'
        
        str_birthday = dicts.get('dob')
        # dt_birthday = datetime.strptime(str_birthday, '%d/%m/%Y')
        dt_birthday = parse(str_birthday)
        birthday = fields.Date.to_string(dt_birthday)
          
        employee_data = {'default_image_1920': base64_img,
                         'default_gender': gender,
                         'default_birthday': birthday,}
        return employee_data
        
    def create_employee_from_applicant(self):
        res = super(Applicant,self).create_employee_from_applicant()
        attachment = self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', self.id)])
        if (len(attachment) > 0):
            res['context'].update(self.create_new_employee_from_cv(attachment))
        return res
                