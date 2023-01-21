import io, os
from PIL import Image, ImageChops, ImageStat


def imgcheck(ref_file, now_file, show_diff=False, generate_ref_files=False):

    def imgdiff(img1, img2, diff_file=None, show_diff=False):

        img1 = Image.open(io.BytesIO(img1))
        img2 = Image.open(io.BytesIO(img2))

        # See https://stackoverflow.com/q/15721484 for motivation
        #  for .convert('RGB')
        imgd = ImageChops.difference(img1, img2).convert('RGB')
        stat = ImageStat.Stat(imgd)

        diff = True
        if stat.sum[0] == 0.0 and stat.sum[1] == 0.0 and stat.sum[2] == 0.0:
            diff = False

        if diff and diff_file is not None:
            imgd.save(diff_file)

        if show_diff:
            imgd.show()

        return diff

    ref_dir = os.path.dirname(ref_file)

    if not os.path.exists(ref_dir):
        os.makedirs(ref_dir)

    if not os.path.exists(ref_file) or generate_ref_files:

        if not os.path.exists(ref_file):
            print('Reference file does not exist. Writing ' + ref_file)
        else:
            print('Generating reference file.')

        if isinstance(now_file, bytes):
            now_img = Image.open(io.BytesIO(now_file))
            now_img.save(ref_file)
        else:
            import shutil
            shutil.copyfile(now_file, ref_file)

        return False

    with open(ref_file, 'rb') as f:
        ref_bytes = f.read()

    if isinstance(now_file, bytes):
        now_bytes = now_file
        now_img = Image.open(io.BytesIO(now_bytes))
        now_img.save(ref_file.replace(".ref.",".now."))
    else:
        with open(now_file, 'rb') as f:
            now_bytes = f.read()

    diff_file = ref_file.replace(".ref.",".dif.")

    diff = imgdiff(ref_bytes, now_bytes, diff_file=diff_file, show_diff=show_diff)

    if diff == False:
        print("imgcheck(): \033[32mPASS\033[0m: Image")
        print("   " + ref_file)
        print("   has not changed")
        return True
    else:
        print("imgcheck(): \033[0;31mFAIL\033[0m: Images differ. See diff image: " + diff_file)
        return False
