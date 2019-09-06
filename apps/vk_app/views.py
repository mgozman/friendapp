from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import *
import bcrypt
import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def index(request):
    if 'email' in request.session:
        user = users.objects.get(email = request.session['email'])
        return redirect('/' + str(user.id))
    else:    
        return render(request, "login_app/index.html")
        
def show_user_page(request, id):
    if 'email' in request.session:
        user = users.objects.get(id = id)
        user_session = users.objects.get(id = request.session['user_id'])
        context = {
            "user": user,
            "posts": Posts.objects.filter(user_where_posted = user).order_by("-updated_at"),
            "user_session": user_session,
            "pics": Images.objects.filter(user = user).order_by("-created_at")
        }
        return render(request, "login_app/result.html", context)
    else:
        return redirect('/')

def process(request):  
    context = users.objects.basic_validator_reg(request.POST)
    return JsonResponse(context)

def adduser(request):  
    context = users.objects.basic_validator_reg(request.POST)
    if len(context) > 0:
        return JsonResponse(context)

    pw = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = users.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw)
    request.session['email'] = user.email
    request.session['user_id'] = user.id
    user.online_status = True
    user.save()
    return JsonResponse({'success': True, 'user_id': user.id})

def login(request):
    context = users.objects.basic_validator_login(request.POST)
    if len(context) > 0:
        return JsonResponse(context)
    user = users.objects.get(email = request.POST['login'])

    if bcrypt.checkpw(request.POST['pw'].encode('utf-8'), user.password.encode('utf-8')):
        print("password match")
        request.session['email'] = user.email
        request.session['user_id'] = user.id
        user.online_status = True
        user.save()
        return JsonResponse({'success': True, 'user_id': user.id})
    else:
        print("failed password")
        return JsonResponse({'password_check': 'Wrong password'})
    
def logout(request):  
    user = users.objects.get(email = request.session['email'])
    user.online_status = False
    user.save()
    del request.session['email']
    del request.session['user_id']
    return redirect('/')

def update_profile(request):
    user = users.objects.get(email = request.session['email'])
    user.status = request.POST['status']
    user.city = request.POST['city']
    user.marrige = request.POST['marrige']
    user.phone = request.POST['phone']
    user.skype = request.POST['skype']
    user.school = request.POST['school']

    user.save()
    return JsonResponse({})

def post_process(request, id):
    user = users.objects.get(email = request.session['email'])
    user_where_to_post = users.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    if len(request.POST['post']) != 0:
        post = Posts.objects.create(post = request.POST['post'], user_who_created = user, user_where_posted = user_where_to_post)
    
    context = {
        "user": user_where_to_post,
        "posts": Posts.objects.filter(user_where_posted = user_where_to_post).order_by("-updated_at"),
        "user_session":user_session,
    }
    return render(request, 'login_app/partials_all_posts.html', context)

def comment_process(request, id):
    user = users.objects.get(email = request.session['email'])
    post = Posts.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    if len(request.POST['comment']) != 0:    
        comment = Comments.objects.create(comment = request.POST['comment'], post = post, user_who_created = user)
        print("COMMENT ", comment.user_who_created.first_name)
    
    context = {
        "user": post.user_where_posted,
        "posts": Posts.objects.all().filter(user_where_posted = post.user_where_posted).order_by("-updated_at"),
        "user_session" : user_session,
    }
    return render(request, 'login_app/partials_all_posts.html', context)

def post_delete(request, id):
    post = Posts.objects.get(id = id)
    user = post.user_where_posted
    comments = Comments.objects.filter(post = post)
    comments.delete()
    post.delete()
    user_session = users.objects.get(email = request.session['email'])
    context = {
        "user": user,
        "posts": Posts.objects.filter(user_where_posted = user).order_by("-updated_at"),
        "user_session" : user_session,
    }
    return render(request, 'login_app/partials_all_posts.html', context)

def delete_comment(request):
    comment = Comments.objects.get(id = request.POST['comment_id'])
    user = comment.post.user_where_posted
    comment.delete()
    context = {
        "user": user,
        "posts": Posts.objects.filter(user_where_posted = user).order_by("-updated_at"),
        "user_session": users.objects.get(email = request.session['email'])
    }
    return render(request, 'login_app/partials_all_posts.html', context)

def display_all_posts(request, id):
    user = users.objects.get(id = id)
    context = {
        "user": user,
        "posts": Posts.objects.filter(user_where_posted = user).order_by("-updated_at"),
        "user_session" :  users.objects.get(email = request.session['email'])
    }
    return render(request, 'login_app/partials_all_posts.html', context)

def display_my_posts(request, id):
    user = users.objects.get(id = id)
    context = {
        "user": user,
        "posts": Posts.objects.filter(user_where_posted = user, user_who_created = user).order_by("-updated_at"),
        "user_session" :  users.objects.get(email = request.session['email'])
    }
    return render(request, 'login_app/partials_all_posts.html', context)

def like_post(request):
    user = users.objects.get(email = request.session['email'])
    post = Posts.objects.get(id = request.POST['post_id'])
    if user in post.users_who_liked.all():
        post.users_who_liked.remove(user)
        user.liked_posts.remove(post)
    else:
        post.users_who_liked.add(user)
        user.liked_posts.add(post)

    user = post.user_where_posted
    context = {
        "user": user,
        "posts": Posts.objects.filter(user_where_posted = user).order_by("-updated_at"),
        "user_session":  users.objects.get(email = request.session['email'])
    }
    return render(request, 'login_app/partials_all_posts.html', context)

def like_comment(request):
    user = users.objects.get(email = request.session['email'])
    comment = Comments.objects.get(id = request.POST['comment_id'])
    if user in comment.users_who_liked.all():
        comment.users_who_liked.remove(user)
        user.liked_comments.remove(comment)
    else:
        comment.users_who_liked.add(user)
        user.liked_comments.add(post)
    user = comment.post.user_where_posted
    context = {
        "user": user,
        "posts": Posts.objects.filter(user_where_posted = user).order_by("-updated_at"),
        "user_session" :  users.objects.get(email = request.session['email'])
    }
    return render(request, 'login_app/partials_all_posts.html', context)

def friends_delete_online(request,  id):
    user1 = users.objects.get(id = request.session['user_id'])
    user2 = users.objects.get(id = id)

    user1.friends.remove(user2)
    user2.friends.remove(user1)

    context = {
        "user": user1,
    }
    return render(request, 'login_app/partials_online_friends.html', context)

def friends_delete(request,  id):
    user1 = users.objects.get(id = request.session['user_id'])
    user2 = users.objects.get(id = id)

    user1.friends.remove(user2)
    user2.friends.remove(user1)

    context = {
        "user": user1,
    }
    return render(request, 'login_app/partials_friends.html', context)

def friends_online(request, id):
    print('ALL GOOD')
    user = users.objects.get(id = id)
    context = {
        "user" : user,
        "friends" : user.friends.filter(online_status = True)
    }
    print("ONLINE ")
    return render(request, 'login_app/partials_online_friends.html', context)

def add_to_friend(request, id):
    user = users.objects.get(email = request.session['email'])
    friend = users.objects.get(id = id)
    user.friends.add(friend)
    friend.friends.add(user)
    return redirect('/' + str(user.id) + '/friends_others')

def friends_others(request, id):
    user = users.objects.get(id = id)
    others = list(set(users.objects.all()) - set(user.friends.all()) - set([user]))
    context = {
        "user" : user,
        "friends" : others
    }
    return render(request, 'login_app/partials_not_friends.html', context)

def display_all_friends(request, id):
    user = users.objects.get(id = id)
    user_session = users.objects.get(id = request.session['user_id'])
    return render(request, 'login_app/display_all_friends.html', {'user':user, 'user_session':user_session})

def friends_process(request, id):
    user = users.objects.get(id = id)
    return render(request, 'login_app/partials_friends.html', {'user':user})

def profile_pic(request):
    if request.method == 'POST':
        print("FIILEES ", request.FILES['fileToUpload'])
        user = users.objects.get(id = request.session['user_id'])
        user.profile_image = request.FILES['fileToUpload']
        user.save()
    return JsonResponse({"url" : user.profile_image.url})

def group_pic(request, id):
    print("ALL GOOD")
    if request.method == 'POST':
        group = Groups.objects.get(id = request.POST['group_id'])
        group.profile_image = request.FILES['fileToUploadGroup']
        group.save()
        print("USER NAME ", group.profile_image.name)
        print("USER PATH ", group.profile_image.path)
        print("USER URL ", group.profile_image.url)
        
    return JsonResponse({"url" : group.profile_image.url})

def display_messages(request, id):
    user = users.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    message_from = Messages.objects.filter(user_from = user).order_by("-created_at")
    message_to = Messages.objects.filter(user_to = user).order_by("-created_at")
    messages = message_from | message_to
    return render(request, 'login_app/display_messages.html', {"messages":messages, "user":user, "user_session":user_session})

def send_messages(request, id):
    #to mark messages as read
    user_from = users.objects.get(id = request.session['user_id'])
    user_to = users.objects.get(id = request.POST['friend_id'])
    messages = Messages.objects.filter(user_from = user_to).filter(user_to = user_from)
    messages.update(was_read = True)

    my_messages = Messages.objects.filter(user_from__in=[user_from, user_to]).filter(user_to__in=[user_from, user_to]).order_by("created_at")
    return render(request, 'login_app/partials_send_message.html', {'user_from':user_from, 'user_to':user_to, "messages":my_messages})

def new_message(request, id):
    user_from = users.objects.get(id = request.session['user_id'])
    user_to = users.objects.get(id = request.POST['friend_id'])
    if request.POST['message'] != '':
        message = Messages.objects.create(message = request.POST['message'], user_from = user_from, user_to = user_to)
        print("Here ", message.message)
    
    my_messages = Messages.objects.filter(user_from__in=[user_from, user_to]).filter(user_to__in=[user_from, user_to]).order_by("created_at")
    return render(request, 'login_app/partials_send_message.html', {'user_from':user_from, 'user_to':user_to, "messages":my_messages})

def check_new_message(request):
    print("I am here")
    user = users.objects.get(email = request.session['email'])
    print('USER ID ', user.first_name)
    messages = Messages.objects.filter(user_to = user, was_read = False)
    print("NEW ", messages)
    return JsonResponse({'new_mess': len(messages)})

def display_groups(request, id):
    user = users.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    my_groups = user.my_groups.all()
    return render(request, 'login_app/display_groups.html', {'user':user, 'user_session':user_session, 'my_groups':my_groups})

def display_my_groups(request, id):
    user = users.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    my_groups = user_session.my_groups.all()
    return render(request, 'login_app/partials_display_groups.html', {'user':user, 'user_session':user_session, 'my_groups':my_groups})

def display_admin_groups(request, id):
    user = users.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    my_groups = user.created_groups.all()
    return render(request, 'login_app/partials_display_groups.html', {'user':user, 'user_session':user_session, 'my_groups':my_groups})

def display_other_groups(request, id):
    user = users.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    all_groups = Groups.objects.all()
    user_groups = user.my_groups.all()

    other_groups = list(set(all_groups) - set(user_groups))
    return render(request, 'login_app/partials_display_groups.html', {'user':user, 'user_session':user_session, 'my_groups':other_groups})

def create_group(request, id):
    user = users.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    group = Groups.objects.create(user_who_created = user_session)
    group.users.add(user_session)
    user_session.my_groups.add(group)
    print("GROUP ", group.title)
    return redirect('/' + str(id) + '/display_group/' + str(group.id))

def display_group(request, id, id_group):
    user = users.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    group = Groups.objects.get(id = id_group)
    print("GROUP ", group.title)
    print("DESC ", group.desc)
    return render(request, 'login_app/display_group.html', {'user':user, 'user_session':user_session, "group":group})

def update_title(request, id):
    user = users.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    group = Groups.objects.get(id = request.POST['group_id'])
    group.title = request.POST['title']
    group.save()
    return JsonResponse({})

def update_desc(request, id):
    user = users.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    group = Groups.objects.get(id = request.POST['group_id'])
    group.desc = request.POST['desc']
    group.save()
    return JsonResponse({})

def delete_group(request, id):
    print("DElete group")
    user = users.objects.get(email = request.session['email'])
    group = Groups.objects.get(id = id)

    user.my_groups.remove(group)
    group.delete()

    user_session = users.objects.get(email = request.session['email'])
    my_groups = user_session.created_groups.all()
    return render(request, 'login_app/partials_display_groups.html', {'user':user, 'user_session':user_session, 'my_groups':my_groups})

def follow_group(request, id, group_id):
    print("Follow group")
    user = users.objects.get(id = id)
    group = Groups.objects.get(id = group_id)
    user_session = users.objects.get(email = request.session['email'])

    user.my_groups.add(group)
    group.users.add(user)

    all_groups = Groups.objects.all()
    user_groups = user.my_groups.all()

    other_groups = list(set(all_groups) - set(user_groups))
    return render(request, 'login_app/partials_display_groups.html', {'user':user, 'user_session':user_session, 'my_groups':other_groups})

def unfollow_group(request, id, group_id):
    print("Follow group")
    user = users.objects.get(id = id)
    group = Groups.objects.get(id = group_id)
    user_session = users.objects.get(email = request.session['email'])

    user.my_groups.remove(group)
    group.users.remove(user)

    all_groups = Groups.objects.all()
    user_groups = user.my_groups.all()

    my_groups = user_session.my_groups.all()
    return render(request, 'login_app/partials_display_groups.html', {'user':user, 'user_session':user_session, 'my_groups':my_groups})

def followGroup(request, id, group_id):
    print("Follow group")
    user = users.objects.get(id = id)
    group = Groups.objects.get(id = group_id)
    user_session = users.objects.get(email = request.session['email'])

    user.my_groups.add(group)
    group.users.add(user)

    all_groups = Groups.objects.all()
    user_groups = user.my_groups.all()

    return render(request, 'login_app/display_group.html', {'user':user, 'user_session':user_session, "group":group})

def unfollowGroup(request, id, group_id):
    print("Follow group")
    user = users.objects.get(id = id)
    group = Groups.objects.get(id = group_id)
    user_session = users.objects.get(email = request.session['email'])

    user.my_groups.remove(group)
    group.users.remove(user)

    all_groups = Groups.objects.all()
    user_groups = user.my_groups.all()
    return render(request, 'login_app/display_group.html', {'user':user, 'user_session':user_session, "group":group})

def my_pic(request):
    if request.method == 'POST':
        user = users.objects.get(id = request.session['user_id'])
        image = Images.objects.create(user = user, image = request.FILES['myFileToUpload'])
        images = Images.objects.filter(user = user).order_by("-created_at")
    return render(request, 'login_app/partials_my_pics.html', {'pics':images})

def more_pic_upload(request, id):
    if request.method == 'POST':
        user = users.objects.get(id = request.session['user_id'])
        image = Images.objects.create(user = user, image = request.FILES['moreFileToUpload'])
        images = Images.objects.filter(user = user).order_by("-created_at")
        user_session = users.objects.get(email = request.session['email'])
    return render(request, 'login_app/partials_display_pics.html', {'user':user, 'pics':images, 'user_session':user_session})

def display_user_pics(request, id):
    user = users.objects.get(id = id)
    user_session = users.objects.get(email = request.session['email'])
    print("USER SESSION ", user_session.first_name)
    pics = user.images.all().order_by("-created_at")
    return render(request, 'login_app/display_pics.html', {'user':user, 'pics':pics, 'user_session':user_session})

def delete_pic(request, id, id_pic):
    print("all GOOD")
    user = users.objects.get(id = id)
    pic = Images.objects.get(id = id_pic)
    print("I GOR USER AND PIC")
    pic.delete()
    pics = user.images.all().order_by("-created_at")
    user_session = users.objects.get(email = request.session['email'])
    return render(request, 'login_app/partials_display_pics.html', {'user':user, 'pics':pics})