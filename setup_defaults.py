# Quick Start Script for WhatsApp Clone

## Create a default user profile image
from PIL import Image, ImageDraw
import os

# Create static/uploads/profiles directory if it doesn't exist
os.makedirs('static/uploads/profiles', exist_ok=True)

# Create a default profile image
img = Image.new('RGB', (200, 200), color='#00ff41')
d = ImageDraw.Draw(img)

# Draw a circle
d.ellipse([50, 50, 150, 150], fill='#0a0e0f', outline='#00ff41', width=3)

# Save
img.save('static/uploads/profiles/default.png')

print("✅ Default profile image created!")
print("✅ Setup complete!")
print("\nRun: python run.py")
