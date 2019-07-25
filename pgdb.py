import os, psycopg2

class PGDB:
    
    def __init__(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        self.conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        self.mycursor = self.conn.cursor()
    
    def get_data(self, query):
        self.mycursor.execute(query)
        return self.mycursor.fetchall()
        
    def execute_query_val(self, query, val):
        self.mycursor.execute(query, val)
        self.conn.commit()
        
    def create_msg(self, user_id, msg):
        query="SELECT MAX(msg_id) FROM message"
        self.mycursor.execute(query)
        res = self.mycursor.fetchall()
        if(res[0][0] is None):
            msg_id = 1
        else:
            msg_id = res[0][0]+1
            
        val = (msg_id, msg, user_id)
        
        query = """INSERT INTO message(msg_id, msg_content, usr_id) 
                    VALUES(%s, %s, %s)"""
        
        self.mycursor.execute(query, val)
        self.conn.commit()