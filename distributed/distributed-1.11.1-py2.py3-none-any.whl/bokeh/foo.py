from distributed import LocalCluster, Executor
c = LocalCluster()
c.start_diagnostics_server(show=True)

e = Executor(c)

def inc(x):
    return x + 1

futures = e.map(inc, range(1000))
