from typing import List

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests as res
import re
import redis
import json

redis_client=redis.Redis(host='localhost',port=63342,db=0)
@api_view(['GET'])
def sampleResponse(request, message):
    if message == 'ping':
        return Response({'data': 'pong'})
    else:

        return Response({'data': 'none'})



@api_view(['GET'])
def getWeatherInfo(request,scode,nocache):

    scode_string = '/' + scode.upper() + '.TXT'
    if nocache==0:
        data_dict=json.loads(redis.get(scode_string))
        return Response({'data': data_dict})
    elif nocache==1:

        url = 'https://tgftp.nws.noaa.gov/data/observations/metar/stations' \
            + scode_string
        result = res.get(url)
        data_list = result.text.split()

        data_string=" ".join(data_list)


        x = re.findall("\s\w+/\w+\s", data_string)
        raw_temprarture = x[-1].split("/")

        wind=re.findall("\w+KT\s", data_string)[0]

        if raw_temprarture[0][0] == 'M':
            temp_celcius = '-' + raw_temprarture[0] + ' C'
        else:
            temp_celcius = raw_temprarture[0] + ' C'
        if raw_temprarture[1][0] == 'M':
            temp_fahrenheit = '-' + raw_temprarture[1] + ' F'
        else:
            temp_fahrenheit = raw_temprarture[1] + ' F'

        data_dict = {
            'station': scode.upper(),
            'last_observation': data_list[0] + ' at ' + data_list[1] + ' GMT',
            'temperature': temp_celcius + ' (' + temp_fahrenheit + ')',
            'wind': wind,
            }
        redis_client.set(scode,json.dumps(data_dict))
        return Response({'data': data_dict})


