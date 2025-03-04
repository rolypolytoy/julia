# julia
Julia's an interactive visualization of the julia sets. The real element and the imaginary element of c can be moved with a slider.
Why make this? It looks cool and is a very small amount of LOC. If you increase the iterations and don't use the @jit option, it'll take too long to load, but you can increase the amount of iterations to 100 or higher, for better quality at the expense of some speed.

# Dependencies
You'll need the numpy, numba, matplotlib and tkinter libraries for this. These are necessary (or effectively necessary) for numerical acceleration and the UI. If you don't already have these, just do the following:

	pip install numpy numba matplotlib tkinter

Then run julia-set.py, and enjoy.
