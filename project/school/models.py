from django.db import models



## \brief status of any entity
class Status(models.Model):
    id      = models.AutoField(primary_key=True)
    name    = models.CharField( max_length=64)
    blocked = models.BooleanField(default=False)
    
    ## \brief print info about object
    def __str__(self):
        return self.name

## \brief shcool subjects
class Subject(models.Model):
    id =         models.AutoField(primary_key=True)
    name = models.CharField( max_length=64)
    status = models.ForeignKey(Status) 
    
    def __str__(self):
        return self.name
    
## \brief personal type 
class Type(Subject): pass
    
    
     
## \brief base info about man
class Person(models.Model):
    
    id         = models.AutoField(primary_key=True)
    first_name = models.CharField( max_length=64)
    last_name  = models.CharField( max_length=64)
   # birthday   = models.DateField() 
    
    type       = models.ManyToManyField(Type)
    status     = models.ForeignKey(Status)
    
    ## \brief print info about object
    def __str__(self):
        return '/'.join([
            self.first_name,
            self.last_name,
        ])

## \brief school class
class SchoolClass(models.Model):
    id        = models.AutoField(primary_key=True)
    
    
    cname      = models.CharField( max_length=64, default="1a")

    teacher   = models.ForeignKey(Person) #, related_name='teacher_class')
    pupil     = models.ManyToManyField(Person, related_name='pupil_class')
    
    status    = models.ForeignKey(Status)
    
        
    
    def __str__(self):
        return """%s(%s)""" % (self.cname, self.teacher)
   


        

        

    