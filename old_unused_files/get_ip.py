import subprocess
def get_ip_address_and_base_or_rover():
    try:
        result = subprocess.check_output(["hostname", "-I"]).decode("utf-8")
        ip_address = result.split()[0]  # Extracting the first IP address in case there are multiple
    except Exception as e:
        print("Could not retrieve IP address: ", e)
        ip_address = "Not Found"
    if(ip_address == '172.20.10.8'):
        return '172.20.10.8', "base"
    elif(ip_address == '172.20.10.9'):
        return '172.20.10.8', "rover"
    elif(ip_address == '192.168.94.226'):
        return '192.168.94.226', "base"
    elif(ip_address == '192.168.94.147'):
        return '192.168.94.226', "rover"
    else: 
        print("-------ERROR--------")
        print("Detect ip is", ip_address)
    '''ip_address is str type'''
    return ip_address