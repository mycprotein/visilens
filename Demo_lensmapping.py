import numpy as np
from RayTracePixels import LensRayTrace
from Model_objs import *
from SourceProfile import *
import matplotlib.pyplot as pl
from matplotlib.widgets import Slider,Button
from astropy.cosmology import get_current,set_current
set_current('WMAP9')
cosmo = get_current()

xim = np.arange(-3,3,.03)
yim = np.arange(-3,3,.03)

xim,yim = np.meshgrid(xim,yim)

zLens,zSource = 0.8,5.656
xLens,yLens = 0.,0.
MLens,eLens,PALens = 2.87e11,0.54,96.4
xSource,ySource,FSource,sSource = 0.216,-0.24,0.023,0.074

Lens = SIELens(zLens,xLens,yLens,MLens,eLens,PALens)
Source = GaussSource(zSource,True,xSource,ySource,FSource,sSource)
Shear = ExternalShear(0.,0.)
Dd = cosmo.angular_diameter_distance(zLens).value
Ds = cosmo.angular_diameter_distance(zSource).value
Dds = cosmo.angular_diameter_distance_z1z2(zLens,zSource).value

xsource,ysource = LensRayTrace(xim,yim,Lens,Dd,Ds,Dds,shear=Shear)

f = pl.figure()
ax = f.add_subplot(111,aspect='equal')
pl.subplots_adjust(bottom=0.25,top=0.98)

#ax.plot(xim,yim,'g-')
p = ax.plot(xsource,-ysource,'b-')

# Put in a bunch of sliders to control lensing parameters

axcolor='lightgoldenrodyellow'
ytop,ystep = 0.2,0.035
axzL = pl.axes([0.07,ytop,0.4,0.03],axisbg=axcolor)
axzS = pl.axes([0.07,ytop-ystep,0.4,0.03],axisbg=axcolor)
axxL = pl.axes([0.07,ytop-2*ystep,0.4,0.03],axisbg=axcolor)
axyL = pl.axes([0.07,ytop-3*ystep,0.4,0.03],axisbg=axcolor)
axML = pl.axes([0.07,ytop-4*ystep,0.4,0.03],axisbg=axcolor)
axeL = pl.axes([0.56,ytop,0.4,0.03],axisbg=axcolor)
axPAL= pl.axes([0.56,ytop-ystep,0.4,0.03],axisbg=axcolor)
axss = pl.axes([0.56,ytop-2*ystep,0.4,0.03],axisbg=axcolor)
axsa = pl.axes([0.56,ytop-3*ystep,0.4,0.03],axisbg=axcolor)

slzL = Slider(axzL,"z$_{Lens}$",0.01,3.0,valinit=zLens)
slzS = Slider(axzS,"z$_{Source}$",slzL.val,10.0,valinit=zSource)
slxL = Slider(axxL,"x$_{Lens}$",-1.5,1.5,valinit=xLens)
slyL = Slider(axyL,"y$_{Lens}$",-1.5,1.5,valinit=yLens)
slML = Slider(axML,"log(M$_{Lens}$)",10.,12.5,valinit=np.log10(MLens))
sleL = Slider(axeL,"e$_{Lens}$",0.,1.,valinit=eLens)
slPAL= Slider(axPAL,"PA$_{Lens}$",0.,180.,valinit=PALens)
slss = Slider(axss,"Shear",0.,1.,valinit=Shear.shear['value'])
slsa = Slider(axsa,"Angle",0.,180.,valinit=Shear.shearangle['value'])

def update(val):
      zL,zS = slzL.val,slzS.val
      xL,yL = slxL.val, slyL.val
      ML,eL,PAL = slML.val,sleL.val,slPAL.val
      sh,sha = slss.val,slsa.val
      newDd = cosmo.angular_diameter_distance(zL).value
      newDs = cosmo.angular_diameter_distance(zS).value
      newDds= cosmo.angular_diameter_distance_z1z2(zL,zS).value
      newLens = SIELens(zLens,xL,yL,10**ML,eL,PAL)
      newShear = ExternalShear(sh,sha)
      xs,ys = LensRayTrace(xim,yim,newLens,newDd,newDs,newDds,newShear)
      for i in range(len(xs)):
            p[i].set_xdata(xs[i])
            p[i].set_ydata(-ys[i])
      f.canvas.draw_idle()

slzL.on_changed(update); slzS.on_changed(update)
slxL.on_changed(update); slyL.on_changed(update)
slML.on_changed(update); sleL.on_changed(update); slPAL.on_changed(update)
slss.on_changed(update); slsa.on_changed(update)

resetax = pl.axes([0.92,0.48,0.05,0.04])
button = Button(resetax,'Reset',color=axcolor,hovercolor='0.975')
def reset(event):
      slzL.reset(); slzS.reset()
      slxL.reset(); slyL.reset()
      slML.reset(); sleL.reset(); slPAL.reset()
      slss.reset(); slsa.reset()
button.on_clicked(reset)


pl.show()
