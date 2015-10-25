__author__ = 'Rahul.R'
import sys
import os
import re
import getpass
import base64
import traceback
import datetime
from Crypto.Cipher import AES
import MySQLdb
from MySQLdb.cursors import DictCursor
#For python 3.x use the following import(s) commented below
# from pip.backwardcompat import raw_input
#TODO Need to add docstrings in all methods
#TODO Need to add reporting metrics here or as sepearate script

class HelpDesk(object):
    """
    Class for Implementing Help Desk
    """

    def __init__(self):
        """
        :return:
        """
        print("Welcome to Help Desk")
        # self.secret_key="Tenmiles"
        self.padding_symbol = "X"
        # self.secret_key = 'my random secret'
        self.secret_key = 'Temiles is cool!'

        self.cipher = AES.new(self.secret_key, AES.MODE_ECB)

    def connect_db(self):
        """
        :return:
        """
        self.db = MySQLdb.connect(host="127.0.0.1", user="singlebox",
                                  passwd="global!23", db="test",
                                  cursorclass=MySQLdb.cursors.DictCursor)
        return self.db
    def encrypt_data(self, password):
        """
        :param password:
        :return:
        """
        aes_size = 32
        aes_encode_construct = lambda password: password + (aes_size - len(
            password) % aes_size) * self.padding_symbol

        aes_encode = lambda c, password: base64.b64encode(c.encrypt(
            aes_encode_construct(password)))
        encrypted_value = aes_encode(self.cipher, password)

        return encrypted_value

    def decrypt_data(self, password):
        """
        @summary:
        @param password:
        @return:
        """
        # import pdb;pdb.set_trace()
        aes_decode_func = lambda cipher, password: cipher.decrypt(
            base64.b64decode(password)).rstrip(self.padding_symbol)
        decrypted_value = aes_decode_func(self.cipher, password)
        return decrypted_value


    def assign_staff(self,ticket_id,current_time,conn):
        """
        @summary: This assigns a staff for a newly raised ticket by considering
                    the staff who has less number of tickets currently.
        @return:
        """
        # import pdb;pdb.set_trace()
        # db = self.connect_db()
        cursor = conn.cursor()
        fetch_query="""SELECT staff_id,number_of_tickets FROM HelpDesk_Staff order by\
                        number_of_tickets,updated_date"""
        cursor.execute(fetch_query)
        staff_list= list(cursor.fetchall())
        if staff_list:
            for per_staff in staff_list:
                print(per_staff)
                staff_id=per_staff['staff_id']
                insert_staff_histoy = """INSERT INTO HelpDesk_Staff_TicketHistory (staff_id,\
                ticket_id,assigned_date) VALUES ('%s','%s','%s')""" % (
                    str(staff_id), ticket_id, current_time)
                no_of_tickets = per_staff['number_of_tickets']+1
                cursor.execute(insert_staff_histoy)
                update_staff_table = """UPDATE HelpDesk_Staff\
                set number_of_tickets='%s',updated_date='%s' where
                staff_id='%s'""" % (no_of_tickets, current_time,staff_id)
                cursor.execute(update_staff_table)
                staff_details_query = """select id, firstname, lastname,\
                email_id from HelpDesk_User where id='%s'""" %(staff_id)
                cursor.execute(staff_details_query)
                staff_details=cursor.fetchone()
                name=staff_details['firstname']+' '+staff_details['lastname']
                email_id=str(staff_details['email_id'])
                print("Assigned Staff for this ticket is \n\t Name: %s \n\t "
                      "Email: %s" % (name,email_id))
                return staff_id
        else:
            print('No staffs currently assigned for this ticket')
        return

    def fetch_open_tickets(self,email_id,user_type):
        # import pdb;pdb.set_trace()
        if user_type == 'ADMIN':
            type = 'asignee_id'
        elif user_type == 'CUSTOMER':
            type = 'customer_id'
        db = self.connect_db()
        cursor = db.cursor()

        fetch_open_query = """SELECT ticket_id,customer_id,subject,\
                    status, asignee_id,created_date FROM HelpDesk_Ticket where\
                    %s='%s' and status in('NEW','OPEN')""" %(str(type),
                                                             str(email_id))
        cursor.execute(fetch_open_query)
        open_ticket_list = list(cursor.fetchall())
        return open_ticket_list

    def customer_portal(self,customer_id, email_id):
        """
        :param password:
        :return:
        """
        # import pdb;pdb.set_trace()
        option = raw_input("What do you want to do? \n\t 1.Raise a Ticket "
                           "\n\t 2.View Open Tickets \n\t 3. Add Followup to "
                           "an Open Ticket\n\t4.Logout \n\t Your Choice :")
        if option == '1':
            ticket_subject = raw_input("\nEnter subject:")
            ticket_content = raw_input("\nEnter Content:")
            db = self.connect_db()
            cursor = db.cursor()
            current_time=datetime.datetime.now()
            insert_ticket_details="""INSERT INTO HelpDesk_Ticket (customer_id,
                                     subject,content,status,created_date)
                                     VALUES(
                                     '%s','%s','%s','%s','%s')"""%(customer_id,
                                                            ticket_subject,
                                                            ticket_content,
                                                            'NEW',current_time)

            cursor.execute(insert_ticket_details)
            ticket_id=cursor.lastrowid

            print("\n\nInserted into database\n\n")
            assignee_id=self.assign_staff(ticket_id,current_time,db)
            if not assignee_id:
                assignee_id=''
            update_ticket_assignee="""UPDATE HelpDesk_Ticket set
            asignee_id='%s' where ticket_id='%s'""" %(assignee_id,ticket_id)
            cursor.execute(update_ticket_assignee)

            insert_ticket_history="""INSERT INTO HelpDesk_Ticket_History(
            ticket_id,customer_id,subject,content,asignee_id,status,
            content_update_by,created_date) VALUES ('%s','%s','%s','%s','%s',
            '%s','%s','%s') """ % (ticket_id, customer_id,
                                                  ticket_subject,
                                                  ticket_content,
                                                  assignee_id, 'NEW',
                                                  customer_id,current_time)
            cursor.execute(insert_ticket_history)
            db.commit()


        elif option == '2':
            current_time=datetime.datetime.now()

            # db = self.connect_db()
            # cursor = db.cursor()
            #
            # fetch_open_query = """SELECT ticket_id,subject,status,
            # asignee_id,created_date FROM HelpDesk_Tickets where asignee_id='%s'
            # and status in('NEW','OPEN')""" % str(email_id)
            # cursor.execute(fetch_open_query)
            # open_ticket_list = list(cursor.fetchall())
            open_ticket_list=self.fetch_open_tickets(email_id,'CUSTOMER')
            if open_ticket_list:
                for per_ticket in open_ticket_list:
                    print("\n")
                    for header,value in per_ticket.iteritems():
                        print("\t%s"%str(header.upper()))
                    break
                for ticket in open_ticket_list:
                    print("\n")
                    for header,value in per_ticket.iteritems():
                        print("\t%s"%str(value))
            else:
                print("\n\tNo Open Tickets\n\n")
                self.customer_portal(customer_id,email_id)
        elif option =='3':
            open_ticket_list=self.fetch_open_tickets(email_id,'CUSTOMER')
            if not open_ticket_list:
                print("\n\tNo Open Tickets\n\n")
                self.customer_portal(customer_id,email_id)
            current_time=datetime.datetime.now()
            db = self.connect_db()
            cursor = db.cursor()
            follow_up_ticket_id = raw_input("Enter Ticket ID :")
            check_valid_query="""SELECT * from HelpDesk_Ticket where
            ticket_id='%s' and customer_id='%s'""" % str(
                follow_up_ticket_id,customer_id)
            cursor.execute(check_valid_query)
            check_valid_ticket=cursor.fetchone()
            if check_valid_ticket:
                update_message=raw_input("Enter followup message content:")

                insert_qry="""INSERT INTO HelpDesk_Ticket_History(
                ticket_id,customer_id,subject,content,asignee_id,status,
                content_update_by,created_date) VALUES ('%s','%s','%s','%s','%s',
                '%s','%s','%s') """ % (check_valid_ticket['ticket_id'],
                                        check_valid_ticket['customer_id'],
                                        check_valid_ticket['subject'],
                                        update_message,
                                        check_valid_ticket['assignee_id'],
                                        check_valid_ticket['status'],
                                        check_valid_ticket['customer_id'],
                                        current_time)
                cursor.execute(insert_qry)
            else:
                print("\n\tInvalid Ticket ID given...\n")
            db.commit()
            self.customer_portal(customer_id,email_id)
        elif option == '4':
            # self.logout()
            sys.exit()

        else:
            print("Invalid option try again..\n\n")
            self.customer_portal(customer_id, email_id)

        return

    def admin_portal(self,asignee_id,email_id):
        """
        :param password:
        :return:
        """
        import pdb;pdb.set_trace()
        option = raw_input("\n\tWhat do you want to do? \n\t 1.View "
                           "Assigned/Open\
                           Tickets\n\t 2.Reply /Open Tickets\n\t 3.Close "
                           "Tickets\n\t\
                           4.View Ticket History\n\t 5.Logout\nYour choice: ")
        if option == '1':
            #View Open Tickets
            db = self.connect_db()
            cursor = db.cursor()

            fetch_open_query = """SELECT ticket_id,subject,status,
            asignee_id,created_date FROM HelpDesk_Ticket where
            asignee_id='%s' and status in('NEW','OPEN')""" % str(asignee_id)
            cursor.execute(fetch_open_query)
            open_ticket_list = list(cursor.fetchall())
            if open_ticket_list:
                header_string=''
                for per_ticket in open_ticket_list:
                    for header,value in per_ticket.iteritems():
                        header_string =header_string+"\t%s"%str(header.upper())
                    break
                print("%s\n"%str(header_string))
                for ticket in open_ticket_list:
                    value_string=''
                    for header,value in per_ticket.iteritems():
                        value_string=value_string+"\t%s"%str(value)
                    print("%s\n"%str(value_string))
                    self.admin_portal(asignee_id,email_id)
            else:
                print("\n\tNo Open Tickets\n\n")
                self.admin_portal(asignee_id,email_id)
        elif option == '2':
            #Open or followup with an open ticket
            db = self.connect_db()
            cursor = db.cursor()
            follow_up_ticket_id = raw_input("Enter Ticket ID :")
            check_valid_query="""SELECT * from HelpDesk_Ticket where
            ticket_id='%s' and asignee_id='%s'""" %  (str(
                follow_up_ticket_id),str(asignee_id))
            cursor.execute(check_valid_query)
            ticket_dict=cursor.fetchone()
            current_time=datetime.datetime.now()
            if ticket_dict:
                if ticket_dict['status'] == 'NEW':
                    update_query1="""UPDATE HelpDesk_Ticket SET \
                    status='OPEN',asignee_id='%s',opened_date='%s'  where
                    ticket_id='%s'""" %(asignee_id,current_time,
                                        follow_up_ticket_id)
                    cursor.execute(update_query1)
                    message=''
                    msg_flag=raw_input("\n\tDo you wish to add followup "
                                       "message? [Y/N] :")
                    if msg_flag.upper() == 'Y':
                        message=raw_input("\n\nEnter followup message : ")
                    if not message:
                        #Adding Default message
                        message = 'Your ticket has been taken up! We will ' \
                                  'reply with the solution soon! Thanks for ' \
                                  'your patience.'
                    insert_qry1="""INSERT INTO HelpDesk_Ticket_History (
                    ticket_id,customer_id,subject,content,status,asignee_id,
                    created_date,content_update_by) values('%s','%s','%s',
                    '%s',%s,'%s','%s','%s')""" % (follow_up_ticket_id,
                                                 ticket_dict['customer_id'],
                                                  ticket_dict['subject'],
                                                  message,'OPEN',
                                                  asignee_id,current_time,
                                                  asignee_id)
                    cursor.execute(insert_qry1)
                    db.commit()
                elif ticket_dict['status'] == 'OPEN':
                    message=''
                    message=raw_input("\n\nEnter followup message : ")
                    if not message:
                        print("Nothing to be updated")
                        self.admin_portal(self,asignee_id,email_id)
                    else:
                        current_time=datetime.datetime.now()
                        insert_qry1="""INSERT INTO HelpDesk_Ticket_History (
                        ticket_id,customer_id,subject,content,status,
                        asignee_id, created_date) values('%s','%s','%s',
                        '%s','%s','%s','%s')""" %(follow_up_ticket_id,
                                              ticket_dict['customer_id'],
                                              ticket_dict['subject'],
                                              message,'OPEN',asignee_id,
                                              current_time)
                        cursor.execute(insert_qry1)
                        db.commit()
                        print("Database updated successfully!!!")
            else:
                print("Invalid Ticket ID")


        elif option == '3':
            #Close an existing ticket
            db = self.connect_db()
            cursor = db.cursor()
            follow_up_ticket_id = raw_input("Enter Ticket ID :")
            check_valid_query="""SELECT * from HelpDesk_Ticket where
            ticket_id='%s' and asignee_id='%s'""" % (str(
                follow_up_ticket_id),str(asignee_id))
            cursor.execute(check_valid_query)
            ticket_dict=cursor.fetchone()
            current_time=datetime.datetime.now()
            if ticket_dict:
                message=''
                message=raw_input("\n\nEnter followup message : ")
                if not message:
                    print("Nothing to be updated")
                    self.admin_portal(self,asignee_id,email_id)
                else:
                    current_time=datetime.datetime.now()
                    update_query1="""UPDATE HelpDesk_Ticket SET \
                    status='CLOSED',asignee_id='%s',closed_date='%s'
                    where ticket_id='%s'""" %(asignee_id,current_time,
                                        follow_up_ticket_id)
                    cursor.execute(update_query1)
                    if ticket_dict['status'] == 'NEW':
                        insert_qry1="""INSERT INTO HelpDesk_Ticket_History (
                        ticket_id,customer_id,subject,content,status,
                        asignee_id, created_date) values('%s','%s','%s',
                        '%s','%s','%s','%s')""" %(follow_up_ticket_id,
                                              ticket_dict['customer_id'],
                                              ticket_dict['subject'],
                                              message,'OPEN',asignee_id,
                                              current_time)
                        cursor.execute(insert_qry1)
                    insert_qry2="""INSERT INTO HelpDesk_Ticket_History (
                        ticket_id,customer_id,subject,content,status,
                        asignee_id, created_date) values('%s','%s','%s',
                        '%s','%s','%s','%s')""" %(follow_up_ticket_id,
                                              ticket_dict['customer_id'],
                                              ticket_dict['subject'],
                                              message,'CLOSED',asignee_id,
                                              current_time)
                    cursor.execute(insert_qry2)
                    fetch_query1="""select * from HelpDesk_Staff where \
                                    staff_id ='%s'"""%str(asignee_id)
                    cursor.execute(fetch_query1)
                    staff_details=cursor.fetchone()
                    if staff_details:
                        no_of_tickets = staff_details['number_of_tickets']-1
                        if no_of_tickets >= 0:
                            update_staff_table = """UPDATE HelpDesk_Staff\
                            set number_of_tickets='%s',updated_date='%s'
                            where staff_id='%s'""" % (
                                no_of_tickets, current_time,asignee_id)
                            cursor.execute(update_staff_table)

                            insert_qry = """UPDATE
                            HelpDesk_Staff_TicketHistory SET
                            completed_date='%s' WHERE staff_id='%s' and
                            ticket_id='%s' """ % (current_time,
                            str(asignee_id), follow_up_ticket_id)
                            cursor.execute(insert_qry)
                    db.commit()
                    print("Database updated successfully!!!")
            else:
                print("Invalid Ticket ID")

        elif option == '4':
            #Show ticket history
            "Not implemented"
            db = self.connect_db()
            cursor = db.cursor()

            fetch_open_query = """SELECT ticket_id,status,subject,
            asignee_id,created_date,opened_date,closed_date FROM
            HelpDesk_Ticket where asignee_id='%s' """ % str(asignee_id)
            cursor.execute(fetch_open_query)
            open_ticket_list = list(cursor.fetchall())
            if open_ticket_list:
                header_string=''
                for per_ticket in open_ticket_list:
                    for header,value in per_ticket.iteritems():
                        header_string =header_string+"\t%s"%str(header.upper())
                    break
                print("%s\n"%str(header_string))
                for ticket in open_ticket_list:
                    value_string=''
                    for header,value in per_ticket.iteritems():
                        value_string=value_string+"\t%s"%str(value)
                    print("%s\n"%str(value_string))
                    self.admin_portal(asignee_id,email_id)
            else:
                print("\n\tNo Assigned tickets yet !!!\n\n")
                self.admin_portal(asignee_id,email_id)
        elif option == '5':
            # self.logout()
            sys.exit()
        else:
            print("\n\tInvalid Option try again...\n\n")
            self.admin_portal(asignee_id,email_id)
        return

    def login(self):
        """
        @summary :
        @param email_id:
        @param password:
        @return:
        """
        try:
            email_id = raw_input("Please Enter Your Email ID : ")
            my_password = getpass.getpass("Please Enter the Password  : ")
            # my_password = raw_input("Please Enter the Password  : ")
            db = self.connect_db()
            cursor = db.cursor()

            fetch_login_query = """SELECT id,user_type,firstname,lastname,
            email_id, password FROM HelpDesk_User where email_id='%s' """ % str(
                email_id)
            cursor.execute(fetch_login_query)
            cust_result = cursor.fetchone()

            if cust_result:
                decrypted_value = self.decrypt_data(cust_result['password'])
                if my_password == decrypted_value:
                    print("You have logged in as %s !!!"%str(
                                            cust_result['user_type']))
                    print("Welcome " + str(cust_result['firstname']) + " "+
                          str(cust_result['lastname']))
                    if cust_result['user_type'] == 'ADMIN':
                        self.admin_portal(cust_result['id'],
                                          cust_result['email_id'])
                    elif cust_result['user_type'] == 'CUSTOMER':
                        self.customer_portal(cust_result['id'],
                                             cust_result['email_id'])
                    else:
                        print('Unknown User type!!!')
                        sys.exit()
                else:
                    print('Invalid Password!!!')
                    sys.exit()
            else:
                print('Invalid Email ID Try Signing Up First!!!')
                signup_flag=raw_input('Do you want to sign up? Choose[Y/N]: ')
                if signup_flag.upper()=='Y':
                    self.customer_signup()
                else:
                    sys.exit()
        except Exception:
            print(traceback.format_exc())
            raise Exception


    def customer_signup(self):
        """
        """
        member_type = raw_input("\nAre you a  \n 1. CUSTOMER \n\t(OR) "
                                "\n 2. ADMIN\n Your Choice: ")
        if member_type == '1':
            user_type = 'CUSTOMER'
        elif member_type == '2':
            user_type = 'ADMIN'
        else:
            print('Invalid member type')
            sys.exit()

        email_id = raw_input("\nEnter Email ID : ")
        password = raw_input("\nEnter Password : ")
        first_name = raw_input("\nEnter First Name : ")
        last_name = raw_input("\nEnter Last Name : ")
        option = raw_input("\nChoose any of the options \n 1. SUBMIT \n 2.EDIT "
                           "\n 3. EXIT\n Your Choice: ")
        if option == '1':
            if email_id and password and first_name and last_name:
                db = self.connect_db()
                cursor = db.cursor()
                encrypted_password = self.encrypt_data(password)
                insert_customer = """INSERT INTO HelpDesk_User (user_type,
                firstname,lastname,email_id,password) values('%s','%s','%s',
                '%s','%s') """ % (user_type, first_name, last_name,
                                  email_id, encrypted_password)
                cursor.execute(insert_customer)
                user_id=cursor.lastrowid
                current_time=datetime.datetime.now()
                if user_type == 'ADMIN':
                    insert_customer = """INSERT INTO HelpDesk_Staff (
                    staff_id,updated_date)values ('%s','%s') """ % (user_id,
                                                                current_time)
                    cursor.execute(insert_customer)
                db.commit()
                print("Inserted into database")
                self.home_page()

        elif option == '2':
            print('\nRe-Enter the details...\n\n')
            self.customer_signup()
        elif option == '3':
            sys.exit()
        else:
            print('Incorrect option. Try again...')
            self.customer_signup()

        # self.()
        return

    def home_page(self):
        """
        :return:
        """
        print("Welcome - Home Page")
        option = raw_input("Enter any of the following option number: \n\t 1.\
                          Log In \n\t 2. Sign Up \n\t 3. Exit \n Your choice: ")
        if option == '1':
            self.login()
        elif option == '2':
            self.customer_signup()
        elif option == '3':
            sys.exit()
        return


if __name__ == '__main__':
    """
    Main Function
    """
    try:
        # import pdb
        # pdb.set_trace()
        helpdesk_obj = HelpDesk()
        option = helpdesk_obj.home_page()
    except SystemExit:
        print("THanks for visiting us!!!")
    except Exception as e:
        # print("There seems to")
        print(traceback.format_exc())



