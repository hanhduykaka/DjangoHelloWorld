from rest_framework import serializers
from .models import Topic ,Organization,Type
from django.contrib.auth.models import User 


class TopicSerializer(serializers.Serializer):
    id= serializers.IntegerField(read_only=True)
    top_name= serializers.CharField(max_length=100)

    def create(self,validated_data):
        return Topic.create(**validated_data)

    def update(self,instance,validated_data):
        instance.top_name= validated_data.get('top_name',instance.top_name)
        instance.save()
        return instance

    class Meta:

        model = Topic
        field = ('id','top_name')


class UserSerializer(serializers.ModelSerializer):
    
  class Meta:
    model=User
    fields = ('username','first_name','last_name','is_active','email','is_superuser',)
    read_only_fields = ('id',)

class TypeSerializer(serializers.ModelSerializer):
    
  class Meta:
    model=Type
    fields = ('id','Name',)
    read_only_fields = ('id',)
class OrganizationSerializer(serializers.ModelSerializer):  
    class Meta:
        model=Organization
        fields=('id','Name','Manager','Type','IsPublic','Purpose',)
        read_only_fields = ('id',)

    def to_representation(self, instance):
        self.fields['Manager'] =  UserSerializer(read_only=True)
        self.fields['Type']=TypeSerializer(read_only=True)
        return super(OrganizationSerializer, self).to_representation(instance)