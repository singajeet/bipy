"""

 An security manager which deals with security objects and
 also provides authentication & authorization objects
 Author: Ajeet Singh
 Date: 5/13/2019

"""
from datetime import datetime
# import socket
from bipy.services.security.objects import User, Role, Privilege, SecuritySession


class SecurityManager:

        ConnectedSession = None
        __instance = None

        def __new__(cls, val):
            if SecurityManager.__instance is None:
                SecurityManager.__instance = object.__new__(cls)
            SecurityManager.__instance.val = val
            return SecurityManager.__instance

        def __init__(self, connection):
            self.ConnectedSession = connection.get_session()

        def __repr__(self):
            return "Security Manager"

        def _update_generic_properties(self, old, new):
            old.name = new.name
            old.description = new.description
            old.modified_on = datetime.utcnow
            # old.modified_by = SecurityManager.get_current_user()

        def add_user(self, user):
            self.ConnectedSession.add(user)
            self.ConnectedSession.commit()

        def add_role(self, role):
            self.ConnectedSession.add(role)
            self.ConnectedSession.commit()

        def addSession(self, session):
            self.ConnectedSession.add(session)
            self.ConnectedSession.commit()

        def add_privilege(self, privilege):
            self.ConnectedSession.add(privilege)
            self.ConnectedSession.commit()

        def update_user(self, updated_user):
            existing_user = self.ConnectedSession.query(User)\
                .filter(User.id == updated_user.id).first()
            self._update_generic_properties(existing_user, updated_user)
            existing_user.password = updated_user.password
            existing_user.email = updated_user.email
            existing_user.phone = updated_user.phone
            self.ConnectedSession.commit()

        def update_role(self, updated_role):
            existing_role = self.ConnectedSession.query(Role)\
                .filter(Role.id == updated_role.id).first()
            self._update_generic_properties(existing_role, updated_role)
            self.ConnectedSession.commit()

        def update_privilege(self, updated_privilege):
            existing_privilege = self.ConnectedSession.query(Privilege)\
                .filter(Privilege.id == updated_privilege.id).first()
            self._update_generic_properties(existing_privilege,
                                            updated_privilege)
            self.ConnectedSession.commit()

        def update_session(self, updated_session):
            existing_session = self.ConnectedSession.query(SecuritySession)\
                    .filter(SecuritySession.id == updated_session.id).first()
            self._update_generic_properties(existing_session, updated_session)
            self.ConnectedSession.commit()

        def delete_user(self, user):
            existing_user = self.ConnectedSession.query(User)\
                .filter(User.id == user.id).first()
            existing_user.delete()
            self.ConnectedSession.commit()

        def delete_role(self, role):
            existing_role = self.ConnectedSession.query(Role)\
                .filter(Role.id == role.id).first()
            existing_role.delete()
            self.ConnectedSession.commit()

        def delete_privilege(self, privilege):
            existing_privilege = self.ConnectedSession.query(Privilege)\
                .filter(Privilege.id == privilege.id).first()
            existing_privilege.delete()
            self.ConnectedSession.commit()

        def delete_session(self, session):
            existing_session = self.ConnectedSession.query(SecuritySession)\
                    .filter(SecuritySession.id == session.id).first()
            existing_session.delete()
            self.ConnectedSession.commit()

        def apply_role_on_user(self, role, user):
            user.roles.extend([role])
            self.ConnectedSession.commit()

        def remove_user_from_role(self, role, user):
            user.roles.remove(role)
            self.ConnectedSession.commit()

        def apply_privilege_to_role(self, privilege, role):
            role.privileges.extend([privilege])
            self.ConnectedSession.commit()

        def remove_privilege_from_role(self, privilege, role):
            role.privileges.remove(privilege)
            self.ConnectedSession.commit()

        def get_user(self, param):
            if isinstance(param, int):
                return self.ConnectedSession.query(User)\
                        .filter(User.id == param)
            elif isinstance(param, str):
                return self.ConnectedSession.query(User)\
                        .filter(User.name == param)
            return None

        def get_role(self, param):
            if isinstance(param, int):
                return self.ConnectedSession.query(Role)\
                        .filter(Role.id == param)
            elif isinstance(param, str):
                return self.ConnectedSession.query(Role)\
                        .filter(Role.name == param)
            return None

        def get_privilege(self, param):
            if isinstance(param, int):
                return self.ConnectedSession.query

        def get_roles_for_user(self, user):
            return user.roles

        def get_privileges_for_role(self, role):
            return role.privileges

        def required_privilege_exists(self, req_prv, prv_list):
            for prv in prv_list:
                if prv.id == req_prv.id:
                    return True
            return False

        def authorize(self, req_privilege):
            # logic to check user is authenticated
            user = self.get_current_user()
            user_roles = self.get_roles_for_user(user)
            auth = False
            for role in user_roles:
                privileges = self.get_privileges_for_role(role)
                auth = self.required_privilege_exists(req_privilege,
                                                      privileges)
                if(auth):
                    pass
                #     return True
            return True  # Always return true for now

        def get_current_user(self):
            """session = self.ConnectedSession.query(SecuritySession)\
                    .filter(SecuritySession.host_name == hostname
                            and SecuritySession.ip_address == ip
                            and SecuritySession.is_valid == True
                            and SecuritySession.session_key is not None)\
                                .first()
            if session is not None:
                user_id = session.user_id
                user = self.get_user(user_id)
                if user is not None:
                    if user.is_active and user.is_loggedin and session\
                            .is_valid\
                       and session.session_key is not None and \
                       session.session_key == user.session_key:
                        return True
            return False
            """
            u = User()
            u.name = "root"
            return u
