# CUMUL

Implementation of "Website Fingerprinting at Internet Scale"

Reproduce from original code of paper's author: [`http://lorre.uni.lu/~andriy/zwiebelfreunde/`](http://lorre.uni.lu/~andriy/zwiebelfreunde/)

------

*Update at Feb. 2023*

Since the original dataset link is no longer available, please download the dataset from the [Web Archive](https://web.archive.org/web/20180716181420/http://lorre.uni.lu/~andriy/zwiebelfreunde/)

------

If you find this method helpful for your research, please cite this paper:

```
@inproceedings{panchenko2016website,
  title={Website Fingerprinting at Internet Scale.},
  author={Panchenko, Andriy and Lanze, Fabian and Pennekamp, Jan and Engel, Thomas and Zinnen, Andreas and Henze, Martin and Wehrle, Klaus},
  booktitle={NDSS},
  year={2016}
}
```

### Dependency

```
Python 3.5 +
sklearn
```

### Dataset

Download `foreground.tar.gz` and `background.tar.gz` from [`http://lorre.uni.lu/~andriy/zwiebelfreunde/`](http://lorre.uni.lu/~andriy/zwiebelfreunde/) and extract files.

Then config your dataset path at `main.py`
