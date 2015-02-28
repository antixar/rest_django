@mainpage Simple REST API

@author Maksym Pavlenok
@mail antixar@gmail.com

========================


Description:
---------------------------
This is simple example to demonstrate  working REST API by Django python framework. This project works with 2 main entities:
> * Person - any human who works or studies  at school (teacher, pupil etc). Every person has status, name and list of roles. For example,
name = 'John/Carter', status = 'fired', roles = ['teacher', 'director']
> * SchoolClass - structure with list of pupils, a name, status and master. For example,
name = '5a', status = 'present', pupils = ['Marta/Siemens','John/Kent'], master = 'John/Carter'.

-------------------------------
All requests must have "POST" type of HTTP.
For working with API, need to get token by login/password of client by 2 steps:
1) client => server: http://127.0.0.1:8080/(xml|json)/auth/ without parameters.
   server => client: json or xml with sessionid
2) client => server: http://127.0.0.1:8080/(xml|json)/auth/ with:
> user - login of client
> sessionid - session id of client
> passwd - sha256( sessionid + client_passwd + sessionid + client_passwd + sessionid)
  server => client: json or xml with token that must be included into all other requests

API functions:
--------------------------------
HTTP link of all requests is http://127.0.0.1:8080/(xml|json)/query/
Type of requests:
> * set - create or update entity
> * get - show list of all entities by list of id
> * del - remove entities by list of id
Default type of request is 'get'

Examples:
----------------------------
POST parameters:
1) get list of all persons:
token=<TOKEN>&type=get&query=person
2) get list of all persons with id is 1 and 5
token=<TOKEN>&type=get&query=person&key=id&value=1,5
3) remove persons with id is 3
token=<TOKEN>&type=del&query=person&key=id&value=3
4) create the new teacher
token=<TOKEN>&type=set&query=person&key=first_name|last_name|status|type&value=John|Carter|present|teacher
5) create the new class
token=<TOKEN>&type=set&query=class&key=name|teacher_id|status|id|pupils&value=1a|9|present|39|10,11,12

All answers of server have standard format by xml or json. If query is incorrect server will return error with description




