from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests as res
import json
@api_view(['GET'])
def index(request,message):
    if message=='ping':
        return Response({'data': 'pong'})
    else:
        return Response({"data":"none"})

@api_view(['GET'])
def getweatherinfo(request,scode):
    scode='/'+scode.upper()+'.TXT'
    url='https://tgftp.nws.noaa.gov/data/observations/metar/stations'+scode
    print(url)
    d=res.get(url)
    datalist=d.text.split()
    temp=datalist[8].split('/')
    if temp[0][0]=='M':
        temp1='-'+temp[0]+'C'
    else:
        temp1=temp[0]+'C'
    if temp[1][0]=='M':
        temp2='-'+temp[1]+"F"
    else:
        temp2=temp[1]+"F"
    data1={'station':datalist[2],
          'last_observation':datalist[0]+' at '+datalist[1]+' GMT',
          'temperature':temp1+' ('+temp2+')',
          'wind':datalist[3]
          }

    return Response({'data':data1})







