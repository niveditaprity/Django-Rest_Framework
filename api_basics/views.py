from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
# Create your views here.

#create GenericViwsets
class ArticleViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
# Create Viewsets

# class ArticleViewSet(viewsets.ViewSet):
    #def list(self,request):
       # artcles = Article.objects.all()
        #serializer = ArticleSerializer(artcles, many=True)
        #return Response(serializer.data)
    #def create(self,request):
     #   serializer = ArticleSerializer(data=request.data)

       # if serializer.is_valid():
         #   serializer.save()
         #   return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #def retrieve(self,request,pk=None):
       # queryset=Article.objects.all()
       # article = get_object_or_404(queryset,pk=pk)
       # serializer = ArticleSerializer(article)
       # return Response(serializer.data)








#generic View

class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = id
    # Authentication
    #authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)
    def put(self,request,id=None):
        return self.update(request,id)













class ArticleAPIView(APIView):
    def get(self,request):
        artcles= Article.objects.all()
        serializer =ArticleSerializer(artcles,many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ArticleDetails(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return  HttpResponse(status=status.HTTP_404_NOT_FOUND)
    def get(self,request,id):
        article=self.get_object(id)
        serializer=ArticleSerializer(article)
        return Response(serializer.data)
    def put(self,request,id):
        article=self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        article=self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









#@csrf_exempt
@api_view(['GET','POST'])
def article_list(request):
    if request.method == 'GET':
        articles =Article.objects.all()
        serializer = ArticleSerializer(articles,many=True)
        #return JsonResponse(serializer.data,safe=False)
        return Response(serializer.data)
    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk):
    try:
        article =Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method =='PUT':
        #data=JSONParser().parse(request)
        serializer = ArticleSerializer(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



