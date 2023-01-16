from PIL import Image

# Create an image with a transparent background
img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))

# Save the image as a PNG file
img.save("transparent.png", "PNG")
