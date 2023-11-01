from datetime import datetime
height_float = 3.57
formatted_height = f"{height_float:06.2f}"
current_time = datetime.now().strftime("%M%S")    # This will turn the time into minute and second format, something like 0835 (08:35)

latitude = 24.732647
longitude = 120.23138773
TCP_msg = str("{:011.8f}".format(latitude)) + str("{:012.8f}".format(longitude)) \
                +  str(formatted_height) + str(current_time)


str_msg = TCP_msg
print(str_msg)
lat = float(str_msg[0:11])
lon = float(str_msg[11:23])
alt = float(str_msg[23:29])
recvTime = int(str_msg[29:])
print(lat, lon, alt, recvTime)