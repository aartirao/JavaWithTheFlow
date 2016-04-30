import pymysql.cursors
import traceback
import operator
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('db.cfg')

connection = pymysql.connect(host=config.get('database','host'),
                             user=config.get('database','username'),
                             password=config.get('database','password'),
                             db = config.get('database','db'),
                             charset = 'utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



def getTags():
    tags = set()
    i = 1
    with connection.cursor() as cursor:
        query = "SELECT DISTINCT(Tags) FROM Posts"
        cursor.execute(query)
        posts = cursor.fetchall()
        for row in posts:            
            if row[u'Tags'] != None and row[u'Tags'] != "":
                s = row[u'Tags'][1:-1]
                a = s.split("><")
                tags = tags | set(a)                
            print i
            i = i + 1
    return tags

def putTags(tags):
    i = 1
    with connection.cursor() as cursor:
        for tag in list(tags):            
            query = "INSERT INTO Tags(TagName) values (%s)"
            cursor.execute(query, (tag))
            connection.commit()
            print "ins" + str(i) 
            i = i + 1
            
            
def getTagFrequency(userId):
    i = 1
    result = {}
    with connection.cursor() as cursor:
       
        query2 = "select TopicId, Weight from UserInterests where UserId = %s order by Weight desc Limit 5"
        cursor.execute(query2, (userId))
        Interests = cursor.fetchall()
        query3 = "SELECT Distinct(Tags) as Tags from Posts where Id in (SELECT PT.PostId from Topics as T join PostTopicMap as PT on \
                PT.TopicId = T.Id where T.Id = %s or T.Id = %s or T.Id = %s or T.Id = %s or T.Id = %s)"
        cursor.execute(query3, (Interests[0][u'TopicId'], Interests[1][u'TopicId'], Interests[2][u'TopicId'], \
                Interests[3][u'TopicId'], Interests[4][u'TopicId']))
        Posts = cursor.fetchall()
        
        for post in Posts:
            if post[u'Tags'] != None and post[u'Tags'] != "":
                s = post[u'Tags'][1:-1]
                a = s.split("><")
                for each in a:
                    if each in result.keys():
                        result[each] = result[each] + 1
                    else:
                        result[each] = 1
            #print i
            i = i + 1
        resultlist = sorted(result.items(), key=operator.itemgetter(1))
        resultlist.reverse()
        print resultlist[:100]
        res = {}
        res["name"] = "words"
        children = []
        for (each, val) in resultlist:
            children.append({"name":each, "size": val})
        res["children"] = children
        return res
             
            

if __name__ == "__main__":
    # tags = getTags()   
    # putTags(tags)
    getTagFrequency("821742")        
        