from PIL import Image
import PIL.ExifTags as ExifTags
import folium

def get_gps(fname):
    im = Image.open(fname)
    
    exif = {
        ExifTags.TAGS[k]: v
        for k, v in im._getexif().items()
        if k in ExifTags.TAGS 
    }

    gps_tags = exif["GPSInfo"]
    gps = {
        ExifTags.GPSTAGS.get(t,t): gps_tags[t]
        for t in gps_tags
    }

    def conv_deg(v):
        d = float(v[0][0]) / float(v[0][1])
        m = float(v[1][0]) / float(v[1][1])
        s = float(v[2][0]) / float(v[2][1])
        return d + (m / 60.0) + (s / 3600.0)
    lat = conv_deg(gps["GPSLatitude"])
    lat_ref = gps["GPSLatitudeRef"]
    if lat_ref != "N": lat = 0 - lat 
    
    lon = conv_deg(gps["GPSLongitude"])
    lon_ref = gps["GPSLongitudeRef"]
    if lon_ref !="E": lon = 0 - lon 
    
    return lat, lon  

if __name__ == "__main__":
    lat, lon = get_gps("gpsimg.jpg")
    print(lat,lon)

    def get_datetime(img):
        exif = img._getexif()
        for id, val in exif.items():
            if id == 36867:
                return val
        return ''

im = Image.open("gpsimg.jpg")
datetime = get_datetime(img)
print(datetime)


map = folium.Map(location=[lat, lon],zoom_start=18)
folium.Marker(location=[lat, lon],popup=datetime).add_to(map)

map.save("map_img.html")
