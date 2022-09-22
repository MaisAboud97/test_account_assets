from odoo import models, fields, api


class AradosEmp(models.Model):
    
    _inherit = 'hr.employee'
    _description = 'Add Citizenship to employees'
 

    def _compute_field(self):
       
        list1 = []
        msg = []
        for rec in self:
            fields = self.env['arados.hr.standards'].search([],limit=1)
            field  = fields.field_ids
            if fields and field:
                for record in field:
                    field_type = record.ttype
                    mini = rec.mapped(record.name)
                    if field_type=='many2one' or field_type=='one2many' or field_type=='many2many':
                        list1.append(mini.id)
                        if mini.id ==False:
                            msg.append(record.field_description)
                    else :
                        list1.append(mini[0])
                        if mini[0] ==False or mini[0] ==0:
                            msg.append(record.field_description)
                    if False in list1 or  0 in list1:
                        state = 'canceled'
                        rec.msg=msg
                        rec.state=state
                    else:
                        state = 'confirmed'
                        rec.msg=msg
                        rec.state=state
            else:
                    rec.msg=' '
                    rec.state =False

    
    def write(self,vals):
        result = super(AradosEmp, self).write(vals)
        list1 = []
        msg = []
        for rec in self:
            fields = self.env['arados.hr.standards'].search([],limit=1)
            field  = fields.field_ids
            for record in field:
                field_type = record.ttype
                mini = rec.mapped(record.name)
                if field_type=='many2one' or field_type=='one2many' or field_type=='many2many':
                    list1.append(mini.id)
                    if mini.id ==False:
                        msg.append(record.field_description)
                else :
                    list1.append(mini[0])
                    if mini[0] ==False or mini[0] ==0:
                        msg.append(record.field_description)
                if False in list1 or  0 in list1:
                    state = 'canceled'
                    vals.update({'msg': msg})
                    vals.update({'state': state})
                    result = super(AradosEmp, self).write(vals)
                else:
                        vals.update({'msg': msg})
                        state = 'confirmed'
                        vals.update({'state': state})
                        result = super(AradosEmp, self).write(vals)
        return result
    
    
    state=fields.Selection([('confirmed','confirmed'),('canceled','canceled')],compute="_compute_field", store=True)
    msg = fields.Char(compute="_compute_field")
    color_of_face = fields.Char(string='Face Color')
    color_of_eyes = fields.Char(string='Eyes Color')
    specail_marks = fields.Char(string='Specail Marks')
    delivery_date = fields.Date(string='Delivery Date')
    honesty = fields.Char(string='Honesty')
    constraint = fields.Char(string='Constraint')    
    card_number = fields.Integer(string='Crad Number')
    first_name = fields.Char(string='name' ,required=False )
    father_name = fields.Char(string='Father name' ,required=False)
    nickname = fields.Char(string=' Nickname',required=False)
    mother_name = fields.Char(string='Mother name and her Nickname')
    
    
    @api.model
    def create(self,vals):
        vals['first_name']= vals.get('first_name')
        vals['father_name']= vals.get('father_name')
        vals['nickname']= vals.get('nickname')
        vals['name']=vals['first_name'] +" "+vals['father_name']+" "+vals['nickname']
        res= super(AradosEmp, self).create(vals)
        return res 
        
    
