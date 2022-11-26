import base64


def read_base64_file(file_name):
    with open(file_name, 'rb') as infile:
        encoded_data = infile.read()
        data = base64.decodebytes(encoded_data)
        data = data.decode('UTF-8')
        return data
