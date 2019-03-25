from rest_framework import serializers
from .models import Topic 

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