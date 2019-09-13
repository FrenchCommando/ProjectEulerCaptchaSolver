from collections import defaultdict
import numpy as np
from PIL import Image
from mnist import Mnist


mnist_model = Mnist()


def resolve(file_path):
    img = Image.open(file_path, 'r')
    # img.show()
    img_array = np.array(img)

    def color_to_coordinates(image):
        d = defaultdict(list)  # matches color with coordinates
        for i, u in enumerate(img_array):
            for j, v in enumerate(u):
                t = tuple(v)
                d[t].append((i, j))
        return d

    def count_to_color(clr_to_coor):
        d2 = defaultdict(list)
        for x, y in clr_to_coor.items():
            d2[len(y)].append(x)
        return d2

    def max_color(cnt_to_clr):
        k = iter(sorted(cnt_to_clr.keys(), reverse=True))
        while True:
            kk = next(k)
            for u in cnt_to_clr[kk]:
                yield kk, u

    d_img = color_to_coordinates(img)
    d2 = count_to_color(d_img)
    m = max_color(d2)
    next(m)
    rep = {}
    for i in range(5):
        c = next(m)[1]
        color_array = np.zeros_like(img_array)
        l_c = d_img[c]
        for (x, y) in l_c:
            color_array[x][y] = [255, 255, 255]
        mmin = np.min(l_c, axis=0)
        mmax = np.max(l_c, axis=0)
        img_i = (Image.fromarray(color_array)).crop((mmin[1] - 10, mmin[0] - 10, mmax[1] + 10, mmax[0] + 10)).resize(
            (Mnist.img_rows, Mnist.img_cols))
        mm = int(np.mean(l_c, axis=0)[1])
        img_i_array = np.array(img_i)
        # img_i.show()
        clean_img = np.mean(img_i_array, axis=2)
        ans = mnist_model.guess(clean_img)
        rep[mm] = ans
    rr = ''.join(str(rep[v]) for v in sorted(rep.keys()))
    # print(rep)
    return rr


if __name__ == "__main__":
    file_path = 'temp.png'
    print(file_path)
    print('Resolving Captcha')
    captcha_text = resolve(file_path)
    print(captcha_text)
    print('Extracted Text', captcha_text)

