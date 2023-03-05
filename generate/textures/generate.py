from PIL import Image


# Define the image size
side_length = 16

img = Image.new("RGB", (side_length, side_length), color=0)
pixels = img.load()
for x in range(side_length):
    for y in range(side_length):
        pixels[x, y] = (0, 100, 0)  # Set RGB value of each pixel

# Save the image as a PNG file
img.save("assets/textures/green.png")

