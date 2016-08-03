from ulo.circuit import Circuit, Swap

def polarize(mode):
    return "{}{}".format("hv"[mode%2], mode/2)

class PBS(Circuit):
    components = [Swap(1, 2)]

    def __str__(self):
        return "PBS ({})".format(", ".join(map(polarize, self.modes)))

class HWP(Circuit):
    components = [BS(0)]

    def __str__(self):
        return "HWP ({})".format(", ".join(map(polarize, self.modes)))


# Dream structure (this is fuckin easy mate)
# PBS acts on two qubits:
p = PBS(0, 1)

# WP acts on one qubit
p = HWP(0)

print p # -> gives a description in polarization encoding

class Fusion(Circuit):
    components = HWP(0), PBS(0, 1), HWP(1)

print Fusion() # -> gives a description in polarizatio encoding

# Trickier:

class TwoFusions(PolarizedCircuit):
    components = Fusion(0, 1), Fusion(2, 3)


