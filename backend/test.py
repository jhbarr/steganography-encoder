import random

binary = list('0111011101101000011000010111010001110011001000000111010101110000')
grouped_binary = [binary[n:n+3] for n in range(0, len(binary), 3)]

pixel_map = [(random.randint(0,255), random.randint(0,255), random.randint(0,255), 255) for i in range(100)]




def change_pixel(binary, pixel, cont):

    new_pixel = []

    for i in range(3):
        try:
            if binary[i] == '1' and pixel[i] % 2 == 0:
                new_pixel.append(pixel[i] - 1)

            elif binary[i] == '0' and pixel[i] % 2 == 1:
                new_pixel.append(pixel[i] - 1)

            else:
                new_pixel.append(pixel[i])
        except:
            new_pixel.append(pixel[i])
            

    if not cont:
        new_pixel.append(254)
    else:
       new_pixel.append(255)


    return tuple(new_pixel)



def encode(binary, p_map):

    for i in range(len(p_map)):
        if len(binary) > 1:
            p_map[i] = change_pixel(binary[0], p_map[i], True)
            binary.pop(0)
        
        else:
            p_map[i] = change_pixel(binary[0], p_map[i], False)
            return p_map


    return p_map





def decode(p_map):
    binary = []
    
    for pixel in p_map:
        for i in range(3):
            if pixel[i] % 2 == 0:
                binary.append('0')
            else:
                binary.append('1')
        
        if pixel[3] == 254:
            while len(binary) % 8 != 0:
                binary.pop(-1)
            return binary
        


def to_string(binary):
    return ''.join(chr(int(binary[i*8:i*8+8],2)) for i in range(len(binary)//8))




new_pixel_map = encode(grouped_binary, p_map=pixel_map)

decoded_binary = ''.join(decode(new_pixel_map))
print(to_string(decoded_binary))





