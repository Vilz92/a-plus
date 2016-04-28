from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class UserProfileManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related("user")


class UserProfile(models.Model):
    """
    Additional user information and methods.
    """

    @classmethod
    def get_by_student_id(cls, student_id):
        return cls.objects.get(student_id=student_id)

    @classmethod
    def get_by_request(cls, request):
        if request.user.is_authenticated():
            return cls.objects.get(user=request.user)
        raise RuntimeError("Seeking user profile without authenticated user.")

    user = models.OneToOneField(User)
    lang = models.CharField(max_length=5, default="en_US")
    student_id = models.CharField(max_length=25, null=True, blank=True)
    objects = UserProfileManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "{} ({})".format(self.student_id, self.user.username)

    @property
    def avatar_url(self):
        """
        URL address for gravatar image based on the user email.
        """
        import hashlib
        hash_key = hashlib.md5(self.user.email.encode('utf-8')).hexdigest()
        return "http://www.gravatar.com/avatar/" + hash_key + "?d=identicon"

    @property
    def shortname(self):
        """
        A short version of the user's name in form "John D."
        """
        try:
            return self.user.first_name + " " + self.user.last_name[0] + "."
        except:
            return self.user.username

    @property
    def is_external(self):
        """
        Is this an external rather than internal account.
        """
        return hasattr(self.user, 'social_auth') and self.user.social_auth.exists()


def create_user_profile(sender, instance, created, **kwargs):
    """
    This function automatically creates an user profile for all new User models. The profiles
    are used for extending the User models with domain specific attributes and behavior.

    @param sender: the signal that invoked the function
    @param instance: the User object that was just created
    @param created: a boolean whether the object was created and not just updated
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)
        # Also make a token for user
        Token.objects.create(user=instance)

# Attach to the post_save signal.
post_save.connect(create_user_profile, sender=User)


class StudentGroup(models.Model):
    """
    Students may form a group that can make a submission together.
    """

    members = models.ManyToManyField(UserProfile, related_name="groups")
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=256)
    member_limit = models.PositiveIntegerField()
    is_public = models.BooleanField(default=False)
    invitation_key = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ['name']

    def get_names(self):
        return ", ".join(x.shortname for x in self.members.all())

    def has_space_left(self):
        return self.members.count() < self.member_limit

    def add_member(self, new_member):
        if self.members.count() >= self.member_limit or new_member in self.members.all():
            return False
        self.members.add(new_member)
        return True

    def __str__(self):
        return self.name
