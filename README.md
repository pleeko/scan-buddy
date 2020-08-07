# Scan buddy
Python utility to auto rotate and crop scans of tcg cards.

<<<<<<< HEAD
### Demo

<table>
  <thead>
      <tr>
          <th scope="col">Input</th>
          <th scope="col">Output</th>
      </tr>
  </thead>
    <tr>
    <td> <img src="./demo/readme/wof-front-scaled.jpg" style="width: 250px;"/> </td>
    <td> <img src="./demo/readme/wof-front-scaled.jpg" style="width: 250px;"/> </td>
  </tr>
</table>

```
python index.py -i demo/wof-front.jpg -o demo/wof-front-op.jpg -s 1.2 -t "Wheel of Fortune HP"
=======
### How to run
``` 
python index.py -i test_data/front-left.jpg -o op/front-left-op.jpg -s 1.1 -t "this is some text"
python index.py -i test_data/front-right.jpg -o op/front-right-op.jpg -s 1.3
python index.py -i test_data/back-left.jpg -o op/back-left-op.jpg -s 1.1 
python index.py -i test_data/back-right.jpg -o op/back-right-op.jpg -s 1.1
>>>>>>> 36e57c5aeb3a31efd1e12fa1d65a183bd93eb41b
```


<table>
  <thead>
      <tr>
          <th scope="col">Input</th>
          <th scope="col">Output</th>
      </tr>
  </thead>
    <tr>
    <td> <img src="./demo/readme/fow-front-scaled.jpg" style="width: 250px;"/> </td>
    <td> <img src="./demo/readme/fow-front-op.jpg" style="width: 250px;"/> </td>
  </tr>
</table>

```
python index.py -i demo/fow-front.jpg -o demo/fow-front-op.jpg -s 1.1 -t "Sample Text"
```

### Todo
- [ ] Different text fonts
- [ ] Naming based on id
- [ ] Bulk import option
- [x] Crop sizing
- [x] Custom text
