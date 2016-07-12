import io
import math
import tkinter

def getPathLength(lat1,lng1,lat2,lng2):
    '''calculates the distance between two lat, long coordinate pairs'''
    R = 6371000 # radius of earth in m
    lat1rads = math.radians(lat1)
    lat2rads = math.radians(lat2)
    deltaLat = math.radians((lat2-lat1))
    deltaLng = math.radians((lng2-lng1))
    a = math.sin(deltaLat/2) * math.sin(deltaLat/2) + math.cos(lat1rads) * math.cos(lat2rads) * math.sin(deltaLng/2) * math.sin(deltaLng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def getDestinationLatLong(lat,lng,azimuth,distance):
    '''returns the lat an long of destination point 
    given the start lat, long, aziuth, and distance'''
    R = 6378.1 #Radius of the Earth in km
    brng = math.radians(azimuth) #Bearing is degrees converted to radians.
    d = distance/1000 #Distance m converted to km
    lat1 = math.radians(lat) #Current dd lat point converted to radians
    lon1 = math.radians(lng) #Current dd long point converted to radians
    lat2 = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1)* math.sin(d/R)* math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d/R)* math.cos(lat1), math.cos(d/R)- math.sin(lat1)* math.sin(lat2))
    #convert back to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return[lat2, lon2]

def calculateBearing(lat1,lng1,lat2,lng2):
    '''calculates the azimuth in degrees from start point to end point'''
    startLat = math.radians(lat1)
    startLong = math.radians(lng1)
    endLat = math.radians(lat2)
    endLong = math.radians(lng2)
    dLong = endLong - startLong
    dPhi = math.log(math.tan(endLat/2.0+math.pi/4.0)/math.tan(startLat/2.0+math.pi/4.0))
    if abs(dLong) > math.pi:
         if dLong > 0.0:
             dLong = -(2.0 * math.pi - dLong)
         else:
             dLong = (2.0 * math.pi + dLong)
    bearing = (math.degrees(math.atan2(dLong, dPhi)) + 360.0) % 360.0;
    return bearing

def main(interval,azimuth,lat1,lng1,lat2,lng2):
    '''returns every coordinate pair inbetween two coordinate 
    pairs given the desired interval'''

    d = getPathLength(lat1,lng1,lat2,lng2)
    remainder, dist = math.modf((d / interval))
    counter = float(interval)
    coords = []
    coords.append([lat1,lng1])
    for distance in range(0,int(dist)):
        coord = getDestinationLatLong(lat1,lng1,azimuth,counter)
        counter = counter + float(interval)
        coords.append(coord)
    coords.append([lat2,lng2])
    return coords

def createGPX(lats,lons,latd,lond,movingspeed):
        #point interval in meters
        interval = movingspeed
        #direction of line in degrees
        #start point
        lat1 = lats
        lng1 = lons
##        lat1 = 28.586357
##        lng1 = 77.091970
        #end point
        lat2 = latd
        lng2 = lond
##        lat2 = 28.642085
##        lng2 = 77.106436
        azimuth = calculateBearing(lat1,lng1,lat2,lng2)
        print (azimuth)
        coords = main(interval,azimuth,lat1,lng1,lat2,lng2)
        stri=""
        stri+="<?xml version=\"1.0\"?>\n"
        stri+="<gpx version=\"1.1\" creator=\"Xcode\">"
        
        for x in coords[:]:
            stri+="\n\t<wpt lat="

            #lat="\""+"{0:.9f}".format(round(x[0],9))+"\""
            #stri+=lat

            #lon="\""+"{0:.9f}".format(round(x[1],9))+"\""
         

            lat="\""+str(x[0])+"\""
            stri+=lat

            lon="\""+str(x[1])+"\""        
     
            stri+=" lon="
            stri+=lon
            stri+="></wpt>"
           
        for num in range(1,1200):
            stri+="\n\t<wpt lat="

            lat="\""+str(latd)+"\""
            stri+=lat

            lon="\""+str(lond)+"\""        
     
            stri+=" lon="
            stri+=lon
            stri+="></wpt>"
        stri+="\n</gpx>"
        #print(stri)
        text_file = open("cycl.gpx", "w")
        text_file.write(stri)
        text_file.close()

def buttonClk(latsource,lonsource,latdest,londest,speed):
    lats=float(latsource.get())
    lons=float(lonsource.get())
    latd=float(latdest.get())
    lond=float(londest.get())
    movingspeed=float(speed.get())
    movingspeed=(movingspeed*1000)/3600
    createGPX(lats,lons,latd,lond,movingspeed)

    
if __name__ == "__main__":
    window=tkinter.Tk()
    window.title("GPX creator")
    window.geometry("500x500")
    
    lblentry1=tkinter.Label(window,text="Source Lat")
    latsource=tkinter.Entry(window)
    latsource.insert(tkinter.END,"28.586357")
    
    lblentry2=tkinter.Label(window,text="Source Lon")
    lonsource=tkinter.Entry(window)
    lonsource.insert(tkinter.END,"77.091970")

    lblentry3=tkinter.Label(window,text="Destination Lat")
    latdest=tkinter.Entry(window)
    latdest.insert(tkinter.END,"28.642085")
    
    lblentry4=tkinter.Label(window,text="Destination Lon")
    londest=tkinter.Entry(window)
    londest.insert(tkinter.END,"77.106436")

    lblentry5=tkinter.Label(window,text="Speed(km/hr)")
    speed=tkinter.Entry(window)
    speed.insert(tkinter.END,"24")

    btn=tkinter.Button(window,text="Create",command=lambda:buttonClk(latsource,lonsource,latdest,londest,speed))

    lblentry1.pack()
    latsource.pack()
    lblentry2.pack()
    lonsource.pack()

    lblentry3.pack()
    latdest.pack()
    lblentry4.pack()
    londest.pack()

    lblentry5.pack()
    speed.pack()
    
    btn.pack()
    
    window.mainloop()


   
    
     
        
