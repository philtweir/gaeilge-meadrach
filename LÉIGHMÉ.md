# gaeilge-meadrach

Cluíche simplí atá scríofa i nGaeilge a úsáideann [AvantPy](https://github.com/philtweir/avantpy-extended)

https://user-images.githubusercontent.com/1624699/128638073-3f7023fe-35be-4845-b3fd-e2317b370089.mp4

![Gabháil scáileáin den chód](https://user-images.githubusercontent.com/1624699/128638142-b38bdb52-2abd-434e-a80b-458f80dda73f.png)

## Suiteáil

Le poetry:

    poetry install

## Rith

Le poetry:

    poetry run ./méadrach_clno.pyga

nó

    poetry run ./méadrach3d_clno.pyga

Le docker:

    > docker run -v $(pwd):/app --rm -ti python:3 /bin/bash
    $ pip install poetry
    $ poetry install
    $ ./méadrach.sh
