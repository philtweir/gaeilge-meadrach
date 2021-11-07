import pandac.PandaModules as pm
from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader

from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import Sequence
import math

#Load the first environment model
base = ShowBase()
loader = Loader(base)
environ = loader.loadModel("models/environment")
environ.reparentTo(base.render)
environ.setScale(0.25,0.25,0.25)
environ.setPos(-8,42,0)

#Load the panda actor, and loop its animation
pandaActor = Actor.Actor("models/panda-model",{"walk":"models/panda-walk4"})
pandaActor.setScale(0.005,0.005,0.005)
pandaActor.reparentTo(base.render)
pandaActor.loop("walk")

#Create the four lerp intervals needed to walk back and forth
pandaPosInterval1= pandaActor.posInterval(13,pm.Point3(0,-10,0), startPos=pm.Point3(0,10,0))
pandaPosInterval2= pandaActor.posInterval(13,pm.Point3(0,10,0), startPos=pm.Point3(0,-10,0))
pandaHprInterval1= pandaActor.hprInterval(3,pm.Point3(180,0,0), startHpr=pm.Point3(0,0,0))
pandaHprInterval2= pandaActor.hprInterval(3,pm.Point3(0,0,0), startHpr=pm.Point3(180,0,0))

#Create and play the sequence that coordinates the intervals
pandaPace = Sequence(pandaPosInterval1, pandaHprInterval1,
  pandaPosInterval2, pandaHprInterval2, name = "pandaPace")
pandaPace.loop()

pandaPos = pandaActor.getPos()

# Camera
cam = pm.Camera("Isometric")

base.cam.setPos(pandaPos+20)
base.cam.lookAt(pandaActor)

base.run()
