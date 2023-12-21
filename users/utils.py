from users.models import UserFollows, UserBlock
from blog.models import Review, Ticket
from django.db.models import CharField, Value
from itertools import chain
# il me manque les 

def get_users_viewable_reviews(user):
    #https://stackoverflow.com/questions/55803243/cannot-query-object-must-be-user-instance
    #https://docs.djangoproject.com/fr/4.2/ref/models/querysets/ le __in est dedans cherche __in
    #Entry.objects.filter(id__in=[1, 3, 4]) example of this site en haut
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
    followed_users = list(followed_users) + [user.id]
    blocked_user = UserBlock.objects.filter(user=user).values_list("blocked_user", flat=True)
    # print(blocked_user)
    viewable_reviews = Review.objects.filter(user__in=followed_users)
    #je recup mes ticket
    user_tickets = Ticket.objects.filter(user=user)
    #je recup les reviews concernant mon ticket pas dans les user que je follow et moi meme
    # si je bloque un user je verrai pas sa réponse a mon ticket, mais si lui me bloque je verrai quand meme sa réponse a mon ticket
    #je laisse comme sa pour pas buguer car sinon sa fairai un ticket deja répondu mais on pourrait rien voir donc un peu bizarre
    no_viewable_reviews = Review.objects.filter(ticket__in=user_tickets).exclude(user__in=followed_users).exclude(user__in=blocked_user)
    
    return viewable_reviews, no_viewable_reviews

def get_users_viewable_ticket(user):
    #https://stackoverflow.com/questions/55803243/cannot-query-object-must-be-user-instance
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
    followed_users = list(followed_users) + [user.id]
    viewable_tickets = Ticket.objects.filter(user__in=followed_users)
    return viewable_tickets