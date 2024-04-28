from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import pickle
import pandas as pd
import numpy as np
import os

def use_model(brand,type_,ram,gpu,os_,weight,touchscreen,ips_panel,sc_size,resol,processor,hdd,ssd):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_pipe_path =  os.path.join(base_dir,'data','model_pipe.pkl')
    model_pipe = pickle.load(open(model_pipe_path,'rb'))
    ram = int(ram)
    hdd = int(hdd)
    ssd = int(ssd)
    weight = float(weight)
    sc_size = float(sc_size)
    if ips_panel == 'Yes':
        ips_panel = 1
    else:
        ips_panel = 0

    if touchscreen == 'Yes':
        touchscreen = 1
    else:
        touchscreen = 0
    
    # calculating the ppi
    res = resol.split('x')
    x = int(res[0])
    y = int(res[1])
    ppi = (((x**2 + y**2)**0.5) / sc_size)
    my_query = [np.array([brand,type_,ram,gpu,os_,weight,touchscreen,ips_panel,ppi,processor,hdd,ssd])]
    ans = int(np.exp(model_pipe.predict(my_query)[0])*(3.34058)) 
    return ans

def predict(request):
    regressedPrice = 0
    if request.method == "POST":
        data = request.POST
        brand = data['brand_name']
        type = data['type']
        ram = data['ram']
        gpu  = data['gpu']
        os_ = data['os']
        weight = data['weight']
        ts = data['touchscreen']
        ips = data['ips_panel']
        screen_size = data['screen_size']
        resolution = data['resolution']
        processor = data['processor']
        hdd = data['hdd']
        ssd = data['ssd']

        regressedPrice = use_model(brand,type,ram,gpu,os_,weight,ts,ips,
                                   screen_size,resolution,processor,hdd,ssd)
        print(regressedPrice)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir,'data','dataset.pkl')
    df = pickle.load(open(dataset_path,'rb'))

    context = {
        'Brands' : df['Company'].unique(),
        'Types'   : df['TypeName'].unique(),
        'Rams'    : [2,4,6,8,12,16,24,32,64],
        'GPUS'    : df['Gpu'].unique(),
        'OSES'     : df['OpSys'].unique(),
        'Resolutions': ["1366 x 768","1600 x 900","1920 x 1080","2304 x 1440","2560 x 1440","2560 x 1600","2880 x 1800","3000 x 2000","3200 x 1800","3840 x 2160"],
        'Processors': df['Processor'].unique(),
        'HDDS': [0,128,256,512,1024,2048],
        'SSDS': [0,128,256,512,1024,2048],
        'regressedPrice' : regressedPrice
    }
    return render(request,'predictor/predictor.html',context=context)