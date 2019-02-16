import cx_Oracle
try:
from multiprocessing.managers import State
con = cx_Oracle.connect(&quot;system/password@localhost/xe&quot;)
cur = con.cursor()
#estate table
statement = &quot;&quot;&quot; create table rl_estate(
pid number(10) not null PRIMARY KEY,
pcat Varchar2(20),
ploc Varchar2(50),
ptype Varchar2(20),
parea Varchar2(50),
pfur Varchar2(3),
pvalue number
)&quot;&quot;&quot;
cur.execute(statement)
#agent table
statement = &quot;&quot;&quot; create table rl_agent(
ag_id number(10) not null PRIMARY KEY,
ag_name Varchar2(20),
ag_loc Varchar2(15)
)&quot;&quot;&quot;
cur.execute(statement)
agent_data = [(201,&quot;Rahul Dua&quot;,&quot;delhi&quot;),(202,&quot;Shankar
Chugani&quot;,&quot;chennai&quot;),(203,&quot;Saurav Mehta&quot;,&quot;mumbai&quot;),(204,&quot;Sejal Bhatt&quot;,&quot;kolkata&quot;)]
statement = &quot;&quot;&quot;insert into rl_agent(ag_id,ag_name,ag_loc) values(:1,:2,:3)
&quot;&quot;&quot;
cur.executemany(statement,agent_data)
con.commit()
statement = &quot;&quot;&quot;create table handlers(
ag_id number(10),
pid number(10),
constraint fk_agent foreign key (ag_id) references
rl_agent(ag_id),
constraint fk_prop foreign key (pid) references rl_estate(pid)
)
&quot;&quot;&quot;
cur.execute(statement)
#customer table
statement = &quot;&quot;&quot;create table rl_customer(
cid number(10) not null PRIMARY KEY,
cname Varchar2(40),
cloc Varchar2(15),
cstatus Varchar2(10)
)&quot;&quot;&quot;
cur.execute(statement)
#owned table
statement = &quot;&quot;&quot; create table owned(
pid number(10),
cid number(10),
constraint fk_estate foreign key (pid) references
rl_estate(pid),

constraint fk_customer foreign key (cid) references
rl_customer(cid)
)&quot;&quot;&quot;
cur.execute(statement)
#BUY/RENT function
def buy_rent():
cid = int(input(&quot;Enter your customer ID:&quot;))
pid = int(input(&quot;Enter property ID: &quot;))
agent = getagent(pid)
print(&quot;Please contact our agent&quot;,agent,&quot;for further transactions.&quot;)
print(&quot;Following property has been reserved for you!&quot;)
cur.execute(&quot;select * from rl_estate where pid = :p1&quot;,{&#39;p1&#39;:pid})
print(cur.fetchall())
statement=&quot;insert into owned values(:p1,:p2)&quot;
cur.execute(statement,{&#39;p1&#39;:pid,&#39;p2&#39;:cid})
statement = &quot;&quot;&quot;update rl_estate set ptype = &#39;owned&#39; where pid = :p1&quot;&quot;&quot;
cur.execute(statement,{&#39;p1&#39;:pid})
statement = &quot;&quot;&quot;update rl_customer set cstatus = &#39;inactive&#39; where cid =
:p1&quot;&quot;&quot;
cur.execute(statement,{&#39;p1&#39;:cid})
con.commit()
#GetAgent function
def getagent(pid):
statement = &quot;select ag_name from rl_agent where ag_id in (select ag_id
from handlers where pid =:p1)&quot;
cur.execute(statement,{&#39;p1&#39;:pid})
res = cur.fetchall()
res = res[0][0]
return res
#CLASS ESTATE
class rl_estate:
def __init__(self):
self.input()
self.update()
self.ragent()
def input(self):
self.pid = int(input(&quot;Enter property ID: &quot;))
self.pcat = input(&quot;Enter Category(Apartment,Builder
Floor,Villa,Shop,PG): &quot;).lower()
self.ploc = input(&quot;Enter location of the
property(Delhi,Mumbai,Chennai,Kolkata):&quot;).lower()
self.ptype = input(&quot;Sale / Rent :&quot;).lower()
self.parea = int(input(&quot;Enter area of property in sqft: &quot;))
self.furnished = input(&quot;Is furnished?(yes/no): &quot;)
self.pvalue =0
if (self.ptype == &quot;rent&quot; or self.ptype == &quot;Rent&quot;) and
self.furnished==&quot;yes&quot;:
self.pvalue = int((self.parea * 10)) #so as to make monthly
rent area multiplied by 10000 divided by 12
elif (self.ptype == &quot;rent&quot; or self.ptype == &quot;Rent&quot;) and
self.furnished==&quot;no&quot;:
self.pvalue = int((self.parea * 5)) #so as to make monthly
rent area multiplied by 6500 divided by 12
elif (self.ptype == &quot;Sale&quot; or self.ptype == &quot;sale&quot;) and
self.furnished==&quot;yes&quot;:
if self.parea &gt; 20000 :
self.pvalue = self.parea*9000
elif self.parea &gt; 12000 and self.parea &lt;=20000:
self.pvalue = self.parea*6500
else:

self.pvalue = self.parea*4500
elif (self.ptype == &quot;Sale&quot; or self.ptype == &quot;sale&quot;) and
self.furnished==&quot;no&quot;:
if self.parea &gt; 20000 :
self.pvalue = self.parea*5000
elif self.parea &gt; 15000 and self.parea &lt;=20000:
self.pvalue = self.parea*3000
else:
self.pvalue = self.parea*2000
print(&quot;Expected Value of property: INR.%d&quot;%self.pvalue)
def update(self):
statement = &quot;&quot;&quot; insert into rl_estate values
(:p1,:p2,:p3,:p4,:p5,:p6,:p7)&quot;&quot;&quot;
cur.execute(statement,{&quot;p1&quot;:self.pid,&quot;p2&quot;:self.pcat,&quot;p3&quot;:self.ploc,&quot;p4&quot;:self.ptype
,&quot;p5&quot;:self.parea,&quot;p6&quot;:self.furnished,&quot;p7&quot;:self.pvalue})
con.commit()
print(&quot;Property details added to database!&quot;)
def ragent(self):
statement = &quot;select ag_id from rl_agent where ag_loc = :p1&quot;
cur.execute(statement,{&#39;p1&#39;:self.ploc})
self.res = cur.fetchall()
self.ag_id = self.res[0][0]
statement = &quot;&quot;&quot;insert into handlers values(:1,:2)&quot;&quot;&quot;
cur.execute(statement,(self.ag_id,self.pid))
self.ag_fee = self.pvalue / 4
self.ag_fee = &quot;%.2f&quot;%self.ag_fee
cur.execute(&quot;select ag_name from rl_agent where ag_loc=:p1
&quot;,{&#39;p1&#39;:self.ploc})
res = cur.fetchall()
res = res[0][0]
print(&quot;Agent :&quot;,res,&quot;has been assigned to property ID:&quot;,self.pid)
def display(self):
cur.execute(&quot;select * from rl_estate where pid= :p1&quot;,{&#39;p1&#39;:self.pid})
print(cur.fetchall())
#Display property function
def viewprop():
print(&quot;1.By Location\n2.By minimum area\n3.By category\n4. By customer&#39;s
budget\n5.For sale\n6.For rent\n7. View all Properties&quot;)
op = int(input(&quot;Enter choice (1-7):&quot;))
if op == 1:
loc = input(&quot;Enter location (choose from Delhi, Mumbai, Kolkata,
Chennai):&quot;).lower()
statement =&quot;&quot;&quot;select * from rl_estate where ploc =:p1&quot;&quot;&quot;
cur.execute(statement,{&#39;p1&#39;:loc})
res = cur.fetchall()
for i in res:
print(i)
elif op ==2:
sqft = int(input(&quot;Enter minimum property area:&quot;))
statement =&quot;&quot;&quot;select * from rl_estate where parea &gt;=:p1&quot;&quot;&quot;
cur.execute(statement,{&#39;p1&#39;:sqft})
res = cur.fetchall()
for i in res:
print(i)
elif op == 3:
cat = input(&quot;Enter category (choose from Villa,Builder
Floor,Apartment,Shop,PG): &quot;).lower()
statement =&quot;&quot;&quot;select * from rl_estate where pcat =:p1&quot;&quot;&quot;
cur.execute(statement,{&#39;p1&#39;:cat})
res = cur.fetchall()
for i in res:

print(i)
elif op == 4:
value = int(input(&quot;Enter your budget: INR.&quot;))
statement =&quot;&quot;&quot;select * from rl_estate where pvalue &lt;=:p1&quot;&quot;&quot;
cur.execute(statement,{&#39;p1&#39;:value})
res = cur.fetchall()
for i in res:
print(i)
elif op ==5:
print (&quot;Following properties are for sale:&quot;)
statement = &quot;select * from rl_estate where ptype = &#39;sale&#39;&quot;
cur.execute(statement)
res = cur.fetchall()
for i in res:
print(i)
elif op ==6:
print (&quot;Following properties are for rent:&quot;)
statement = &quot;select * from rl_estate where ptype = &#39;rent&#39;&quot;
cur.execute(statement)
res = cur.fetchall()
for i in res:
print(i)
elif op ==7:
print (&quot;Following properties:&quot;)
statement = &quot;select * from rl_estate where ptype = &#39;rent&#39; or ptype
= &#39;sale&#39;&quot;
cur.execute(statement)
res = cur.fetchall()
for i in res:
print(i)
else:
print(&quot;Incorrect choice.&quot;)
print(&quot;Interested in buying or renting any property?&quot;)
xyz = input(&quot;Enter yes or no: &quot;)
if xyz == &#39;yes&#39;:
buy_rent()
#CUSTOMER CLASS
class rl_customer:
def __init__(self):
self.cid = int(input(&quot;Enter customer ID: &quot;)) # Customer id
self.cname = input(&quot;Enter customer name: &quot;) #Cusotmer Name
self.cloc= input(&quot;Enter your location (choose from
Delhi,Kolkata,Mumbai,Chennai):&quot;).lower()
self.cbudget= int(input(&quot;Enter customer budget: &quot;)) #Maximum amount
customer willing to spend
self.ctype = input(&quot;looking for buying/ renting?(enter buy /
rent):&quot;).lower()
self.update()
self.view_estate()
def view_estate(self):
if self.ctype == &quot;buy&quot; :
statement = &quot;&quot;&quot;select * from rl_estate where ptype = &#39;sale&#39; and
ploc = :p2 and pvalue &lt;= :p1&quot;&quot;&quot;
cur.execute(statement,{&#39;p1&#39;:self.cbudget,&#39;p2&#39;:self.cloc})
res = cur.fetchall()
print(&quot;Properties that may interest you:&quot;)
for i in res: print(i)
print(&quot;Interested in buying or renting any property?&quot;)
xyz = input(&quot;Enter yes or no: &quot;)
if xyz == &#39;yes&#39;:
buy_rent()
elif self.ctype == &quot;rent&quot;:

statement = &quot;&quot;&quot;select * from rl_estate where ptype = &#39;rent&#39; and
pvalue &lt;= :p1 and ploc = :p2&quot;&quot;&quot;
cur.execute(statement,{&#39;p1&#39;:self.cbudget,&#39;p2&#39;:self.cloc})
res = cur.fetchall()
print(&quot;Properties that may interest you:&quot;)
for i in res: print(i)
print(&quot;Interested in buying or renting any property?&quot;)
xyz = input(&quot;Enter yes or no: &quot;)
if xyz == &#39;yes&#39;:
buy_rent()
else:
print(&quot;Incorrect customer details added&quot;)
def update(self):
statement = &quot;&quot;&quot; insert into rl_customer values (:p1,:p2,:p3,:p4)&quot;&quot;&quot;
cur.execute(statement,{&quot;p1&quot;:self.cid,&quot;p2&quot;:self.cname,&quot;p3&quot;:self.cloc,&quot;p4&quot;:&quot;active&quot;}
)
con.commit()
print(&quot;Customer details added to database!&quot;)
ch = 0
while(ch &lt;=3):
print(&quot;Menu\n1.Enter Real Estate Details\n2.Enter Customer
Details\n3.View Property \n4.Buy or Rent estate\n5.Exit&quot;)
ch = int(input(&quot;Enter choice (1-5): &quot;))
if ch == 1:
r1 = rl_estate()
elif ch == 2:
c1 = rl_customer()
elif ch == 3:
viewprop()
elif ch == 4:
print(&quot;Browse our real estate catalogue:&quot;)
viewprop()
elif ch == 5:
print(&quot;You chose to exit. Thanks for using the software.&quot;)
else:
raise ValueError
con.close()
except ValueError as e:
print(&quot;Value Error!&quot;,e)
except TypeError as e:
print(&quot;Type Error!&quot;,e)
except IOError as e:
print(&quot;IO Error!&quot;,e)
except cx_Oracle.DatabaseError as e:
print(&quot;Database Error!&quot;,e)
