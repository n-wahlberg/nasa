import testing as x

img = x.Query('natural', '2022-04-10')
img.retrieve_data()
x.save_images(img)
