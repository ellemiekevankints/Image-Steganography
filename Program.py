from PIL import Image
import numpy as np
import sys

# GLOBAL VARIABLES

loop = True

# FUNCTIONS

def prompt_user():
   print("\nCommand Options")
   print(" - Encode: e")
   print(" - Decode: d")
   print(" - Quit: q\n") 

def input_msg():
    
    msg = '' 
    file = input("Enter the file containing the message you wish to hide: ").strip()
    print()
    
    # open and read the file
    try: 
        with open(file) as f:
            msg = f.read() 
            f.close() 
            print("File opened successfully!\n")    
    except OSError as e:
        print("OS ERROR:", e.strerror)
        print("Exiting program...")
        sys.exit(1)
    except:
        print("UNEXPECTED ERROR:", sys.exc_info()[0])
        print("Exiting program...")
        sys.exit(1)
    
    return msg

def input_img():
   
    img = input("Enter the source image path: ").strip()
    print()
    
    # open and read the file
    try: 
        with open(img) as f:
            print("Image opened successfully!\n")   
            f.close()  
    except OSError as e:
        print("OS ERROR:", e.strerror)
        print("Exiting program...")
        sys.exit(1)
    except:
        print("UNEXPECTED ERROR:", sys.exc_info()[0])
        print("Exiting program...")
        sys.exit(1)
    
    return img 

def encode(src, message, dest, n):
    
    """ Encodes the source image with the secret message. 
        This code was provided in a Medium article written by Devang Jain, which can be found here: https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2
    """
     
    img = Image.open(src, 'r')
    img = img.convert('RGB') # convert image to RBG
    width, height = img.size
    array = np.array(list(img.getdata())) # 2D aray which holds the pixel data, with each band in its own cell
     
    total_pixels = array.size//3 # 3 represents the 3 bands, RGB
    
    message += "$t3g0" # delimiter so program knows when to stop
    b_message = ''.join([format(ord(i), "08b") for i in message]) # binary form of the message 

    req_pixels = len(b_message)
    
    # check to ensure the total pixels available is sufficient for the secret message 
    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")
        return
    else: 
        index = 0
        for p in range(total_pixels):
            # replace 0 to n (exclusive) least significant bits in img with secret message
            for q in range(0, 3): 
                if index < req_pixels:
                    
                    b_new = b_message[index:n+index] # the new bits to insert
                    n_len = len(b_new) # the number of bits to insert 
                    
                    b_val = bin(array[p][q])[:9-n_len] # remove the bits that will be replaced
                    b_val += b_new # add the new bits to the binary pixel value 
                     
                    array[p][q] = int(b_val, 2) # put back in the img array 
                    index += n

        array = array.reshape(height, width, 3) # updated pixels array, with encoded secret message
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully") 
     
    return

def decode(src, n):
    
    """ Decodes the secret message from the image.
        This code was provided in a Medium article written by Devang Jain, which can be found here: https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2
    """
    
    img = Image.open(src, 'r')
    img = img.convert('RGB') # convert image to RBG
    array = np.array(list(img.getdata())) # 2D aray which holds the pixel data

    total_pixels = array.size//3 # 3 represents the 3 bands, RGB
    
    hidden_bits = ""
    for p in range(total_pixels):
        # extract the n least significant bits from the image 
        for q in range(0, 3):
            hidden_bits += bin(array[p][q])[9-n:]
     
    # store 8 bits together
    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)] 
    
    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            # convert binary to ASCII character 
            message += chr(int(hidden_bits[i], 2))
    
    # check if the delimiter was found or not
    if "$t3g0" in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")

# MAIN PROGRAM BEGINS 

print()
print("  ____  _                                                     _            ")   
print(" / ___|| |_ ___  __ _  __ _ _ __   ___   __ _ _ __ __ _ _ __ | |__  _   _  ") 
print(" \___ \| __/ _ \/ _` |/ _` | '_ \ / _ \ / _` | '__/ _` | '_ \| '_ \| | | | ")
print("  ___) | ||  __/ (_| | (_| | | | | (_) | (_| | | | (_| | |_) | | | | |_| | ")
print(" |____/ \__\___|\__, |\__,_|_| |_|\___/ \__, |_|  \__,_| .__/|_| |_|\__, | ")
print("                |___/                   |___/          |_|          |___/  ") 
print()

# MAIN PROGRAM LOOP

n = 3 # number of least significant bits modified, by default set to 3

while (loop):
    
    prompt_user()
    inp = input("Choose a command: ").strip()
    print()
     
    if inp == "q":
        
        print("Quitting the program..\nBye!\n")
        loop = False
         
    elif inp == "e":
        
        img = input_img() 
        msg = input_msg()
        dest = input("Enter the destination image path: ").strip()
        print()
        n = int(input("Enter the number of least-significant bits you wish to modify: ").strip())
        
        # the number of LSB to be modified must be greater than 0 and less than 8
        if n < 1 or n > 7:
            print("ERROR: The chosen value for n is invalid.")
            continue
        
        print("\nEncoding...\n")
        encode(img, msg, dest, n)
        
    elif inp == "d":
       
       img = input_img()
       print("Decoding...\n")
       decode(img, n) 
    
    else:
        print("ERROR: Command not recognized")
        