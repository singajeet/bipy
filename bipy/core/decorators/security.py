###################################################################################
#
# Various decorators for security ppurpose
# Author: Ajeet Singh
# Date: 5/15/2019
#
###################################################################################

def authorize(privilege):
    def do_authorization(func):
        def wrapper(*args, **kwargs):
            # Authorization logic will go here
            # Get current logged in user
            # if user have role for current privilege
            # execute function
            func(*args, **kwargs)
            # else throw exception
        return wrapper
    return do_authorization

