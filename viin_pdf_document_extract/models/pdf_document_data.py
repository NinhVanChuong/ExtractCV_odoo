from odoo import models, fields

class PdfDocumentData(models.Model):
    _name = 'pdf.document.data' #Têh bảng trong cơ sở dữ liệu phải theo quy chuẩn . ở giữa
    _description = 'PDF Document Data' #Tên không theo quy chuẩn của model
    # _auto = True #có lưu bảng vào trong database hay không
    # _table = 'table_anh' #đặt tên cho table phải đặt tên có _
    # _rec_name = 'pdf_id' #chọn trường hiển thị thay cho trường name
    #_inherit = '' #string hoặc list( string) cho phép kế thừa đến một model khác 
    #_inherits = '' #string hoặc list( string) cho phép kế thừa đến một model khác theo kiểu uỷ thác
    #_sql_constraints = [(name,'sql_def',message)] tạo ra điều kiện ràng buộc sql
    # _order = 'pdf_id' #chỉ định trường được sắp xếp mặc định đối với kết quả lấy từ database - số trc rồi chữ hoa sau đó là chữ thg
    ''' Trường Selection đóng gói một lựa chọn duy nhất
        Tham số selection nhận vào list các tuple, tham số selection_add nhận vào list các tuple để ghi đè - mở rộng selection
        Đối với các bản ghi tham chiếu đến trường selection_add, cung cấp 1 cơ chế dự phòng đối với trường bị ghi đè và tham
        chiếu với selection_add là ondelete với các lựa chọn: set null, cascade, set default
'''
    state = fields.Selection(string='Status', selection=[('new_employee', 'New Employee'), ('inter', 'Inter'), ('employee','Employee')], copy=True)
    
    pdf_id = fields.Many2one('pdf.document', string='PDF Document', help='Help Document PDF')
    pdf_data = fields.Float(digits=(12,3))
    # pdf_data = fields.Text(string='Text Data', default='No Text',
    #                         states={'new_employee': [('invisible', False),('readonly', False),
    #                                                  ('required',True)],
    #                         'inter': [('invisible', True), ('readonly', False), ('required', False)], 
    #                         'employee': [('invisible', False), ('readonly', True), ('required', False)]})
    #invisible Có ẩn trường này trên view hay không , readonly chỉ đọc trên giao diện
    #phân quyền trường sử dụng thuộc tính groups trong fields
    
    #pdf_file = fields.Binary(attachment=True)# quy định có lưu trong bảng ir.attachment hay không, nếu Flase thì lưu trong bảng hiện tạ
    # html = fields.Html(string='HTML')# được dùng để đóng gói nội dung mã html
    
    '''Trường Montery đóng gói một Float được biểu thị bằng một loại tiền tệ res_currency nhất định
    Độ chính xác thập phân và ký hiệu tiền tệ được lấy từ thuộc tính currency_field, mặc định currency_field là currency_id
    là trường Many2one liên kết với bảng res.currency trong base của odoo'''
    # currency_id = fields.Many2one('res.currency', string='Currency')
    # class_fund = fields.Monetary(string='Class Fund', currency_field='currency_id')
    
    
    
    
    