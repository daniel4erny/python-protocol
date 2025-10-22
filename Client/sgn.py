import math

def sgn(x):
    try:
        x = int(x)
        if x == int(0):
            return(0)
        elif x == 69:
            return("fuck niggas")
        else:
            y = x * x 
            y = math.sqrt(y)
            if y == x:
                return(1)
            elif y != x:
                return(-1)
    except Exception as e:
        return(f"kokot tupa tady mas error (debile) {e}")
        
while True:
    print(sgn(input("napiš čisličko")))
    