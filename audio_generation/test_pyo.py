# Installed pyo==0.7.7 via http://ajaxsoundstudio.com/pyodoc/compiling.html:
# git clone https://github.com/belangeo/pyo.git
# cd pyo
# python setup.py install --install-layout=deb
from time import sleep
from pyo import *
s = Server()
# 12 = pulse, get all numbers by pa_list_devices()
s.setOutputDevice(12)
s = s.boot()
s.start()

wav = SquareTable()
env = CosTable([(0,0), (100,1), (500,.3), (8191,0)])
met = Metro(.125, 12).play()
amp = TrigEnv(met, table=env, mul=.1)
pit = TrigXnoiseMidi(met, dist='loopseg', x1=20, scale=1, mrange=(48,84))
out = Osc(table=wav, freq=pit, mul=amp).out()

sleep(10)
