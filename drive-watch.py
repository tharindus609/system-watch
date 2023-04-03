import subprocess
import json


def convert_to_terabytes(byte_value):
    if len(str(byte_value)) > 12:
        return "{0} T".format(round(byte_value/1024**4, 2))
    else:
        return "{0} G".format(round(byte_value/1024**3, 2))

result = subprocess.run(["smartctl", "--json", "--scan"], capture_output=True)

device_list = json.loads(result.stdout)['devices']

for device in device_list:
    print("Checking Device: {0}".format(device['name']))
    smart_json_data = subprocess.run(["smartctl", "--json", "--all", "{0}".format(device['name'])], capture_output=True)
    smart_data = json.loads(smart_json_data.stdout)
    try:
        print("Device model: {0} ({1})".format(smart_data['model_family'], smart_data['model_name']))
    except KeyError as ex:
        print("Device model: {0}".format(smart_data['model_name']))
        
    print("Device serial: {0}".format(smart_data['serial_number']))
    print("Device capacity: {0}".format(convert_to_terabytes(smart_data['user_capacity']['bytes']), 2))
    print("Device temperature: {0} C".format(smart_data['temperature']['current']))
    print("Smart check status: {0}".format("PASS" if bool(smart_data['smart_status']['passed']) else "FAIL"))

    print("Reading SMART data")
    for attribute in smart_data['ata_smart_attributes']['table']:
        if attribute['id'] == 3: # Spin_Up_Time
            attribute['raw']['value'] = "{0} ms".format(round(attribute['raw']['value']/1000,2))
        # elif attribute['id'] in (241, 242): # Total_LBAs_Written/Read
        #     attribute['raw']['value'] = "{0}".format(round((attribute['raw']['value']*512)/1024**3,2))
        
        if attribute['id'] in (1,2,5,):
            print("ID {0} {1}: {2}/{3}".format(attribute['id'], attribute['name'], attribute['raw']['value'], attribute['thresh']))
        else:
            print("ID {0} {1}: {2}".format(attribute['id'], attribute['name'], attribute['raw']['value']))
    print("---")
