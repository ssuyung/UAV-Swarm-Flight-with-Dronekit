from datetime import datetime
height_float = 3.57
formatted_height = f"{height_float:06.2f}"

lat = 24.732647
lon = 120.23138773
height = 23.23213
current_time = datetime.now().strftime("%M%S")    # This will turn the time into minute and second format, something like 0835 (08:35)
assert(lat/100 < 1 and lat/10 >= 1)
assert(lon/1000 < 1 and lon/100 >= 1)
assert(height/100 < 1)
TCP_msg = str("{:011.8f}".format(lat)) + str("{:012.8f}".format(lon)) + str("{:06.2f}".format(height)) + str(current_time)


str_msg = TCP_msg
print(str_msg)
lat = float(str_msg[0:11])
lon = float(str_msg[11:23])
alt = float(str_msg[23:29])
recvTime = int(str_msg[31:33])
print(lat, lon, alt, recvTime)