Pre-trained Grapheme-to-Phoneme (G2P) models
====
This project is aiming to produce high quality phoneme transcriptions as the ground-truth for other non-grapheme-to-phoneme projects.

### Highlights

* If a word can be found in the given phonemic dictionary, it will use the phonemic transcriptions provided by the dictionary.
* If a word can not be found in the given phonemic dictionary, it will do the convertion with the pre-trained G2P model.
* You don't need to mind the speed of the pre-trained G2P model since all the convertion results of it will be cached.
* You can check the convertion results in the logs at the debug level.

### Installation

* Install [Sequitur G2P](https://github.com/sequitur-g2p/sequitur-g2p)
* Clone the repository and update the submodules
```sh
git clone https://github.com/petronny/g2p
cd g2p
git submodule update --init
```

### Usage

See [demo.py](https://github.com/petronny/g2p/blob/master/demo.py)
