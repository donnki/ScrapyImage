 #! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
  
import Image
import os
  
  
class WaterMark(object):
    '''
    水印工具类，提供基本的给图片打水印的功能
    使用：
        marker = WaterMark(path) # path为水印图片的路径
        marker.mark(pic) # pic为待打水印的图片
        marker.mark_dir(pic_dir) # pic_dir为待打水印的目录
    '''
  
    POSITION_TOP_LEFT = 0
    POSITION_TOP_RIGHT = 1
    POSITION_BOTTOM_LEFT = 2
    POSITION_BOTTOM_RIGHT = 3
  
    # 在原图片中打水印的区域
    box = (0, 0, 0, 0)
  
    backup_suffix = '.bak'
  
    def _gen_mosaic(self, arg):
        '''打开水印图片'''
  
        try:
            mosaic = Image.open(arg).convert('RGBA')
        except IOError:
            print 'cannot convert file.'
        return mosaic
  
    def __init__(self, *args, **kwargs):
  
        if args:
            arg = args[0]
            self._mosaic = self._gen_mosaic(arg)
  
    def _locate(self, image,  position=POSITION_BOTTOM_RIGHT):
        '''定位原图片打水印的位置'''
  
        w, h = self._mosaic.size
        i_w, i_h = image.size
        if position == self.POSITION_TOP_LEFT:
            self.box = (0, 0, w, h)
        elif position == self.POSITION_TOP_RIGHT:
            self.box = (i_w - w, 0, i_w, h)
        elif position == self.POSITION_BOTTOM_LEFT:
            self.box = (0, i_h - h, w, i_h)
        elif position == self.POSITION_BOTTOM_RIGHT:
            self.box = (i_w - w, i_h - h, i_w, i_h)
        else:
            self.box = (0, 0, 0, 0)
  
    def mark(self, path, position=POSITION_BOTTOM_RIGHT):
        '''给单个图片打水印'''
  
        try:
            img = Image.open(path)
        except IOError:
            return None
  
        if img.size[0] < self._mosaic.size[0]:
            print 'width', img.size[0], self._mosaic.size[0]
            return None
        if img.size[1] < self._mosaic.size[1]:
            print 'height', img.size[1], self._mosaic.size[1]
            return None
        img_area = img.size[0] * img.size[1]
        mosaic_area = self._mosaic.size[0] * self._mosaic.size[1]
        ratio = 4
        if img_area < mosaic_area * ratio:
            return None
  
        self._locate(img, position)
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        layer.paste(self._mosaic, self.box)
  
        return Image.composite(layer, img, layer)
  
    def mark_dir(self, path, backup=False, position=POSITION_BOTTOM_RIGHT):
        '''批量打水印'''
  
        for root, dirs, files in os.walk(path):
  
            for f in files:
                path = os.path.join(root, f)
                if path.endswith(self.backup_suffix):
                    continue
                print path
  
                f_marked = self.mark(path)
                if not f_marked:
                    continue
  
                if backup:
                    os.rename(path, path + self.backup_suffix)
  
                f_marked.save(path, f_marked.format)
  
  
def test():
    '''
    用来测试打水印功能
    命令行使用：
        python watermark.py 水印图片路径 待打水印图片的目录
    '''
  
    import sys
    if len(sys.argv) < 3:
        return False
    mosaic_path = sys.argv[1]
    directory = sys.argv[2]
  
    marker = WaterMark(mosaic_path)
    marker.mark_dir(directory, backup=True)
  
  
if __name__ == '__main__':
    test()