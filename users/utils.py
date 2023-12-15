from users.models import UserFollows
from blog.models import Review, Ticket



def get_users_viewable_reviews(user):
    #https://stackoverflow.com/questions/55803243/cannot-query-object-must-be-user-instance
    #https://docs.djangoproject.com/fr/4.2/ref/models/querysets/ le __in est dedans cherche __in
    #Entry.objects.filter(id__in=[1, 3, 4]) example of this site en haut
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
    followed_users = list(followed_users) + [user.id]
    viewable_reviews = Review.objects.filter(user__in=followed_users)
    return viewable_reviews

def get_users_viewable_ticket(user):
    #https://stackoverflow.com/questions/55803243/cannot-query-object-must-be-user-instance
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
    followed_users = list(followed_users) + [user.id]
    viewable_tickets = Ticket.objects.filter(user__in=followed_users)
    return viewable_tickets