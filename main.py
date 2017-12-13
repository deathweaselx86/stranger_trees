import lib.opc
import time, copy

OFF_PIXEL = (0,0,0)

# here is a table matching ASCII characters to
# pixels in our string and colors
ASCII_PIXEL_TABLE = {
    'A': (0, (255,255,255)), # white
    'B': (1, (255,245,255)),
    'C': (2, (255,235,255)),
    'D': (3, (255,225,255)),
    'E': (4, (255,215,255)),
    'F': (5, (255,205,255)),
    'G': (6, (255,195,255)),
    'H': (7, (255,185,255)),
    'I': (8, (255,175,255)),
    'J': (9, (255,165,255)),
    'K': (10, (255,155,255)),
    'L': (11, (255,145,255)),
    'M': (12, (255,135,255)),
    'N': (13, (255,125,255)),
    'O': (14, (255,115,255)),
    'P': (15, (255,105,255)),
    'Q': (16, (255,95,255)),
    'R': (17, (255,85,255)),
    'S': (18, (255,75,255)),
    'T': (19, (255,65,255)),
    'U': (20, (255,55,255)),
    'V': (21, (255,45,255)),
    'W': (22, (255,35,255)),
    'X': (23, (255,25,255)),
    'Y': (24, (255,15,255)),
    'Z': (25, (255,5,255)),
    '@': (26, (255,0,255)),
    '!': (27, (255,0,245)),
    '.': (28, (255,0,235)),
    '#': (29, (255,0,225)),
    '"': (30, (255,0,215)),
    "'": (30, (255,0,215))
}


def get_reset_pixels():
    return [copy.deepcopy(OFF_PIXEL) for i in xrange(50)]

if __name__ == '__main__':
    client = lib.opc.Client('10.0.10.129:7890')
    test = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ@!.#"'
    print('testing %(test)s' % {'test': test})
    for i in range(len(test)):
        pixels = get_reset_pixels()
        index = ASCII_PIXEL_TABLE[test[i]][0]
        value = ASCII_PIXEL_TABLE[test[i]][1]
        print('lighting up pixel %(index)s for %(value)s' % 
                {'index': index, 'value': value})
        pixels[index] = value
        client.put_pixels(pixels)
        time.sleep(1)
