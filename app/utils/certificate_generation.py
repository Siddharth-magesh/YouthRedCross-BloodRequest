from PIL import Image, ImageDraw, ImageFont
import os

def generate_certificate(donor_name,donation_date,blood_group,location):
    template_path = r'app\static\images\certificate_templates\template1.png'
    template = Image.open(template_path)

    draw = ImageDraw.Draw(template)
    font_path = r'app\static\fonts\ARLRDBD.TTF'
    font_size = 25
    font = ImageFont.truetype(font_path,font_size)

    text_details = [
        (donor_name, (328, 187)),
        (donation_date, (215, 417)),
        (blood_group, (675, 188)), 
        (location, (267, 455))  
    ]

    for text , position in text_details:
        draw.text(position, text,font=font,fill='black')

    save_path = r'app\static\images\certificates'
    os.makedirs(save_path, exist_ok=True)
    file_name = f"{donor_name.replace(' ', '_')}_certificate.png"
    file_path = os.path.join(save_path,file_name)
    template.save(file_path)

    #print(f"Certificate saved at {file_path}")
    return file_path