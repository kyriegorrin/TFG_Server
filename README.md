# TFG_Server
Repositori per la part del servidor/GUI del sistema, en Python 3.

El programa principal espera connexions entrants i fa display de les dades rebudes via socket, enviades per la Raspberry Pi dedicada a recol·lecció i tractament de dades 3D.

En aquest repositori poden existir programes secundaris, ja sigui de test de funcionalitats o secundaris.

## Llista de dependencies (python)
Si no s'indica el contrari, totes les dependències s'instalaran via pip (pip install <package name>).

- Numpy: pip install numpy
- Cython: pip install Cython
- PyQt5: pip install PyQt5
- Matplotlib: pip install matplotlib

//La resta pot ser que siguin necessaris en un futur:
- ModernGL: pip install moderngl
- - Required sub-dependencies:
- - objloader
- - numpy
- - pillow
- - pyrr
- - pymunk
- - matplotlib
- - imageio

## Dependencies de software
Software que no són packages de Python.

- Qt5