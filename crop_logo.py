from PIL import Image

im = Image.open('results/poster_assets/image1.png')
# bbox is (97, 30, 457, 390)
# let's add a 2px margin around the circular border
crop_box = (95, 28, 459, 392)
im_cropped = im.crop(crop_box)
im_cropped.save('results/poster_assets/iitp_logo_cropped.png')
print(f'Cropped IIT Patna logo: original {im.size} -> cropped {im_cropped.size}')

