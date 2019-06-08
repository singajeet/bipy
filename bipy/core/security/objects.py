"""
 MetaModel objects for security (users, roles, etc) to be used by OLAP services
 Author: Ajeet Singh
 Date: 5/13/2019
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Sequence, DateTime, ForeignKey
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase


Base = declarative_base()


class AbstractSecurityObject(AbstractConcreteBase, Base):
    """An abstract class representing an basic security object
    """
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(255))
    description = Column(String(255), nullable=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(255))
    modified_on = Column(DateTime)
    modified_by = Column(String(255))


class UsersRoles(Base):
    """ An metamodel object to keep users and roles relationship
    """
    __tablename__ = 'warehouse_users_roles'

    user_id = Column(Integer, ForeignKey("warehouse_users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("warehouse_roles.id"), primary_key=True)


class User(AbstractSecurityObject):
    """ An metamodel object representing an User
    """
    __tablename__ = 'warehouse_users'

    password = Column(String(255))
    email = Column(String(255))
    phone = Column(String(255))
    roles = relationship("Role", secondary='warehouse_users_roles',
                         backref='warehouse_users')
    session_key = Column(String(255))
    is_active = Column(Boolean)
    is_loggedin = Column(Boolean)

    def __repr__(self):
        """ String representation
        """
        return "User [Name=%s, Email=%s]" % (self.name, self.email)


class Role(AbstractSecurityObject):
    """ An metamodel object representing an Role
    """
    __tablename__ = 'warehouse_roles'

    users = relationship("User", secondary='warehouse_users_roles', backref='warehouse_roles')
    privileges = relationship("Privilege", secondary='warehouse_roles_privileges',
                              backref="warehouse_roles")

    def __repr__(self):
        """ String representation
        """
        return "Role [Name=%s, Description=%s]" % (self.name, self.description)


class RolePrivileges(Base):
    """ An metamodel object to keep roles & privileges relationship
    """
    __tablename__ = 'warehouse_roles_privileges'

    role_id = Column(Integer, ForeignKey('warehouse_roles.id'), primary_key=True)
    privileg_id = Column(Integer, ForeignKey('warehouse_privileges.id'), primary_key=True)


class Privilege(AbstractSecurityObject):
    """ An metamodel object representing an Privilege
    """
    __tablename__ = 'warehouse_privileges'

    roles = relationship("Role", secondary='warehouse_roles_privileges',
                         backref='warehouse_privileges')

    def __repr__(self):
        """ String representation
        """
        return "Privilege [Name=%s, Description=%s]" % (self.name, self.description)


class SecuritySession(AbstractSecurityObject):
    session_key = Column(String(255))
    user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
    is_valid = Column(Boolean)
