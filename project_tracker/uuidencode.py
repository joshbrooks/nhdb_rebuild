import base64, uuid, bitstring


def base64_to_uuid(b64str):
    """Credit to tpatja http://stackoverflow.com/questions/23515237/decoding-base64-guid-in-python"""
    b64str += '=='
    bytes = base64.urlsafe_b64decode(b64str)
    array = bitstring.BitArray(bytes = bytes)
    hex = array.hex
    return '-'.join([hex[:8], hex[8:12], hex[12:16], hex[16:20], hex[20:]])


def uuid_to_base64(uuid_instance):
    bytes = uuid_instance.bytes
    return base64.urlsafe_b64encode(bytes).strip('==')

if __name__ == '__main__':

    ofile = open('test_uuids.json', 'w')
    import json

    results = []


    for loop_id  in range(0,1000):
        i = uuid.uuid4()
        i64 = uuid_to_base64(i)
        _i = base64_to_uuid(i64)
        results.append(
            {'input':str(i) ,
             'shortform': uuid_to_base64(i),
             'python_reproduce': base64_to_uuid(i64)
             }
        )

    ofile.write(json.dumps(results, indent=1))