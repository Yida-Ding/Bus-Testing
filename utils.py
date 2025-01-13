import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import math
import os
import time
import shutil
import requests

"""
高德的数据应该是GCJ02, OSM地图是WGS84
"""

def deg2num(lng_deg, lat_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lng_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lng_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lng_deg, lat_deg)

def download_mapfile(minlng, minlat, maxlng, maxlat, direname, mapfile):
    """
    mapfile: e.g., 'beijing.png'
    """
    smurl = "http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"

    zoom = 18
    while True:
        xmintile, ymaxtile = deg2num(minlng, minlat, zoom)
        xmaxtile, ymintile = deg2num(maxlng, maxlat, zoom)
        if (xmaxtile + 1 - xmintile) * (ymaxtile + 1 - ymintile) <= 50:
            break
        zoom -= 1
    
    newminlng, newminlat = num2deg(xmintile, ymaxtile + 1, zoom)
    newmaxlng, newmaxlat = num2deg(xmaxtile + 1, ymintile, zoom)

    tmpfolder = Path(f"./{direname}/OSMTiles/{zoom}")
    if not os.path.exists(f"./{direname}/OSMTiles"):
        os.mkdir(f"./{direname}/OSMTiles")
    if not os.path.exists(tmpfolder):
        os.mkdir(tmpfolder)
    n_error_count = 0

    errorinfo = 0
    session = requests.Session()
    while True:
        try:
            for xtile in range(xmintile, xmaxtile+1):
                for ytile in range(ymintile,  ymaxtile+1):
                    if not os.path.exists(tmpfolder/(f"{xtile}")):
                        os.mkdir(tmpfolder/(f"{xtile}"))

                    tmptilefile = tmpfolder/(f"{xtile}")/(f"{xtile}_{ytile}_{zoom}.png")
                    if os.path.exists(tmptilefile): continue     
                    imgurl=smurl.format(zoom, xtile, ytile)
                    print("Downloading image tiles: " + imgurl)
                    headers = {
                        # "Host": "artodb-basemaps-a.global.ssl.fastly.net",
                        #"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"
                        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42",
                        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
                    }
                    # req = requests.get(imgurl, stream = True, headers=headers)
                    req = session.get(imgurl, stream = True, headers=headers)
                    with open(tmptilefile, 'wb') as fp:
                        req.raw.decode_content = True
                        shutil.copyfileobj(req.raw, fp) 
            break   
        except Exception as e:
            print(e)
            print("Downloading error, sleeping 5 minutes")
            time.sleep(60 * 5)
            if n_error_count > 5:
                print("The map file cannot be downloaded now, please try draw image without map")
                errorinfo = 1
                break
            n_error_count += 1

    session.close()

    if errorinfo == 0:
        # print("Join the tiles to final image")
        list_rows = []
        for xtile in range(xmintile, xmaxtile + 1):
            list_columns = []
            for ytile in range(ymintile,  ymaxtile + 1):
                # print(xtile, ytile, zoom)
                arr = plt.imread(tmpfolder/(f"{xtile}")/(f"{xtile}_{ytile}_{zoom}.png"))
                list_columns.append(arr)
            list_rows.append(np.vstack(list_columns))
        finarr = np.hstack(list_rows)
        plt.imsave("./%s/"%direname + mapfile, finarr)

    # print("Success")
    return (newminlng, newminlat, newmaxlng, newmaxlat)   


def plot_on_basemap(direname, mapfile, extent, dpi=200, alpha=0.8):
    if not os.path.exists(direname):
        os.makedirs(direname)

    extent = download_mapfile(*extent, direname, mapfile)
    whration = (extent[2] - extent[0]) / (extent[3] - extent[1])
    fig, ax = plt.subplots(1, 1, figsize = (10, 10 * whration), dpi=dpi)
    ax.imshow(plt.imread(direname+"/"+mapfile), extent = (extent[0], extent[2], extent[1], extent[3]),alpha=alpha)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    return fig, ax



"""
高德坐标要用这个函数转成OSM坐标
"""

def trans_coord(lng, lat):
    """
    GCJ02(火星坐标系)转WGS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    ee = 0.00669342162296594323  # 偏心率平方
    a = 6378245.0  # 长半轴
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return lng * 2 - mglng, lat * 2 - mglat


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 *
            math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 *
            math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
    return ret

def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * math.pi) + 40.0 *
            math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 *
            math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
    return ret

def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

def transform_xs_ys(xs, ys, pair=True):
    nxs, nys = [], []
    for i in range(len(xs)):
        lon, lat = trans_coord(xs[i], ys[i])
        nxs.append(lon)
        nys.append(lat)
    if pair:
        return [[nxs[i], nys[i]] for i in range(len(nxs))]
    else:
        return nxs, nys

def transform_stops(coords):
    ncoords = []
    for coord in coords:
        lon, lat = trans_coord(coord[0], coord[1])
        ncoords.append([lon, lat])
    return ncoords

def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return gg_lng, gg_lat
