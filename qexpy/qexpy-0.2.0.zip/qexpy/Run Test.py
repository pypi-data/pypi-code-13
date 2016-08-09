import error as e
import plotting as p

x = e.Measurement(10, 1)
y = e.Measurement(5, 1)

z = x+y
z.rename('Final Value')
z.show_MC_histogram()
