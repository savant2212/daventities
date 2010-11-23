from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, relationship, backref

from sqlalchemy.sql.expression import desc
import time

Base = declarative_base()

class ActionRestrict(Base):
    __tablename__='Restrictions'
    id          = Column(Integer, primary_key=True)
    actor_id    = Column(Integer)
    actor_type  = Column(Integer)    
    object_id   = Column(Integer)
    action   = Column(Integer)    

    def __init__(self, actor_id, actor_type, object_id, action):
        self.actor_id = actor_id
        self.actor_type = actor_type
        self.object_id = object_id
        self.action = action
        
     

# user data
user_group = Table(
    'UserGroups', Base.metadata,    
    Column('user_id', Integer, ForeignKey('Users.id')),
    Column('group_id', Integer, ForeignKey('Groups.id'))
    )

group_directory = Table(
    'GroupDirectories', Base.metadata,    
    Column('object_id', Integer, ForeignKey('TreeObjects.id')),
    Column('group_id', Integer, ForeignKey('Groups.id'))
    )

user_directory = Table(
    'UserDirectories', Base.metadata,    
    Column('object_id', Integer, ForeignKey('TreeObjects.id')),
    Column('user_id', Integer, ForeignKey('Users.id'))
    )

class ObjectRevision(Base):
    __tablename__= 'ObjectRevisions'
    id = Column(Integer , primary_key=True)
    revision  = Column(Integer)
    mod_time  = Column(Float)
    TreeObjects_id = Column(Integer, ForeignKey('TreeObjects.id'))
    Contents_id= Column(Integer, ForeignKey('Contents.id'))
    content = relationship("Content", backref=backref("object_assocs", uselist=False), uselist=False, cascade="all")
    
        
class User(Base):
    __tablename__='Users'
    id          = Column(Integer, primary_key=True)
    login       = Column(String)
    password    = Column(String)
    full_name   = Column(String)
    groups      = relationship("Group", secondary=user_group, backref='User')
    directories = relationship("TreeObject", secondary=user_directory, backref='User')
    is_deleted  = Column(Boolean,nullable=False)
    
    def __init__(self, login, password, full_name, is_deleted=False):
        self.login = login
        self.password = password
        self.full_name = full_name
        self.is_deleted = is_deleted
    
    def getRestrictions(self, obj, sess):        
        return sess.query(ActionRestrict).filter_by(actor_id=self.id, object_id=obj.id, actor_type='1')

class Group(Base):
    __tablename__='Groups'
    id          = Column(Integer, primary_key=True)    
    name        = Column(String)
    parent_id   = Column(Integer, ForeignKey('Groups.id'))
    users       = relationship("User", secondary=user_group, backref='Group')
    directories = relationship("TreeObject", secondary=group_directory, backref='Group')
    is_deleted  = Column(Boolean, nullable=False)
    base_dir_id = Column(Integer, ForeignKey('TreeObjects.id'))
    base_dir    = relationship("TreeObject", backref=backref("Groups", uselist=False))
    subgroups   = relationship("Group",
                    backref=backref('parent', remote_side=id)
                )
    
    def __init__(self, name, base_dir = None, parent = None, is_deleted=False):
        self.name=name
        self.is_deleted = is_deleted
        self.parent  = parent        
        self.base_dir   = base_dir

#content
class Content(Base):
    __tablename__= 'Contents'

    id        = Column(Integer, primary_key=True)
    content   = Column(String)    
    is_deleted  = Column(Boolean)
    mime_type = Column(String)
    
    def __init__(self, content, mime_type='application/octet-stream'):
        self.content    = content
        self.mime_type  = mime_type

    def __repr__(self):
        return "<Content('%s','%s')>" % (self.id, self.content)


class TreeObject(Base):
    __tablename__= 'TreeObjects'
    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    type        = Column(Integer)
    parent_id   = Column(Integer, ForeignKey('TreeObjects.id'))
    owner       = Column(Integer)
    group       = Column(Integer)
    size        = Column(Integer)    
    path        = Column(String)
    mod_time    = Column(Float)
    creat_time  = Column(Float)
    is_deleted  = Column(Boolean, nullable=False)
    
    #revisions =  relationship('Content', secondary=object_revision, backref='objects', order_by=desc("Contents.revision"))
    revisions = relationship("ObjectRevision", backref="objects", order_by=desc("ObjectRevisions.revision"), cascade='all')
    
    nodes   = relationship("TreeObject",
                    backref=backref('parent', remote_side=id)
                )   
  
    
    TYPE_FILE       = 0
    TYPE_COLLECTION = 1
    TYPE_HISTORY    = 2
    TYPE_REV_FILE   = 3
    
    def get_last_revision(self):
        if len(self.revisions) > 0:
            return self.revisions[0]
        else:
            return None
    
    last_revision=property(get_last_revision)

    def __init__(self, name, type, parent, owner, group, size, content, path,
        creat_time=time.time(), mod_time=time.time(),is_deleted=False):
        self.name      = name
        self.type      = type
        self.parent    = parent
        self.owner     = owner
        self.group     = group
        self.size      = size
        self.content   = content
        self.path      = path
        self.mod_time  = mod_time
        self.creat_time= creat_time
        self.is_deleted= is_deleted

    def __repr__(self):
        return "<TreeObject('%s','%s','%s',)>" % (
         self.name, self.type, self.parent)
