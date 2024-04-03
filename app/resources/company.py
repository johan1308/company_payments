from django.db import connections
import datetime
from django.db import transaction
from rest_framework import status
from app.resources.base import BaseResource

class CompanyResource(BaseResource):

    def statistics(
        self,
        since: str = str(datetime.date.today()),
        until: str = str(datetime.date.today()),
        company: int = None,
        bank: int=None,
        payment_method: int = None
    ):
        with connections['default'].cursor() as cursor:
            query = f"""SELECT 
                    c.name as commpany,
                    YEAR(date) as year,
                    MONTH(date) as month,
                    pm.name as payment_method,
                    b.name as bank,
                    COUNT(pc.id) as quantity,
                    SUM(pc.amount) as total
                FROM payments_company pc
                INNER JOIN banks b ON b.id=pc.bank_origin_id
                INNER JOIN payment_methods pm on pm.id=pc.method_id
                INNER JOIN companies c on c.id=pc.company_id
                WHERE DATE(pc.date) >='{since}' 
                AND DATE(pc.date) <='{until}' 
                """

            if company:
                query+= f" AND pc.company_id = {company}"

            if bank:
                query+= f" AND pc.bank_origin_id = {bank}"

            if payment_method:
                query+= f" AND pc.method_id = {payment_method}"
        
            query += " GROUP by c.name, YEAR(date), MONTH(date), pm.name, b.name"

            cursor.execute(query)
            data = self.dictfetchall(cursor)

        return data

