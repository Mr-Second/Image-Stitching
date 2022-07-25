# Image Stitching

## About thestitchlibrary

This library aims to help users quickly and orderly splicing pictures.

## Usage

>python setup.py install # install package

```python
from stitch import Painter

if __name__ == "__main__":
    p = Painter()
    p.set_source(r"C:\Users\Administrator\Desktop\test_data")
    p.set_result_directory(r"C:\Users\Administrator\Desktop")
    p.set_suffix(["ssn", "gt", "pred"], ['jpg', 'png', 'png', 'png']) # the former list is name suffix list, the latter list is type suffix list
    p.set_horizontal_text(['Original Image', 'Superpixel Image', 'Ground Truth', 'Predict Image'])
    p.generate()
```

## Input & Output

### Input

<div align=center>
    <img src="https://cdn.jsdelivr.net/gh/Mr-Second/ImageBed@master/img/202207251654503.png"/>
</div>

### Output

![result](https://cdn.jsdelivr.net/gh/Mr-Second/ImageBed@master/img/202207251658418.png)

