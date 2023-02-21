from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User,Post,Comment,LikedPost
from .serializers import verifier,postSerializer,UserSerializer,commentSerializer,LikedPostSerializer

from django.db.models import Q
@api_view(['POST'])
def verify(request):
    print(request.data['id'],"----------------------")
    serializer=verifier(data=request.data)
    if(serializer.is_valid()):
        try:
            user=User.objects.get(email=request.data['id'])
            user.is_verified=True
            user.is_active=True
            user.save()
            return Response({'status':"success"})
        except:
            return Response({'status':'User does not exist'})
    return Response(serializer.errors)

@api_view(['POST'])
def postItem(request):
    id=request.data["poster"]
    user=User.objects.get(id=id)
    serializer=postSerializer(data=request.data)
    print("-----------------",request.FILES)
    print("-----------------",request.data)
    print(user.is_authenticated)
    if(serializer.is_valid()):
        post=Post.objects.create(poster=user);
        post.caption=request.data["caption"]
        post.file=request.FILES.get('file')

        post.save()
        return Response({"status":"SUCCESS","data":serializer.data})
    return Response(serializer.errors)

@api_view(['GET'])
def getItem(request):
    posts=Post.objects.all().order_by('-created');
    serialiser=postSerializer(posts,many=True);
    return Response(serialiser.data)

@api_view(['GET'])
def getItemid(request,pk):
    try:
        post = Post.objects.get(id=pk)
        serializer = postSerializer(post)
        data = serializer.data
        return Response(serializer.data)
    except:
        return Response({"status": 404})

@api_view(['GET'])
def searchPost(request):
    query=request.GET.get('s')
    posts=''
    if(query=='top'):
        posts=Post.objects.all().order_by('-likes')
    elif(query=='new'):
        posts=Post.objects.all().order_by('-created')
    elif(query=='hot'):
        posts=Post.objects.all().order_by('-comments')
    else:
        posts=Post.objects.filter(
            Q(caption__icontains=query) |
            Q(poster__first_name__icontains=query)
        )
    data=postSerializer(posts,many=True)
    return Response(data.data)

@api_view(['GET'])
def getUser(request,pk):
    try:
        user=User.objects.get(id=pk)
        user_serializer = UserSerializer(user)
        all_posts = Post.objects.filter(poster=user)
        post_serializer = postSerializer(all_posts, many=True)
        
        data = {
            'user': user_serializer.data,
            'posts': post_serializer.data
        }
        
        return Response(data)
    except User.DoesNotExist:
       return Response({"status":404})

@api_view(['GET'])
def updateLike(request, pk):
    v = int(request.GET.get('v'))
    u = int(request.GET.get('u'))
    case=int(request.GET.get('c'))
    post = Post.objects.get(id=pk)
    user = User.objects.get(id=u)
    try:
        liked = LikedPost.objects.get(liked_by=user, liked_post=post)
    except:
        liked = LikedPost.objects.create(liked_by=user, liked_post=post)
    post.likes+=v
    post.save()
    if(case==1):
        liked.value=1
        liked.save()
        return Response({"status":"upVoted","likecount":post.likes})
    if(case==2 or case==5):
        liked.delete()
        return Response({"status":"unMarked","likecount":post.likes})
    if(case==3):
        liked.value=1
        liked.save()
        return Response({"status":"upVoted","likecount":post.likes})
    if(case==6):
        liked.value=-1
        liked.save()
        return Response({"status":"downVoted","likecount":post.likes})
    if(case==4):
        liked.value=-1
        liked.save()
        return Response({"status":"downVoted","likecount":post.likes})
    
@api_view(['GET'])
def getLike(request,pk):
    u = int(request.GET.get('u'))
    post = Post.objects.get(id=pk)
    user = User.objects.get(id=u)
    try:
        liked = LikedPost.objects.get(liked_by=user, liked_post=post)
        if(liked.value==1):
            return Response({"upToggled":True,"downToggled":False})
        elif(liked.value==-1):
            return Response({"upToggled":False,"downToggled":True})
        else:
            return Response("Error")
    except:
        return Response({"upToggled":False,"downToggled":False})

@api_view(['GET'])
def getComments(request):
        pid=int(request.GET.get('pid'))
        comments=Comment.objects.filter(comment_post__id=pid)
        serializer=commentSerializer(comments,many=True);
        data=serializer.data
        return Response(data)
    

@api_view(['POST'])
def addComment(request):
    user=User.objects.get(id=request.data["uid"])
    post=Post.objects.get(id=request.data["pid"])
    post.comments+=1
    post.save()
    text=request.data["text"]
    
    if(request.data["parent"] != None):
        parent=Comment.objects.get(id=request.data["parent"])
        newComment=Comment.objects.create(comment_post=post,commented_by=user,text=text,parent=parent)
    else:
        newComment=Comment.objects.create(comment_post=post,commented_by=user,text=text)
    newComment.save()
    return Response("Comment added")
