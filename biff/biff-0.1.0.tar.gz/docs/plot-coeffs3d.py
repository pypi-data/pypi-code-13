# # visualize coefficients

# from mpl_toolkits.mplot3d import Axes3D
# fig = pl.figure(figsize=(10,8))
# ax = fig.add_subplot(111, projection='3d')
# n,l,m = np.mgrid[:nmax+1, :lmax+1, :lmax+1]
# c = ax.scatter(n.ravel(), l.ravel(), m.ravel(), c=Snlm.ravel(), s=64,
#                norm=mpl.colors.SymLogNorm(1E-5), cmap='RdBu_r',
#                vmin=-1.5, vmax=1.5, linewidths=1., edgecolors='#666666')

# ax.xaxis.set_ticks(np.arange(0,nmax+1,1))
# ax.yaxis.set_ticks(np.arange(0,lmax+1,1))
# ax.zaxis.set_ticks(np.arange(0,lmax+1,1))

# ax.set_xlim(-0.5, nmax+0.5)
# ax.set_ylim(-0.5, lmax+0.5)
# ax.set_zlim(-0.5, lmax+0.5)

# ax.set_xlabel('$n$')
# ax.set_ylabel('$l$')
# ax.set_zlabel('$m$')

# tickloc = np.concatenate((-10.**np.arange(0,-5-1,-1),
#                           10.**np.arange(-5,0+1,1)))
# fig.colorbar(c, ticks=tickloc)

# fig.tight_layout()

# pl.show()
