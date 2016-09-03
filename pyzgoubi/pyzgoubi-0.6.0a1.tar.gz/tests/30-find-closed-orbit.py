tline = Line('t')
xpas = (20,20,20)
angle = 360/1000
angle = 1e-1

#lengths
ld = 50 * mm
sd = 50 * mm

fq = 50 * mm
dq = 50 * mm

# quad radius
fr = 50 * mm
dr = 50 * mm

fb = -4 * fr * T
db = 4 * dr * T

ob = OBJET2()
tline.add(ob)

tline.add(ELECTRON())

tline.add(DRIFT('ld', XL=ld*cm_/2))
tline.add(CHANGREF(ALE=angle))

tline.add(QUADRUPO('defoc', XL=dq*cm_, R_0=dr*cm_, B_0=db*kgauss_, XPAS=xpas, KPOS=1))
tline.add(DRIFT('sd', XL=sd*cm_))
tline.add(QUADRUPO('foc', XL=fq*cm_, R_0=fr*cm_, B_0=fb*kgauss_, XPAS=xpas, KPOS=1))
tline.add(DRIFT('ld', XL=ld*cm_/2))

offset = -0.5311063 -0.05748192 -6.16712135e-03 -6.61037008e-04 -7.08476342e-05 -7.59311969e-06
offset  =0
tline.add(CHANGREF(YCE=offset))
tline.add(FAISCNL(FNAME='zgoubi.fai'))
tline.add(CHANGREF(YCE=-offset))

tline.add(REBELOTE(K=99, NPASS=10))
tline.add(END())

rigidity = ke_to_rigidity(10e6, ELECTRON_MASS)
ob.set(BORO=-rigidity)
ob.add(Y=0, T=0, D=1)


closed_orbit = find_closed_orbit(tline, init_YTZP=[0,0,0,0], tol=1e-10)
#closed_orbit = find_closed_orbit(tline, init_YTZP=[0,0,0,0], tol=1e-10, plot_search="/tmp/foo.pdf")

print closed_orbit

