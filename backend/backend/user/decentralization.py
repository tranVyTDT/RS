from django.contrib.auth.models import Permission, Group


class UserGroupPermission:
    @staticmethod
    def get_staff_group():
        staff_group, created = Group.objects.get_or_create(name= 'staff') 
        # if created:
        #     permission_add_post   = Permission.objects.get(codename= 'add_post') 
        #     permission_delete_post = Permission.objects.get(codename= 'delete_post') 
        #     permission_change_post = Permission.objects.get(codename= 'change_post') 
        #     permission_view_post = Permission.objects.get(codename= 'view_post')
        #     learner_group.permissions.add(permission_add_post, permission_delete_post, permission_change_post, permission_view_post)
        #     return learner_group
        # else:
        return staff_group
    
    @staticmethod
    def get_director_group():
        director_group, created = Group.objects.get_or_create(name= 'director') 
        # if created:
        #     permission_view_post = Permission.objects.get(codename= 'view_post') 
        #     teacher_group.permissions.add(permission_view_post)
        #     return teacher_group
        # else:
        return director_group




