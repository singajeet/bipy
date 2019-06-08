"""

 An security manager which deals with security objects and
 also provides authentication & authorization objects
 Author: Ajeet Singh
 Date: 5/13/2019

"""
from datetime import datetime
from bipy.core.security.objects import User, Role, Privilege


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

        def get_roles_for_user(self, user):
            pass

        def get_privileges_for_role(self, role):
            pass

        def required_privilege_exists(self, req_prv, prv_list):
            pass

        def authorize(self, user, req_privilege):
            # logic to check user is authenticated
            user_roles = self.get_roles_for_user(user)
            auth = False
            for role in user_roles:
                privileges = self.get_priviliges_for_role(role)
                auth = self.required_privilege_exists(req_privilege,
                                                      privileges)
                if(auth):
                    return True
            return False

        def get_current_user(self):
            pass
