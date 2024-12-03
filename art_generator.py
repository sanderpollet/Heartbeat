from PIL import Image, ImageDraw, ImageFont
import random

def generate_art(heart_rate, temperature):
    # Create a base image with a white background
    img = Image.new('RGB', (800, 800), color='white')
    draw = ImageDraw.Draw(img)
    
    # Use temperature to change the background color dynamically
    if temperature < 26:
        background_color = (0, 0, 255)  # cool blue for lower temperatures
    elif temperature > 28:
        background_color = (255, 0, 0)  # hot red for higher temperatures
    else:
        background_color = (255, 255, 0)  # yellow for moderate temperatures
    
    img.paste(background_color, [0, 0, img.size[0], img.size[1]])

    # Add heart rate as text
    text = f"Heart Rate: {heart_rate}\nTemperature: {temperature}"
    font = ImageFont.load_default()
    draw.text((10, 10), text, fill="black", font=font)
    
    # Optionally, add randomness based on temperature (e.g., changes in texture or patterns)
    for _ in range(int(temperature * random.uniform(0, 2))):  # More randomness for higher temperatures
        x1 = random.randint(0, img.width)
        y1 = random.randint(0, img.height)
        x2 = random.randint(0, img.width)
        y2 = random.randint(0, img.height)
        draw.line((x1, y1, x2, y2), fill="black", width=2)
    
    # Save the image
    img.save("static/images/current_art.png")

# Example usage:
generate_art(heart_rate=75, temperature=27.33)
