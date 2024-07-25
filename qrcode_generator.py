from PIL import Image, ImageDraw, ImageFont
from enum import Enum
import qrcode
import numpy as np

class Shape(Enum):
    SQUARE = 'square'
    ROUND = 'round'
    ELLIPSE = 'ellipse'

def url_to_qr_matrix(url, error_correction:str='M'):
    match error_correction:
        case 'L':
            e = qrcode.constants.ERROR_CORRECT_L
        case 'M':
            e = qrcode.constants.ERROR_CORRECT_M
        case 'Q':
            e = qrcode.constants.ERROR_CORRECT_Q
        case 'H':
            e = qrcode.constants.ERROR_CORRECT_H
        case _:
            raise ValueError('Error correction must be L, M, Q or H')

    qr = qrcode.QRCode(
        version=1,
        error_correction=e,
        box_size=1,
        border=0,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')

    img_array = np.array(img)

    qr_matrix = (img_array == 0).astype(int)
    
    return qr_matrix

def draw_qr_code(matrix, 
                 color='black', 
                 marge=50, 
                 pixel_size=100, 
                 shape:Shape=Shape.SQUARE, 
                 image_path=None,
                 image_percent=0.2,
                 background_color='#FFFFFF',
                 border_color='black',
                 border_size=0,
                 border_radius=10,
                 border_padding=1000,
                 text_color='white',
                 text_size=20,
                 text = None, 
                 text_background_color='black',
                 text_background_radius=10, 
                 text_background_padding=10):
    
    COTE = matrix.shape[0]*pixel_size

    font = ImageFont.truetype("Cards/fonts/static/Montserrat-Bold.ttf", text_size)
    
    # Gestion du texte pour la création de l'image
    (_, height), _ = font.font.getsize(text)
    text_shape = 0 if text is None else marge+height+text_background_padding*2
    print(text_shape)
    
    img_shape = marge*2+COTE+border_size*2+border_padding*2

    offset = marge+border_size+border_padding
    qr_img = Image.new("RGBA", (img_shape, img_shape+text_shape), background_color)
    print(qr_img.size)

    draw = ImageDraw.Draw(qr_img)

    # Ajout de la bordure
    if border_size > 0:
        if border_radius > 0:
            draw.rounded_rectangle([marge, marge, marge+COTE+border_size*2+border_padding*2, marge+COTE+border_size*2+border_padding*2], fill=border_color, radius=border_radius)
            draw.rounded_rectangle([marge+border_size, marge+border_size, marge+COTE+border_size+border_padding*2-1, marge+COTE+border_size+border_padding*2-1], fill=background_color, radius=border_radius)
        else:
            draw.rectangle([marge, marge, marge+COTE+border_size*2+border_padding*2, marge+COTE+border_size*2+border_padding*2], fill=border_color)
            draw.rectangle([marge+border_size, marge+border_size, marge+COTE+border_size+border_padding*2-1, marge+COTE+border_size+border_padding*2-1], fill=background_color)

    # Génération du QR code
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 1:
                if shape == Shape.SQUARE:
                    draw.rectangle([offset+j*pixel_size, offset+i*pixel_size, offset+(j+1)*pixel_size-1, offset+(i+1)*pixel_size-1], fill=color)
                elif shape == Shape.ELLIPSE:
                    draw.ellipse([offset+j*pixel_size, offset+i*pixel_size, offset+(j+1)*pixel_size, offset+(i+1)*pixel_size], fill=color)

    # Ajout de l'image au centre du QR code
    if image_path:
        img = Image.open(image_path).convert("RGBA")
        
        c_img = (int((image_percent*COTE**2)**0.5)//pixel_size-1)*pixel_size
        img = img.resize((c_img, c_img))

        qr_img.paste(img, (offset+(COTE-c_img)//2, offset+(COTE-c_img)//2), img)

    # Ajout du texte
    if text:
        if text_background_color:
            x1 = marge
            y1 = 2 * marge + COTE + border_size * 2 + border_padding * 2
            x2 = marge + COTE + border_size * 2 + border_padding * 2
            y2 = y1 + height + text_background_padding * 2

            if text_background_radius > 0:
                draw.rounded_rectangle([(x1, y1), (x2, y2)], fill=text_background_color, radius=text_background_radius)
            else:
                draw.rectangle([(x1, y1), (x2, y2)], fill=text_background_color)

        # texte centré en x et y
        w = draw.textlength(text, font=font)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_height = text_bbox[3] - text_bbox[1]
        
        text_y = y1 + (y2 - y1 - text_height) / 2

        draw.text(((img_shape - w) / 2, text_y), text, font=font, fill=text_color)


    return qr_img


if __name__ == '__main__':
    img = draw_qr_code(url_to_qr_matrix('www.google.fr'), 
                 color='black', 
                 pixel_size=10, 
                 shape=Shape.SQUARE, 
                 image_path='images.png',
                 border_size=50,
                 border_radius=30,
                 border_padding=40, 
                 text="¡SCAN ME!", 
                 text_size=70,
                 text_background_radius=10,
                 text_color='white',
                 text_background_padding=50,)

    
    img.save("QR.png")
    