import pymysql.cursors
import datetime
import json
import traceback
import ConfigParser
import random
config = ConfigParser.ConfigParser()
config.read('db.cfg')


connection = pymysql.connect(host=config.get('database','host'),
							 user=config.get('database','username'),
							 password=config.get('database','password'),
							 db = config.get('database','db'),
							 charset = 'utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

try:
        with connection.cursor() as cursor:
            sql=""" select PostId,EventId,sum(Duration) from UserEventStore where EventId=2 group by PostId """
            cursor.execute(sql)
            dur = cursor.fetchall()
            #sumOfDuration=dur["sum('Duration')"]
            #post_id_iterator=dur["PostId"]
        with connection.cursor() as cursor:
            sql=""" select PostId,count(EventId) from UserEventStore where EventId = 3 group by PostId """
            cursor.execute(sql)
            count_act = cursor.fetchall()
            #SelectTextScore  =count_act["count('EventId')"]
        with connection.cursor() as cursor:
            sql=""" select PostId, sum(Rating) from UserRatingsScore group by PostId """
            cursor.execute(sql)
            rating = cursor.fetchall()
            #user_rating =rating["sum('Rating')"]
        with connection.cursor() as cursor:
            sql=""" select Id , ViewCount from Posts  group by Id """
            cursor.execute(sql)
            clicks = cursor.fetchall()
            #click_count=count_act["viewcount"]
          
            for a in clicks:
                user_rating = 0;
                SelectTextScore = 0;
                sumOfDuration = 0 ;
                for b in rating:
                    if(a['Id']==b['PostId']):
                       user_rating = b['sum(Rating)']
                       print (user_rating)
                       break

                for c in count_act:
                    if(a['Id']==c['PostId']):
                       SelectTextScore = c['count(EventId)']
                       print (user_rating)
                       break
                for d in dur:
                    if(a['Id']==d['PostId']):
                       sumOfDuration = d['sum(Duration)']
                       print (user_rating)
                       break

                TimeScore= 2 ** ((sumOfDuration+1)/5)


                if(a['ViewCount'] == None):
                    a['ViewCount'] = 0
                    randomNumber=random.randint(10,300)
                    usefulness = (((a['ViewCount']) * 1 )+ (sumOfDuration * 2) + (SelectTextScore * 3) ) + user_rating + randomNumber
                else:
                    usefulness = (((a['ViewCount']) * 1 )+ (sumOfDuration * 2) + (SelectTextScore * 3) ) + user_rating + randomNumber

                with connection.cursor() as cursor:
                 sql = """UPDATE `Posts` SET
                 `usefulness` = %s   WHERE Id = %s"""
                 cursor.execute(sql, (usefulness,a['Id']))
                print(a['Id'])
                usefulness=0
                connection.commit()

finally:
   connection.close()