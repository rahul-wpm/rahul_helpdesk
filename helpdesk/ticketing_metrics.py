__author__ = 'Rahul.R'
import traceback
import datetime
from utils.db_utils import connect_db


class Reports(object):
    """
    @summary : This class generates reports relates to the Help Desk tickets.
    """

    def __init__(self):
        """
        @summary: Constructor
        @return: None
        """
        self.db = connect_db()

    def display_metrics(self, result_dict_list):
        """
        @summary : This method is used for displaying the headers and the values
                   of the query result
        @param result_dict_list: This is result dict after querying
        @return: None
        """
        if result_dict_list:
            header_string = ''
            for per_record in result_dict_list:
                for header in per_record.keys():
                    header_string += "\t%s" % str(header.upper())
                break
            print(header_string)
            for per_record in result_dict_list:
                value_string = ''
                for header, value in per_record.iteritems():
                    if header == 'avg_time':
                        value = str(datetime.timedelta(seconds=int(value)))
                    value_string += "\t\t%s" % str(value)
                print("%s\n" % str(value_string))
        return

    def average_first_reply(self):
        """
        @summary : This gives the average response time between all the tickets
                    moving from New to Open
        @return: None
        """
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
                for header, value in per_month.iteritems():
                    if header == 'avg_response_time':
                        value = str(datetime.timedelta(seconds=int(value)))
                    value_string += "\t%s" % str(value)
                print("%s\n" % str(value_string))

        first_resp_year = """SELECT asignee_id,extract(YEAR FROM
        opened_date) AS year, avg(time_to_sec(timediff(opened_date,
        created_date))) AS avg_response_time FROM  \
        HelpDesk_Ticket WHERE opened_date IS NOT NULL GROUP BY month,
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
                for header, value in per_year.iteritems():
                    if header == 'avg_response_time':
                        value = str(datetime.timedelta(seconds=int(value)))
                    value_string1 += "\t%s" % str(value)
                print("%s\n" % str(value_string1))
        return

    def average_reponse_time(self):
        """
        @summary : Average Response time of Customer /Staff while ticket
                   status is in OPEN
        @return: None
        """
        cursor = self.db.cursor()
        average_response_time = """SELECT tmp.ticket_id as ticket_id,\
        AVG(time_to_sec(tmp.result)) as avg_time FROM \
        (SELECT T.ticket_id, T.history_id, T.created_date, \
        IFNULL(timediff(T.created_date,(select MAX(TT.created_date) FROM\
        HelpDesk_Ticket_History TT WHERE TT.created_date < T.created_date \
        and TT.ticket_id = T.ticket_id and TT.status in ('OPEN') )),0) as result \
        FROM HelpDesk_Ticket_History T where T.status in ('OPEN') \
        order by T.ticket_id, T.history_id) tmp GROUP BY tmp.ticket_id"""

        cursor.execute(average_response_time)
        avg_response_open = cursor.fetchall()
        self.display_metrics(avg_response_open)
        return

    def ticket_lifetime(self):
        """
        @summary : This method gives the Minimum / Maximum and Average Lifetime
                    of a ticket from New to Closed.
        @return: None
        """
        cursor = self.db.cursor()
        min_ticket_lifetime = """select ticket_id,\
                time_to_sec(timediff(closed_date,created_date))\
                time_taken from HelpDesk_Ticket where closed_date is not null\
                order by time_taken limit 1"""
        cursor.execute(min_ticket_lifetime)
        min_time_result = cursor.fetchone()
        if min_time_result:
            min_value = str(datetime.timedelta(seconds=int(
                min_time_result['time_taken'])))
            print("\n\t Minimum Life Time taken by a ticket : '%s'" % str(
                min_value))

        max_ticket_lifetime = """select ticket_id,\
                time_to_sec(timediff(closed_date,created_date))\
                time_taken from HelpDesk_Ticket where closed_date is not null\
                order by time_taken desc limit 1"""
        cursor.execute(max_ticket_lifetime)
        max_time_result = cursor.fetchone()
        if max_time_result:
            max_value = str(datetime.timedelta(seconds=int(
                max_time_result['time_taken'])))
            print("\n\tMaximum Life Time taken by a ticket : '%s'" % str(
                max_value))

        avg_ticket_lifetime = """ select ticket_id,\
            avg(time_to_sec(timediff(closed_date,created_date))) time_taken\
            from HelpDesk_Ticket where closed_date is not null"""
        cursor.execute(avg_ticket_lifetime)
        avg_time_result = cursor.fetchone()
        if avg_time_result['time_taken']:
            avg_value = str(datetime.timedelta(seconds=int(
                avg_time_result['time_taken'])))
            print("\n\tAverage Life Time taken by a ticket : '%s'" % str(
                avg_value))
        return

    def staff_performance(self):
        """
        @summary : This lists Staff Performance  based on the average
                    completion time of all the tickets by the staff
        @return: None
        """
        cursor = self.db.cursor()
        staff_performance_qry = """select staff_id,\
        avg(time_to_sec(timediff(completed_date,assigned_date))) avg_time FROM\
        HelpDesk_Staff_TicketHistory where completed_date is not null group by \
        staff_id order by avg_time"""
        cursor.execute(staff_performance_qry)
        staff_performance_result = cursor.fetchall()
        self.display_metrics(staff_performance_result)
        return


if __name__ == '__main__':
    """
    @summary : Main Method
    @:return : None
    """
    try:
        rep_obj = Reports()
        print("\n \t Average First Response Per Month and Per Year \n")
        rep_obj.average_first_reply()
        print("\n \t Average Response time of Customer/Staff for Open tickets "
              "\n")
        rep_obj.average_reponse_time()
        print("\n \tMin / Max /Avg life time of tickets  \n")
        rep_obj.ticket_lifetime()
        print("\n \t Staff Performance Report on Avg time taken for Solving "
              "Ticket "
              "\n")
        rep_obj.staff_performance()
    except Exception:
        print(traceback.format_exc())


