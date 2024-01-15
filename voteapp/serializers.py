from rest_framework import serializers

from . import models


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vote
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True)
    vote_count = serializers.IntegerField(required=False)

    class Meta:
        model = models.Choice
        fields = '__all__'
    

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        if self.instance:
            if self.many:
                queryset = self.instance
                vote_count = sum([instance.votes.count() for instance in queryset])
            else:
                vote_count = self.instance.votes.count()
            
            self['vote_count'].value = vote_count


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    no_votes = serializers.IntegerField(required=False) #not in model

    class Meta:
        model = models.Poll
        fields = '__all__'
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     if self.instance:
    #         no_votes = self.instance.votes.count()
    #         self['no_votes'].value = no_votes

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'