from flask import Flask, send_file, request
import os
from PIL import Image
from werkzeug.utils import secure_filename


app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = os.getcwd() + "/test_docs"

#--------Binary conversion functions--------

# to_binary(string) => str
# INPUTS:
#     string: A string type
# This function converts and returns the inputted string into binary 
def to_binary(string):
   binary = str(''.join(format(ord(i), '08b') for i in string))
   
   return binary   


#--------Image encoding functions--------------

# change_pixel(binary, pixel, cont) => tuple
# INPUTS:
#     binary: A list consisting of either '1' or '0'
#     pixel: A tuple of integers of the form (r, g, b, alpha)
#     cont: Boolean
# This function changes the r,g,b channels of the inputted pixel to either odd or even integers according to the corresponding binary values
# '1' signifies an odd value
# '0' signifies an even value
def change_pixel(binary, pixel, cont):
    new_pixel = list(pixel)

    for i in range(len(binary)):
      if binary[i] == '1' and pixel[i] % 2 == 0:
        new_pixel[i] = pixel[i]- 1
      elif binary[i] == '0' and pixel[i] % 2 == 1:
        new_pixel[i] = pixel[i]- 1
            
    if not cont:
        new_pixel[3] = 254
    else:
       new_pixel[3] = 255

    return tuple(new_pixel)


# encode(binary, p_map, img) => Image object
# INPUTS:
#     binary: A nested list of the form [['1', '0', '1'] ['1', '0', '1']...] 
#     p_map: An Image pixel object
#     img: An Image object
# This function encodes an entire binary message in the given pixels of an Image object. 
def encode(binary, p_map, img):

  for i in range(img.width):
    for j in range(img.height):
      try:
        if len(binary) > 1:
          p_map[i,j] = change_pixel(binary[0], p_map[i,j], True)
          binary.pop(0)
        elif len(binary) == 1:
          p_map[i,j] = change_pixel(binary[0], p_map[i,j], False)
          binary.pop(0)
      except:
        pass

  return p_map



@app.route("/encode_request", methods=["POST"])
def encode_request():
   
   file = request.files["file"]
   message = request.form["message"]


   file_path = os.path.join(UPLOAD_FOLDER, file.filename)
   file.save(file_path)

   # Open the image in PIL
   img = Image.open(file_path)
   pix_map = img.load()
  
   # Image encoding
   binary_message = to_binary(message)
   grouped_list = [binary_message[n:n+3] for n in range(0, len(binary_message), 3)]

   encode(grouped_list, pix_map, img)

   img.save(file_path)
   img.close()


   return_obj = send_file(file_path, mimetype="image/png")
   os.remove(file_path)
   
   return return_obj






#-----Decoding binary conversion functions------------

# to_string(binary) => str
# INPUTS:
#     binary: A list consisting of either '1' or '0'
# This function converts given binary into a string
def to_string(binary):
    binary = ''.join(binary)
    return ''.join(chr(int(binary[i*8:i*8+8],2)) for i in range(len(binary)//8))


#--------Decoding functions----------------

# decode(p_map, img) => list
# INPUTS:
#     p_map: An Image pixel object
#     img: An Image object
# This function goes through an extracts binary from an known encoded image. 
def decode(p_map, img):

  binary = []

  for i in range(img.width):
    for j in range(img.height):
      
      for k in range(3):
        if p_map[i,j][k] % 2 == 0 :
          binary.append('0')
        else:
          binary.append('1')

        if p_map[i,j][3] == 254:
          return binary



@app.route("/decode_request", methods=["POST"])
def decode_request():
   
   file = request.files["file"]

   file_path = os.path.join(UPLOAD_FOLDER, file.filename)
   file.save(file_path)

    #----Open the image in PIL-------
   img = Image.open(file_path)
   pix_map = img.load()

   #-------Perform decoding operation-------
   decode_binary_message = decode(pix_map, img)
   final_message = to_string(decode_binary_message)

   img.save(file_path)
   img.close()

   os.remove(file_path)
   
   return {"message" : final_message}



if __name__ == "__main__":
    app.run(debug=True)
