import sys

if sys.platform[:5] == 'linux' or sys.platform[:6] == 'darwin':
    import linux_monitoring as agent
else:
    print {'error':'platform not supported'}
    sys.exit(1)

def get_metrics():
    return agent.get_metrics()
