from odoo import models, fields, api

class EmpStandards(models.Model):
    _name = 'arados.hr.standards'
    _description = 'hr.standards'



    name = fields.Char()
    model_id = fields.Many2one(string='Model',comodel_name='ir.model',domain=[('model','=','hr.employee')])
    field_ids =  fields.Many2many('ir.model.fields')

    
    def write(self,values):
        res = super(EmpStandards, self).write(values)
        fields = self.env['ir.model.fields'].search([('id','in',self.field_ids.ids)])
        employee = self.env['hr.employee'].search([])
        for emp in employee:
            msg =[]
            list1=[]
            for rec in fields:
                field_name = rec.name
                field_type = rec.ttype
                mini = emp.mapped(field_name)
                if field_type=='many2one' or field_type=='one2many' or field_type=='many2many':
                    list1.append(mini.id)
                    if mini.id ==False:
                        msg.append(rec.field_description)
                else :
                    list1.append(mini[0])
                    if mini[0] ==False or mini[0] ==0:
                        msg.append(rec.field_description)
                if False in list1:
                    emp.state='canceled'
                else:
                    emp.state='confirmed'
        return res
