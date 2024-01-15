from datetime import datetime

from rest_framework import serializers
from django.utils import timezone
from django.db import IntegrityError

from .. import models

import user.models


DAYS_OF_THE_WEEK = 7
WEEK_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def is_within_time(some_time, t1, t2):
    # Check if the t2 is before the t1 (crossing midnight)
    if t2 < t1:
        return some_time >= t1 or some_time <= t2
    else:
        # Check if the some_time is within the open hours
        return t1 <= some_time <= t2


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user.models.User
        exclude = ['password', 'last_login']


class ShopSearchSerializer(serializers.ModelSerializer):
    days_open = serializers.ListField(child=serializers.IntegerField(), help_text='must be an array. eg. [1,2,3] -> ["monday", "tuesday", "wednesday"], Note: an empty array means open every day')
    owner = UserSerializer(read_only=True, required=False)

    class Meta:
        model = models.Shop
        exclude = []
        extra_kwargs = {
            'open_hour': {'help_text': 'format is HH:MM[:ss[.uuuuuu]], eg. 21:25:00'},
            'close_hour': {'help_text': 'format is HH:MM[:ss[.uuuuuu]], eg. 21:25:00'},
            'is_manually_closed': {'help_text': 'the shop is closed manually'},
            # 'owner': {
            #     'read_only': True,
            #     'required': False
            # },
        }
    
    def to_representation(self, instance):
        request = self.context.get('request')
        representation = super().to_representation(instance)

        # this is to make owner read only
        # owner = UserSerializer(instance.owner)
        # representation['owner'] = owner.data
        
        # inteprete week days
        # The following code stole my sleep, thread with caution !!!
        days_open = representation['days_open']
        if days_open:
            days_open.sort()
            representation['week_days_open'] = [WEEK_DAYS[day_num-1] for day_num in days_open]
        else:
            representation['week_days_open'] = []

        
        current_datetime = timezone.localtime(timezone.now())
        current_time = current_datetime.time()
        current_weekday = current_datetime.strftime('%A').lower()
        representation['server_time'] = str(current_time)[:8]
        if representation['is_manually_closed']:
            representation['is_closed'] = True
        else:
            open_hour = representation['open_hour']
            close_hour = representation['close_hour']

            if current_weekday in representation['week_days_open']:
                if open_hour and close_hour:
                    time_format = '%H:%M:%S'
                    open_hour = datetime.strptime(open_hour, time_format).time()
                    close_hour = datetime.strptime(close_hour, time_format).time()
                    representation['is_closed'] = not is_within_time(current_time, open_hour, close_hour)   # if the current time is not within the time frame then shop is closed
                else:
                    representation['is_closed'] = False            # still not sure what to say if open_hour and close_hour is not set
            else:
                representation['is_closed'] = True



        return representation


    def validate_days_open(self, value):
        l = len(value)
        value = list(set(value))          # removing duplicates, I'll let you go this time without an error.
        if l > DAYS_OF_THE_WEEK:
            raise serializers.ValidationError(f"The size of the array should be <= 7 not {l}")
        if value and (max(value) > DAYS_OF_THE_WEEK or min(value) < 1):
            raise serializers.ValidationError("Invalid items in array only 1 to 7 allowed")

        return value
    

    def validate(self, data):
        open_hour = data.get('open_hour')
        close_hour = data.get('close_hour')
        e = lambda t: {'detail': str(t)}
        if (open_hour and not close_hour) or (not open_hour and close_hour):
            raise serializers.ValidationError(e('Set both open_hour and close_hour'))
        
        if open_hour and close_hour:
            if open_hour >= close_hour:
                raise serializers.ValidationError(e(f"open_hour must be less than close hour got open_hour={open_hour} close_hour={close_hour}"))
        return data


    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as ex:
            self.do_integrity_error(ex)

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as ex:
            self.do_integrity_error(ex)

    
    def do_integrity_error(self, ex):
        error_message = {"detail": str(ex)}
        if str(ex) == "UNIQUE constraint failed: ecommerce_shop.slug":
            error_message['detail'] = 'This Shop name already exists'
        raise serializers.ValidationError(error_message)
