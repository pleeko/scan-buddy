# Scan buddy
Python utility to auto rotate and crop scans of tcg cards.

### How to run
``` 
python index.py -i test_data/front-left.jpg -o op/front-left-op.jpg -s 1.1 -t "this is some text"
python index.py -i test_data/front-right.jpg -o op/front-right-op.jpg -s 1.3
python index.py -i test_data/back-left.jpg -o op/back-left-op.jpg -s 1.1 
python index.py -i test_data/back-right.jpg -o op/back-right-op.jpg -s 1.1
```
### Todo
- [ ] Different text fonts
- [ ] Naming based on id
- [ ] Bulk import option
- [x] Crop sizing
- [x] Custom text
