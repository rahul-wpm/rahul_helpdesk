__author__ = 'Rahul.R'
import traceback
import datetime
from utils.db_utils import connect_db
class Reports(object):
    """
    """
    def __init__(self):
        self.db = connect_db()
    def average_first_reply(self):
        cursor = self.db.cursor()
        first_resp__month = """select extract(MONTH from opened_date) as\
        month, extract(YEAR from opened_date) as year, \
        avg(time_to_sec(timediff(opened_date,created_date))) as
        avg_response_time from  \
        HelpDesk_Ticket where opened_date is not null group by month,year"""
        cursor.execute(first_resp__month)
        avg_response_month = cursor.fetchall()
        if avg_response_month:
            header_string = ''
            for per_month in avg_response_month:
                for header in per_month.keys():
                    header_string += "\t%s" % str(header.upper())
                break
            print(header_string)
            for per_month in avg_response_month:
                value_string = ''
                for header,value in per_month.iteritems():
                    if header=='avg_response_time':
                        value=str(datetime.timedelta(seconds=int(value)))
                    value_string += "\t%s" % str(value)
                print("%s\n"%str(value_string))

        first_resp_year = """select asignee_id,extract(YEAR from
        opened_date) as year, avg(time_to_sec(timediff(opened_date,
        created_date))) from  \
        HelpDesk_Ticket where opened_date is not null group by month,
        asignee_id"""

        cursor.execute(first_resp__month)
        avg_response_year = cursor.fetchall()
        if avg_response_year:
            header_string1 = ''
            for per_year in avg_response_year:
                for header in per_year.keys():
                    header_string1 += "\t%s" % str(header.upper())
                break
            print(header_string1)
            for per_year in avg_response_year:
                value_string1 = ''
                for header,value in per_year.iteritems():
                    if header=='avg_response_time':
                        value=str(datetime.timedelta(seconds=int(value)))
                    value_string1 += "\t%s" % str(value)
                print("%s\n"%str(value_string1))
        return

if __name__=='__main__':
    try:
        rep_obj=Reports()
        rep_obj.average_first_reply()
        
    except Exception:
        print(traceback.format_exc())








"""SELECT IFNULL(TIMESTAMPDIFF(SECOND, created_date, opened_date) / NULLIF(COUNT(*) - 1, 0), 0)
FROM HelpDesk_Ticket where opened_date is not NULL"""

#Grouping average response time using month
"""SELECT opened_date.MONTH, IFNULL(TIMESTAMPDIFF(SECOND, created_date,
opened_date) / NULLIF(COUNT(*) - 1, 0), 0)
FROM HelpDesk_Ticket where opened_date is not NULL group by opened_date.MONTH"""

#Grouping average response time using year
"""SELECT opened_date.MONTH, IFNULL(TIMESTAMPDIFF(SECOND, created_date,
opened_date) / NULLIF(COUNT(*) - 1, 0), 0)
FROM HelpDesk_Ticket where opened_date is not NULL group by opened_date.MONTH"""


