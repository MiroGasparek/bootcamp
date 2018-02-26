# 26 February 2018 Miroslav Gasparek
# The useful functions written over the course of the Python bootcamp

def ecdf(data):
    """ Function that computes empirical cumulative distribution function of data."""
    # Get x data (sort out data)
    x = np.sort(data)
    # Get y data (compute from x)
    y = np.arange(1, len(data)+1)/len(data)
    return x,y
 
