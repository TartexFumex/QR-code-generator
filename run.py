import configparser
from qrcode_generator import Shape, draw_qr_code, url_to_qr_matrix

# Lecture du fichier de configuration
config = configparser.ConfigParser()
config.read('configuration.conf')

url = config.get('QR_CODE', 'URL')
color = config.get('QR_CODE', 'color')
pixel_size = config.getint('QR_CODE', 'pixel_size')
shape = Shape.SQUARE if config.get('QR_CODE', 'shape') == 'SQUARE' else Shape.ELLIPSE
error_correction = config.get('QR_CODE', 'error_correction')

border_size = config.getint('BORDER', 'size')
border_color = config.get('BORDER', 'color')
border_radius = config.getint('BORDER', 'radius')
border_padding = config.getint('BORDER', 'padding')

text = config.get('TEXT', 'content')
text_color = config.get('TEXT', 'color')
text_size = config.getint('TEXT', 'size')
text_background_color = config.get('TEXT', 'background_color')
text_background_radius = config.getint('TEXT', 'background_radius')
text_background_padding = config.getint('TEXT', 'background_padding')

image_path = config.get('IMAGE', 'path')
image_percent = config.getfloat('IMAGE', 'percent')

marge = config.getint('MISC', 'marge')
background_color = config.get('MISC', 'background_color')

file_name_output = config.get('OUTPUT', 'file_name_output')


# Génération du QR code
matrix = url_to_qr_matrix(url, error_correction)

qr_img = draw_qr_code(matrix, 
                        color=color, 
                        pixel_size=pixel_size, 
                        shape=shape, 
                        border_size=border_size, 
                        border_color=border_color, 
                        border_radius=border_radius, 
                        border_padding=border_padding, 
                        text=text, 
                        text_color=text_color, 
                        text_size=text_size, 
                        text_background_color=text_background_color, 
                        text_background_radius=text_background_radius, 
                        text_background_padding=text_background_padding, 
                        image_path=image_path, 
                        image_percent=image_percent,
                        marge=marge, 
                        background_color=background_color)

if file_name_output is None or file_name_output == '':
    file_name_output = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(".", "_") + '.png'
    print(file_name_output)
    
qr_img.save(file_name_output)
