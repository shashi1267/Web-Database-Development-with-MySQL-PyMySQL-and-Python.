#!"C:/Users/shash/AppData/Local/Programs/Python/Python310/python.exe"


import pymysql
import cgi
import cgitb
cgitb.enable()
import mysql.connector





#	solution for CSCI 4333 Spring 2022 HW #7.



cnx = pymysql.connect(user='root', 
                      password='',
                      host='localhost',
                      database='swim')
                              

cursor = cnx.cursor()

#	Create HTTP response header
print("Content-Type: text/html;charset=utf-8")
print()

#	Create a primitive HTML starter
print ('''<html>
<head></head>
<body>
''')

#	Get HTTP parameter
form = cgi.FieldStorage()
eid = form.getfirst('eid')

if eid is None:
    #	No HTTP parameter eid submitted: show all events
    print('<h3>Kinds of events in meets</h3>')

    query = '''


with t1 AS(
SELECT DISTINCT e.eventId,e.Title,COUNT(e.meetId) AS numMeets
FROM event AS e GROUP BY e.Title),
t2 AS(
SELECT distinct e.eventId,
GROUP_CONCAT(CONCAT('     <li><a href="?eid=',e.eventId,'">',m.title,' at ',v.name,'</a>','</li>\n') SEPARATOR '')as events	
FROM meet AS m INNER JOIN venue AS v 
		ON (m.venueId = v.venueId)
	INNER JOIN event AS e
		ON (e.meetId = m.meetId) group by e.title)

select distinct t1.eventId,t1.Title,t1.NumMeets,t2.events
from t1 inner join t2 on (t1.eventId=t2.eventId);
'''
    cursor.execute(query)
    
    for (eid,eTitle, numMeets, events ) in cursor:
            print(str(eTitle)  + ': in ' + str(numMeets)
              + ' meets.\n<ol>\n' + events +'</ol>\n')

   
    print('</body></html>')
    cursor.close()
    cnx.close()		
    quit()
	
if eid is not None:	#	This will always be satisfied at this point.
    #	Show meet information.
    #   The query is the same as HW #7.
    query = '''

with t as(select distinct p.EventId,concat(s.fname,' ',s.lname) as Swimmer, concat (c.fname,' ',c.lname,'( primary )') as 'PrimaryCaretaker' ,IFNULL(group_concat(concat(c1.fname,' ',c1.lname,'( alternate)') order by c1.lname separator ' , '),'') as 'SecondaryCaretakers',count(c.CT_Id+oc.CT_Id)+1 as cc from Participation p inner join swimmer s on (p.SwimmerId=s.SwimmerId) inner join caretaker c on (s.main_ct_id=c.ct_id) left join othercaretaker oc on(s.swimmerid=oc.swimmerid) left join caretaker c1 on (oc.ct_id=c1.ct_id) where p.EventId=%s group by (s.swimmerid) order by swimmer)
select distinct t.EventId,
Group_Concat(concat("<li> ",t.Swimmer," has ",t.cc," caretakers: ",t.SecondaryCaretakers," , ",t.PrimaryCaretaker,"</li>")separator ' ') as details from t ;
'''
    #   Show more information in the meet 
    cursor.execute(query,(int(eid),))
    (eid,details) = cursor.fetchone()
    print("<h3>Swimmers in event #" + str(eid) + "</h3>")
    print("<ol>",details,"<ol>")
    
                  
cursor.close()
cnx.close()		
				  
print ('''</body>
</html>''')