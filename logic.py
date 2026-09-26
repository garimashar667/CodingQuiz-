# logic.py
import random
import string
from PIL import Image, ImageDraw

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def calculate_points(time_remaining, difficulty, total_time=15):
    multiplier = {"Easy": 1, "Medium": 1.5, "Hard": 2, "Extreme": 3}
    base_points = 500 * multiplier.get(difficulty, 1)
    if time_remaining <= 0:
        return int(base_points)
    bonus = ((time_remaining / total_time) * 500) * multiplier.get(difficulty, 1)
    return int(base_points + bonus)

def create_certificate(player_name, rank=None):
    img = Image.new('RGB', (800, 600), color='#1A252C')
    draw = ImageDraw.Draw(img)
    draw.rectangle([(20, 20), (780, 580)], outline='#F1C40F', width=5)
    
    draw.text((400, 100), "CERTIFICATE OF ACHIEVEMENT", fill="#F1C40F", anchor="mm")
    draw.text((400, 180), "This is proudly presented to", fill="#FFFFFF", anchor="mm")
    draw.text((400, 260), player_name.upper(), fill="#3498DB", anchor="mm")
    
    if rank is not None and rank <= 3:
        text_content = f"For securing Rank {rank} in the CodeQuest Custom Challenge Arena!"
        draw.text((400, 350), text_content, fill="#2ECC71", anchor="mm")
        draw.text((400, 420), "TOP PERFORMER AWARD", fill="#F1C40F", anchor="mm")
    else:
        draw.text((400, 350), "For successfully participating and surviving all levels", fill="#CCCCCC", anchor="mm")
        draw.text((400, 390), "in the CodeQuest Dynamic User Generated Portal.", fill="#CCCCCC", anchor="mm")
        
    draw.text((400, 520), "Verified by: CodeQuest Python Engine", fill="#7F8C8D", anchor="mm")
    filename = f"{player_name.replace(' ', '_')}_cert.png"
    img.save(filename)
    return filename