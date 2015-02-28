
import json, time
from django.views.generic import ListView
from django.http import Http404
from django.shortcuts import render_to_response
import hashlib
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
#import xml.etree.cElementTree as xml

from lxml import etree as xml
from school import models as SchoolModels


TAG_XML_ARRAY      = "list"
TAG_XML_DICT       = "dict"
TAG_XML_ITEM       = "item"
TAG_XML_ROOT       = "entity"
TAG_XML_ITEM_NAME  = "name"
TAG_XML_SERVERTIME = "servertime"
TAG_XML_STATUS     = "status"
TAG_XML_COUNT      = "count"
TAG_XML_DATA       = "data"

## \brief array of errors
class RestError:
    bad_request = {"code":701,"message":"incorrect format of request"}
    no_data     = {"code":702,"message":"no found any data for request"}
    bad_passwd  = {"code":703,"message":"incorrect login/password"}
    bad_token   = {"code":704,"message":"incorrect token"}

## \brief array of type of response
class TypeRestResponse:
    json = 0
    xml = 1
    
## \brief base class  for any handlers
class BaseRestView(ListView):
    type_response = None
#=====================================================================
    ## \brief create xml scalar item
    #  \param arr input structure
    #  \return xml object 
    def __createXmlItem( self, value ):
        root = xml.Element(TAG_XML_ITEM)
        try:
            t = str(value).decode("UTF-8")
            if len(t) and t != "[]":
                root.text = t
        except UnicodeEncodeError, e:
                print "bad encode %s" % e
        return root
    
#=============================================================================
    ## \brief create xml dist
    #  \param arr input scructure
    #  \return xml object 
    def __createXmlDict( self, arr ):
        if not len(arr):
            return None
        root = xml.Element(TAG_XML_DICT)
        root.set(TAG_XML_COUNT, str(len(arr)))
        for a in arr:
            item = None
            if type(arr[a]) is dict and len(arr[a]):
           #     print "dist=>dist"
                item = self.__createXmlDict(arr[a])
            elif type(arr[a]) is list and len(arr[a]): 
             #   print "dist=>array"
                item = self.__createXmlArray(arr[a])
            else:
             #   print "dist=>item"
                try:
                    item = self.__createXmlItem(arr[a])
                except:
                        print arr[a]
                        raise
            if item is not None :
                item.set(TAG_XML_ITEM_NAME, str(a).decode("UTF-8"))
                root.append(item)
        return root
#============================================================================
    ## \brief create xml list
    #  \param arr input structure
    #  \return xml object 
    def __createXmlArray(self, arr ):
        if not len(arr):
            return None
        root = xml.Element(TAG_XML_ARRAY)
        root.set(TAG_XML_COUNT, str(len(arr)))
        for a in arr:
            item = None
            if type(a) is dict and len(a):
                item = self.__createXmlDict(a)
            elif type(a) is list and len(a): 
           
                item = self.__createXmlArray(a)
            elif len(str(a)):
                item = self.__createXmlItem(a)
             
            if item is not None:
                root.append(item)
        return root
    
    
    def _finish(self, status, data ):
        #type = data
        res = {
               TAG_XML_STATUS: "success" if status else "error",
               TAG_XML_DATA: data,
               TAG_XML_SERVERTIME: time.time()
        }
        if self.type_response == TypeRestResponse.json:
            res = {"data":json.dumps(res)}
        else:
            root = xml.Element(TAG_XML_ROOT)
            root.set(TAG_XML_STATUS,res[TAG_XML_STATUS])
            root.set(TAG_XML_SERVERTIME, str(TAG_XML_SERVERTIME))
            print res[TAG_XML_DATA]
            item =  self.__createXmlDict(res[TAG_XML_DATA]) if type(res[TAG_XML_DATA]) is dict else self.__createXmlArray(res[TAG_XML_DATA])
           
            if item is not None:
                root.append(item)
            res = {"data": xml.tostring( root, pretty_print=True, xml_declaration=True, encoding='UTF-8')}
        return render_to_response('simple.json', res)
    
    #    return render_to_response('base.xml', res)
    
    def _validTypeResponce(self, t):
        if t == 'xml':
            self.type_response = TypeRestResponse.xml
        elif t == 'json':
            self.type_response = TypeRestResponse.json
        else:
            raise Http404("bad type of content, need xml|json only")
        return True


## \brief class auth any clients and genetation of token
class AuthRestToken(BaseRestView):
    

    def post(self, request, *args, **kwargs):
        self._validTypeResponce(args[0].lower())
        
        
        user = request.POST['user'] if 'user' in request.POST else None 
        passwd = request.POST['passwd'] if 'passwd' in request.POST else None
        
        
        args ={}
        if hasattr(request, 'session') and not request.session.session_key:
            request.session.modified = True
            request.session.set_expiry(140000)
            request.session.save()
        session_key = request.session.session_key if "sessionid" not in request.POST else request.POST['sessionid']
        
        print repr(session_key)
        if user is None or passwd is None:
            args["sessionid"] = str(session_key)
            return self._finish(True, args)
        elif not User.objects.filter(username=user).count():
            self._finish(False, RestError.bad_passwd)
            
        u = User.objects.filter(username=user).get()
        secret_pass = "test"
        
        if (False and not  hashlib.sha256(session_key + 
                            secret_pass + 
                            session_key + 
                            secret_pass +
                            session_key ).hexdigest() != passwd):
            return self._finish(False, RestError.bad_passwd)

        token = Token.objects.get_or_create(user=u)[0]
        token.delete()
        token = Token.objects.create(user=u)
        
        args["token"] = token.key
        #=======================================================================
        return self._finish(True, args)


## \brief main class for REST API
class QuaryHandler(BaseRestView):

    def post(self, request, *args, **kwargs):
        self._validTypeResponce(args[0].lower())
        
        
        token = request.POST['token'] if 'token' in request.POST else None
        if token is None or not Token.objects.filter(key=token).count():
            return self._finish(False, RestError.bad_token) 
        
       # curr_user = Token.objects.get(key=token).user
        
        query = request.POST['query'] if 'query' in request.POST else None
        if query is None:
            print "no set query name"
            return self._finish(False, RestError.bad_request)
        qtype = request.POST['type'] if 'type' in request.POST else "get"
        query_name = qtype + '_' + query
        func = None
        try:
            func = getattr(self, query_name)
        except AttributeError, e:
            print str(e)
            return self._finish(False, RestError.bad_request)
        
        keys  = request.POST['key'] if 'key' in request.POST else ""
        keys = keys.split("|")
        values = request.POST['value'] if 'value' in request.POST else ""
        values = values.split("|")
        if len(keys) != len(values):
            print 'lengths of key/values are different'
            return self._finish(False, RestError.bad_request)
        values = {x:y for x,y in zip(keys,values) if len(x) and len(y)}
        
        res = func( values)
        if res is None:
            return self._finish(False, RestError.bad_request)
        return self._finish(True, res)
    
#=========================================================================================
    ## \brief get status object by its name
    #  \param n name of status
    #  \return object or None
    def __getStatus(self, n):
      #  print n
        if n is None or not SchoolModels.Status.objects.filter(name=n).count():
            return None
        return SchoolModels.Status.objects.get(name=n)
    
#=========================================================================================
    ## \brief get person object by its id
    #  \param i id of person
    #  \return object or None
    def __getPerson(self, i):
        if i is None or not SchoolModels.Person.objects.filter(id=i).count():
            return None
        return SchoolModels.Person.objects.get(id=i)
    
#=========================================================================================
    ## \brief get type of person by its name
    #  \param n name of status
    #  \return object or None
    def __getPersonType(self, n):
        print SchoolModels.Type.objects.all()
        if n is None or not SchoolModels.Type.objects.filter(name=n).count():
            return None
        return SchoolModels.Type.objects.get(name=n)
    
#=========================================================================================
    ## \brief check and split of line with ids
    #  \param param string
    #  \return list or None
    def __parseIds(self, param, is_str):
        if param is None:
            return None 
        return  [ int(r) if not is_str else r for r in param.split(",")  if is_str or r.isdigit() ]
#==============API FUNCTIONS==============================================================
#=========================================================================================
    ## \brief create data for API, set/update person entity
    #  \param values dist of parameters
    #  \return dist of data or None
    def set_person(self, values):
        person_id = None if "id" not in values or not values["id"].isdigit() else  int(values["id"])
        first_name = None if "first_name" not in values else  values["first_name"]
        last_name = None if "last_name" not in values else  values["last_name"]
        status = self.__getStatus(None if "status" not in values else  values["status"])
        types = self.__parseIds(None if "type" not in values else  values["type"],True)
        if types is not None:  types = [ self.__getPersonType(r) for r in types ]
        
        person = None
        if person_id is None:
            #create the new person
            if status is None:
                status = self.__getStatus("present")
            if(first_name is None or
               last_name is None ):
                    return None
            person = SchoolModels.Person(first_name=first_name,
                                         last_name=last_name,
                                         status=status)
            person.save()
        elif SchoolModels.Person.objects.filter(id=person_id).count():
            person = SchoolModels.Person.objects.get(id=person_id)
        else:
            return None
        
        if first_name is not None:
            person.first_name = first_name
        
        if last_name is not None:
            person.last_name = last_name
            
        if status is not None:
            person.status =  status
        
        if types is not None:
            for t in person.type.all(): person.type.remove(t)
            for t in types:
                print r
                if t is None: continue
                person.type.add(t)
            
        person.save()
        return self.get_person({"id":str(person.id)})
    
#======================================================================================================
    ## \brief create data for API, get person entity by id
    #  \param values dist of parameters
    #  \return dist of data or None
    def get_person(self, values):
        person_id = self.__parseIds( None if "id" not in values else  values["id"], False)
        if person_id is not None:
            persons = SchoolModels.Person.objects.filter(id__in=person_id)
        else:
            persons = SchoolModels.Person.objects.all()
        if not len(persons):
            return None
        res = []
        for p in persons:
            pp = {
                    "first_name": p.first_name,
                    "last_name": p.last_name,
                    "status": p.status.name,
                    "types": [],
                    "id": p.id,
                  }
            for t in p.type.all():
                pp["types"].append(t.name)
            res.append(pp)
        return res
    
#==========================================================================================
    ## \brief create data for API, remove person entity by id
    #  \param values dist of parameters
    #  \return dist of data or None
    def del_person(self, values):
        person_id = self.__parseIds( None if "id" not in values else  values["id"], False)
        if person_id is None:
            return None
        
        persons = SchoolModels.Person.objects.filter(id__in=person_id)
        if not len(persons):
            return None
        for p in persons:
            p.delete()
        return []
    
#===========================================================================================
    ## \brief create data for API, set/update school class entity
    #  \param values dist of parameters
    #  \return dist of data or None
    def set_class(self, values):
        class_id = None if "id" not in values or not values["id"].isdigit() else  int(values["id"])
        name = None if "name" not in values else  values["name"]
        teacher = None if "teacher_id" not in values or not values["teacher_id"].isdigit() else  int(values["teacher_id"])
        if teacher is not None:
            teacher = self.__getPerson(teacher)
        status  = self.__getStatus(None if "status" not in values else  values["status"])
        pupils = self.__parseIds(None if "pupils" not in values else  values["pupils"],True)
        if pupils is not None:  pupils = [ self.__getPerson(p) for p in pupils ]
        
        sclass = None
        if class_id is None:
            #create the new class
            if status is None:
                status = self.__getStatus("present")
            if(name is None or
               teacher is None ):
                    return None
            
            sclass = SchoolModels.SchoolClass(cname=name,
                                         teacher=teacher,
                                         status=status)
            sclass.save()
            
        elif SchoolModels.SchoolClass.objects.filter(id=class_id).count():
            sclass = SchoolModels.SchoolClass.objects.get(id=class_id)
        else:
            return None
        print repr(sclass)
        if name is not None:
            sclass.name = sclass
        
        if teacher is not None:
            sclass.teacher = teacher
            
        if status is not None:
            sclass.status =  status
        
        if pupils is not None:
            for p in sclass.pupil.all(): sclass.pupil.remove(p)
            for p in pupils:
                if p is None: continue
                sclass.pupil.add(p)
            
        sclass.save()
        return self.get_class({"id":str(sclass.id)})
    
#======================================================================================================
    ## \brief create data for API, get class entity by id
    #  \param values dist of parameters
    #  \return dist of data or None
    def get_class(self, values):
        class_id = self.__parseIds( None if "id" not in values else  values["id"], False)
        if class_id is not None:
            classes = SchoolModels.SchoolClass.objects.filter(id__in=class_id)
        else:
            classes = SchoolModels.SchoolClass.objects.all()
        if not len(classes):
            return None
        
        res = []
        for c in classes:
            pp = {
                    "name": c.cname,
                    "teacher": str(c.teacher),
                    "teacher_id": c.teacher.id,
                    "status": c.status.name,
                    "pupils": [],
                    "id": c.id,
                  }
            for p in c.pupil.all():
                pp["pupils"].append({"name": str(p),"id":p.id})
            res.append(pp)
        return res
    
#==========================================================================================
    ## \brief create data for API, remove class entity by id
    #  \param values dist of parameters
    #  \return dist of data or None
    def del_class(self, values):
        class_id = self.__parseIds( None if "id" not in values else  values["id"], False)
        if class_id is None:
            return None
        
        classes = SchoolModels.SchoolClass.objects.filter(id__in=class_id)
        if not len(classes):
            return None
        for p in classes:
            p.delete()
        return []
#==========================================================================================