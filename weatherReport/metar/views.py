from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests as res
import json


@api_view(['GET'])
def index(request, message):
    if message == 'ping':
        return Response({'data': 'pong'})
    else:
        return Response({'data': 'none'})


@api_view(['GET'])
def getweatherinfo(request, scode):

    scode = '/' + scode.upper() + '.TXT'
    url = 'https://tgftp.nws.noaa.gov/data/observations/metar/stations' \
        + scode
    result = res.get(url)
    data_list = result.text.split()
    raw_temprarture = data_list[8].split('/')
    if raw_temprarture[0][0] == 'M':
        temp_celcius = '-' + raw_temprarture[0] + ' C'
    else:
        temp_celcius = raw_temprarture[0] + ' C'
    if raw_temprarture[1][0] == 'M':
        temp_fahrenheit = '-' + raw_temprarture[1] + ' F'
    else:
        temp_fahrenheit = raw_temprarture[1] + ' F'

    data_dict = {
        'station': data_list[2],
        'last_observation': data_list[0] + ' at ' + data_list[1] \
            + ' GMT',
        'temperature': temp_celcius + ' (' + temp_fahrenheit + ')',
        'wind': data_list[3],
        }

    return Response({'data': data_dict})
