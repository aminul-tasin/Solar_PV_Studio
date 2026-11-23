import math

def bisection(f, a, b, tol=1e-8, max_iter=200):
    fa, fb = f(a), f(b)
    if fa == 0: return a, 0
    if fb == 0: return b, 0
    if fa * fb > 0: raise ValueError("Bisection requires a sign-changing interval.")
    for i in range(1, max_iter + 1):
        c = (a+b)/2
        fc = f(c)
        if abs(fc) < tol or abs(b-a)/2 < tol: return c, i
        if fa*fc < 0: b, fb = c, fc
        else: a, fa = c, fc
    return (a+b)/2, max_iter

def newton_raphson(f, df, x0, tol=1e-8, max_iter=100):
    x = float(x0)
    for i in range(1, max_iter+1):
        fx, dfx = f(x), df(x)
        if abs(fx) < tol: return x, i
        if abs(dfx) < 1e-14: raise ValueError("Derivative is too small.")
        xn = x - fx/dfx
        if not math.isfinite(xn): raise ValueError("Newton iteration diverged.")
        if abs(xn-x) < tol: return xn, i
        x = xn
    return x, max_iter
