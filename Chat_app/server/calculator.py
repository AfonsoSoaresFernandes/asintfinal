from math import radians, cos, sin, asin, sqrt

def findDistance(lat1 ,lng1, lat2, lng2):
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371

    dist = c*r*1000
    return dist

def in_building(esq,dir,cima,baixo, lat,lng):
    if lat>baixo and lat<cima and lng>esq and lng<dir:
        return True
    else:
        return False
