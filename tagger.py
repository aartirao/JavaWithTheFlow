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
    tags = {}
    i = 1
    with connection.cursor() as cursor:
        query = "SELECT DISTINCT(P.Tags) as Tags, PT.TopicId as TopicId FROM Posts P join PostTopicMap PT on PT.PostId = P.Id"
        cursor.execute(query)
        posts = cursor.fetchall()
        for row in posts:            
            if row[u'Tags'] != None and row[u'Tags'] != "":
                s = row[u'Tags'][1:-1]
                a = s.split("><")
                for each in a:
                    tags[each] = row[u'TopicId']                            
            i = i + 1
    return tags

def putTags(tags):
    i = 1
    with connection.cursor() as cursor:
        for tag in list(tags):            
            query = "INSERT INTO Tags(TagName, TopicId) values (%s, %s)"
            cursor.execute(query, (tag, tags[tag]))
            connection.commit()
            i = i + 1
            
            
def getTagFrequency(userid):
    i = 1
    result = {}
    with connection.cursor() as cursor:
        query1 = "select TagName, TopicId from Tags"
        cursor.execute(query1)
        Tags = cursor.fetchall()
        
        tags = {}
        for tag in Tags:
            tags[tag[u'TagName']] = tag[u'TopicId']
        
        query2 = "select TopicId, Weight from UserInterests where UserId = %s order by Weight desc Limit 5"
        cursor.execute(query2, (userid))
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
            i = i + 1
        resultlist = sorted(result.items(), key=operator.itemgetter(1))
        resultlist.reverse()
        res = {}
        res["name"] = "words"
        children = []
        childs = {}
        
        for (each, val) in resultlist[:150]:
            if each != "java":                
                if tags[each] not in childs.keys():
                    childs[tags[each]] = [{"name":each, "size": val}]
                else:
                    childs[tags[each]] = childs[tags[each]] + [{"name":each, "size": val}]
        i = 0
        
        for each in childs.keys():                
            i += 1
            subchildren = []
            #for e in childs[each]:
            #    subchildren.append(e)
            children.append({"name": i, "children":childs[each]})                        
        res["children"] = children
        return res
             
            

if __name__ == "__main__":
    #tags = getTags()   
    #putTags(tags)
    print getTagFrequency("821742")        
        