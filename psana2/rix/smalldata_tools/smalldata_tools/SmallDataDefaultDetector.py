# importing generic python modules
import psana
import abc
import numpy as np
try:
    basestring
except NameError:
    basestring = str

#
# classes for default detector types
#
class defaultDetector(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, detname, name, run=None):
        self.name=name
        self.detname=detname
        self._debug = False
        self._run = run
        self.det = None
        if self.inRun():
            if run is None:
                self.det=psana.Detector(detname)
            else:
                self.det=run.Detector(detname)
    def inRun(self):
        dNames=[]
        try:
            detnames = psana.DetNames()
            for dn in detnames:
                for dnn in dn:
                    if dnn!='':
                        dNames.append(dnn)
        except:
            detnames = self._run.detinfo
            for dn in detnames:
                dNames.append(dn[0])
        if self.detname in dNames:
            return True
        return False
    def _setDebug(self, debug):
        self._debug = debug 
    def params_as_dict(self):
        """returns parameters as dictionary to be stored in the hdf5 file (once/file)"""
        parList =  {key:self.__dict__[key] for key in self.__dict__ if (key[0]!='_' and isinstance(getattr(self,key), (basestring, int, float, np.ndarray, tuple))) }
        parList.update({key: np.array(self.__dict__[key]) for key in self.__dict__ if (key[0]!='_' and isinstance(getattr(self,key), list) and len(getattr(self,key))>0 and isinstance(getattr(self,key)[0], (basestring, int, float, np.ndarray))) })
        #remKeys = [key for key in self.__dict__ if (key not in parList)]
        #print('DEBUG: keys which are not parameters:',remKeys)
        #for k in remKeys:
        #    if k[0]!='_':
        #        print k, self.__dict__[k]
        return parList
    @abc.abstractmethod
    def data(self,evt):
        """method that should return a dict of values from event"""

class lightStatus(defaultDetector):
    def __init__(self, codes=[[162],[]], evrName=None):
        if evrName is None:
            evrNames = [ n[0] for  n in psana.DetNames() if ':Evr.' in n[0] ]
            #print('in lightStatus', evrNames)
            if len(evrNames)<1:
                return
            nCodesMax = -1
            for name in evrNames:
                nCodes = psana.Detector(name)._fetch_configs()[0].neventcodes()
                if nCodes > nCodesMax:
                    nCodesMax = nCodes
                    evrName = name
            if nCodesMax < 0:
                return
        defaultDetector.__init__(self, evrName, 'lightStatus')
        self.xrayCodes_drop = [ c for c in codes[0] if c > 0]
        self.laserCodes_drop = [ c for c in codes[1] if c > 0]
        self.xrayCodes_req = [ -c for c in codes[0] if c < 0]
        self.laserCodes_req =  [ -c for c in codes[1] if c < 0]

    def data(self,evt):
        xfel_status, laser_status = (1,1) # default if no EVR code matches
        dl={}
        evtCodes = self.det.eventCodes(evt)
        if evtCodes is not None:
            for xOff in self.xrayCodes_drop:
                if xOff in evtCodes:
                    xfel_status = 0
            for lOff in self.laserCodes_drop:
                if lOff in evtCodes:
                    laser_status = 0
            if len(self.xrayCodes_req)>0 and xfel_status==1:
                xfel_status = 0
                for code in evtCodes:
                    if code in self.xrayCodes_req:
                        xfel_status = 1
            if len(self.laserCodes_req)>0 and laser_status==1:
                laser_status = 0
                for code in evtCodes:
                    if code in self.laserCodes_req:
                        laser_status = 1
        else:
            xfel_status, laser_status = (-1,-1) # default if no EVR code matches
        dl['xray']=xfel_status
        dl['laser']=laser_status
        return dl
        
class ipmDetector(defaultDetector):
    def __init__(self, detname, name=None, savePos=False):
        if name is None:
            self.name = detname
        else:
            self.name = name
        defaultDetector.__init__(self, detname, self.name)
        self.savePos = savePos
    def data(self, evt):
        dl={}
        if self.det.sum(evt) is not None:
            dl['sum']=self.det.sum(evt)
            dl['channels']=self.det.channel(evt)
            if self.savePos:
                dl['xpos']=self.det.xpos(evt)
                dl['ypos']=self.det.ypos(evt)
        return dl

class bmmonDetector(defaultDetector):
    def __init__(self, detname, name=None, savePos=True):
        if name is None:
            self.name = detname
        else:
            self.name = name
        defaultDetector.__init__(self, detname, self.name)
        self.savePos = savePos
    def data(self, evt):
        dl={}
        data = self.det.get(evt)
        dl['sum']=data.TotalIntensity()
        dl['peaks']=data.peakA()
        if self.name=='snd_dio':
            dl['dcc']=dl['peaks'][8]
            dl['dco']=dl['peaks'][9]
            dl['do']=dl['peaks'][10]
            dl['t1d']=dl['peaks'][11]
            dl['dd']=dl['peaks'][12]
            dl['dci']=dl['peaks'][13]
            dl['di']=dl['peaks'][14]
            dl['t4d']=dl['peaks'][15]
        if self.savePos:
            dl['xpos']=data.X_Position()
            dl['ypos']=data.Y_Position()
        return dl

class wave8Detector(defaultDetector):
    def __init__(self, detname, name=None, saveTime=False):
        if name is None:
            self.name = detname
        else:
            self.name = name
        self.saveTime = saveTime
        defaultDetector.__init__(self, detname, self.name)
        cfg = self.det.env.configStore().get(psana.Generic1D.ConfigV0, psana.Source(detname))
        self.wave8_shape = None
        if cfg is not None:
            self.wave8_shape = cfg.Length()

    def data(self, evt):
        dl={}
        raw = self.det.raw(evt)
        if raw is not None:
            for itrace in range(len(raw)):
                dl['ch%02d'%itrace]=raw[itrace]
            if self.saveTime:
                wftime = self.det.wftime(evt)
                for itrace,trace in enumerate(wftime):
                    dl['wftime_ch%02d'%itrace]=wftime
        return dl

class impDetector(defaultDetector):
    def __init__(self, detname, name=None, saveTime=False):
        if name is None:
            self.name = detname
        else:
            self.name = name
        self.saveTime = saveTime
        defaultDetector.__init__(self, detname, self.name)
        cfg = self.det.env.configStore().get(psana.Imp.ConfigV1, psana.Source(detname))
        self.imp_shape = None
        if cfg is not None:
            self.imp_shape = cfg.numberOfSamples()

    def data(self, evt):
        dl={}
        wfs = self.det.waveform(evt)
        if wfs is not None:
            for itrace in range(wfs.shape[0]):
                dl['ch%02d'%itrace]=wfs[itrace]
            if self.saveTime:
                wftime = self.det.wftime(evt)
                dl['wftime']=wftime
        return dl

class epicsDetector(defaultDetector):
    def __init__(self, name='epics', PVlist=[]):
        self.name = name
        self.detname='epics'
        self.PVlist = []
        self.PVlist_PV = []
        self.pvs = []
        enames = psana.DetNames('epics')
        aliases = [k[1] for k in enames if k[1]!='']
        pvnames = [k[0] for k in enames if k[1]!='']
        for pv in PVlist:
            try:
                self.pvs.append(psana.Detector(pv))
                self.PVlist.append(pv)
                self.PVlist_PV.append(pvnames[aliases.index(pv)])
            except:
                print('could not find EPICS PV %s in data'%pv)

    def inRun(self):
        if len(self.pvs)>0:
            return True
        return False

    def data(self,evt):
        dl={}
        for pvname,pv in zip(self.PVlist,self.pvs):
            try:
                dl[pvname]=pv()
                if isinstance(dl[pvname], basestring):
                    dl[pvname]=np.nan
            except:
                #print('we have issues with %s in this event'%pvname)
                pass
        return dl

class encoderDetector(defaultDetector):
    def __init__(self, detname, name=None):
        if name is None:
            self.name = detname
        else:
            self.name = name
        defaultDetector.__init__(self, detname, self.name)
    def data(self, evt):
        dl={}
        if self.det.descriptions() is None:
            dl['ch0']=self.det.values(evt)[0]
        else:
            for desc,value in zip(self.det.descriptions(), self.det.values(evt)):
                if desc!='':
                    dl[desc]=value
        return dl

class controlDetector(defaultDetector):
    def __init__(self, name='scan'):
        defaultDetector.__init__(self, 'ControlData', 'scan')
        try:
            self.stepPV = psana.Detector('scan_current_step')
        except:
            try:
                self.stepPV = psana.Detector('Scan_current_step')
            except:
                self.stepPV = None
    def data(self, evt):
        dl={}
        if self.stepPV is not None:
            dl['varStep']=self.stepPV()
        for icpv,cpv in enumerate(self.det().pvControls()):
            dl['var%d'%icpv]=cpv.value()
            #this can lead to issues with utf-8 encoded python3 strings.....
            #dl[(cpv.name()).decode('utf-8', errors='ignore').encode('ascii')]=cpv.value()
            dl[cpv.name()]=cpv.value()
        return dl

class aiDetector(defaultDetector):
    def __init__(self, detname, name=None):
        if name is None:
            self.name = detname
        else:
            self.name = name
        defaultDetector.__init__(self, detname, self.name)
        self.aioInfo = [[ i for i in range(0,16)], [ 'ch%02d'%i for i in range(0,16)], [ 1. for i in range(0,16)], [ 0. for i in range(0,16)]]

    def setPars(self, AIOPars):
        if len(AIOPars)<2:
            print('need 2/3 lists: channel#, user-friendly names & conversion factors (optional)')
            return
        self.aioInfo[0] = AIOPars[0]
        self.aioInfo[1] = AIOPars[1]
        if len(AIOPars)>=3:
            self.aioInfo[2] = AIOPars[2]
            if len(AIOPars)==4:
                self.aioInfo[3] = AIOPars[3]
            else:
                self.aioInfo[3] = [0. for entry in AIOPars[0]]
        else:
            self.aioInfo[2] = [1. for entry in AIOPars[0]]

    def data(self, evt):
        dl={}
        for ichn,chName,chnScale,chnOffset in zip(self.aioInfo[0], self.aioInfo[1], self.aioInfo[2], self.aioInfo[3]):
            try: 
                dl[chName]=self.det.get(evt).channelVoltages()[ichn]*chnScale+chnOffset
            except:
                break
        return dl

class adcDetector(defaultDetector):
    def __init__(self, detname, name=None):
        if name is None:
            self.name = detname
        else:
            self.name = name
        defaultDetector.__init__(self, detname, self.name)

    def data(self, evt):
        dl={}
        for ichn,chv in enumerate(self.det.get(evt).channelValue()):
            dl['ch%d'%ichn]=chv
        return dl

class feeBldDetector(defaultDetector):
    def __init__(self, detname, name=None):
        if name is None:
            self.name = detname
        else:
            self.name = name
        defaultDetector.__init__(self, detname, self.name)

    def data(self, evt):
        dl={}
        dl['hproj'] = self.det.get(evt).hproj()
        return dl

class ttDetector(defaultDetector):
    def __init__(self, name='tt', baseName='TTSPEC:'):
        self.name = name
        self.detname='epics'
        self.ttNames = ['FLTPOS','FLTPOS_PS','AMPL','FLTPOSFWHM','REFAMPL','AMPLNXT']
        self.PVlist = [ baseName+pvname for pvname in self.ttNames ]
        self.pvs=[]
        for pv in self.PVlist:
            try:
                self.pvs.append(psana.Detector(pv))
            except:
                print('could not find timetool EPICS PV %s in data'%pv)
        self.ttCalib=None
    def inRun(self):
        if len(self.pvs)>0:
            return True
        return False
    def setPars(self, calibPars):
      if calibPars != None:
        self.ttCalib = calibPars

    def data(self,evt):
        dl={}
        for ttname,pvname,pv in zip(self.ttNames,self.PVlist,self.pvs):
            dl[ttname]=pv()
        if self.ttCalib is None:
            dl['ttCorr']= dl['FLTPOS_PS']
        else:
            ttOrg = dl['FLTPOS']
            dl['ttCorr']=self.ttCalib[0] + self.ttCalib[1]*ttOrg
            if len(self.ttCalib)>2:
                dl['ttCorr']+=ttOrg*ttOrg*self.ttCalib[2]
            #pixel 0 is special:
            #it indicates that fit was not attempted/unsuccessful
            if ttOrg == 0:
                dl['ttCorr']=np.nan
        return dl

class damageDetector(defaultDetector):
    def __init__(self, name='damage'):
        self.name = name
        self.detNames=[]
        for dn in psana.DetNames():
            if dn[1]!='':
                self.detNames.append(dn[1])
            else:
                self.detNames.append(dn[0])
        self.detAlias=[ det for det in self.detNames]
    def inRun(self):
        return True
    def setPars(self, detList):
        for det in detList:
            try:
                if det.detname in self.detNames:
                    self.detAlias[self.detNames.index(det.detname)]=det.name
            except:
                pass    
    def data(self,evt):
        #check if detectors are in event
        dl={}
        aliases = [ k.alias() for k in evt.keys() ]
        srcNames = [ k.src().__str__().replace(')','').replace('BldInfo(','').replace('DetInfo(','') for k in evt.keys() ]
        for det,alias in zip(self.detNames,self.detAlias):
            val=0
            if det in aliases:
                val=1
            elif det in srcNames:
                val=1
            dl[det.replace('-','_')]=val
            if alias!=det:
                dl[alias.replace('-','_')]=val
        return dl

#no psana detector for this. Need to code 'from scratch'
class l3tDetector(object):
    def __init__(self, name=None):
        if name is None:
            self.name = 'l3t'
        else:
            self.name = name

        #self.det=psana.Detector(detname)
        self._debug = False

    #rely on fail save
    def inRun(self):
        return True

    def _setDebug(self, debug):
        self._debug = debug

    def params_as_dict(self):
        return {'name': self.name}

    def data(self, evt):
        dl={}
        try:
            l3t = evt.get(psana.L3T.DataV2,psana.Source(''))
            if l3t is not None:
                dl['accept']=l3t.accept()
        except:
            pass
        return dl

#
# needs testing with data.
#
class ttRawDetector(defaultDetector):
    def __init__(self, name='ttRaw', env=None):
        self.name = name
        self.detname = ''
        self.kind='stepDown'
        self.weights=None
        self.ttROI_signal=None
        self.ttROI_sideband=None
        self.ttROI_reference=None
        self.ttProj=False
        self.runningRef=None
        self.refitData=False
        self.useProjection=False
        self.beamOff=[]
        self.laserOff=[]
        self.sb_convergence=1.
        self.ref_convergence=1.
        self.subtract_sideband=False
        self.ttCalib = [0.,1.]
        ttCfg=None
        self.evrdet=psana.Detector('NoDetector.0:Evr.0')
        if env is None:
            env = psana.Env
            #getting the env this way unfortunatly does not work. Find out how psana.DetNames() does it.
            return
        for cfgKey in env.configStore().keys():
            if cfgKey.type() == psana.TimeTool.ConfigV2:
                ttCfg = env.configStore().get(psana.TimeTool.ConfigV2, cfgKey.src())
                self.detname = cfgKey.alias()
                defaultDetector.__init__(self, self.detname, 'ttRaw')
            elif cfgKey.type() == psana.TimeTool.ConfigV3:
                ttCfg = env.configStore().get(psana.TimeTool.ConfigV3, cfgKey.src())
                self.detname = cfgKey.alias()
                defaultDetector.__init__(self, self.detname, 'ttRaw')
        if ttCfg is not None:
            self.ttProj=ttCfg.write_projections()
            self.ttROI_signal = [[ttCfg.sig_roi_lo().row(),ttCfg.sig_roi_hi().row()],\
                                 [ttCfg.sig_roi_lo().column(),ttCfg.sig_roi_hi().column()]]
            self.ttROI_sideband = [[ttCfg.sb_roi_lo().row(),ttCfg.sb_roi_hi().row()],\
                                   [ttCfg.sb_roi_lo().column(),ttCfg.sb_roi_hi().column()]]
            if ttCfg.use_reference_roi()>0:
                self.ttROI_reference = [[ttCfg.ref_roi_lo().row(),ttCfg.ref_roi_hi().row()],\
                                        [ttCfg.ref_roi_lo().column(),ttCfg.ref_roi_hi().column()]]
            else:
                self.ttROI_reference = self.ttROI_signal

            self.weights = ttCfg.weights()
            self.sb_convergence=ttCfg.sb_convergence()
            self.ref_convergence=ttCfg.ref_convergence()
            self.subtract_sideband=ttCfg.subtract_sideband()
            self.ttCalib = ttCfg.calib_poly()
                
            for el in ttCfg.beam_logic():
                self.beamOff.append(el.event_code())
            for el in ttCfg.laser_logic():
                self.laserOff.append(el.event_code())
        else:
            defaultDetector.__init__(self, self.detname, 'ttRaw')
            
    def inRun(self):
        if self.detname=='':
            return False

    def setPars(self, ttPars):
        if 'ttProj' in ttPars.keys():
            self.ttProj=ttPars['ttProj']
        if 'ttROI_signal' in ttPars.keys():
            self.ttROI_signal=ttPars['ttROI_signal']
        if 'ttROI_reference' in ttPars.keys():
            self.ttROI_reference=ttPars['ttROI_reference']
        if 'ttROI_sideband' in ttPars.keys():
            self.ttROI_sideband=ttPars['ttROI_sideband']
        if 'weights' in ttPars.keys():
            self.weights=ttPars['weights']
        if 'runningRef' in ttPars.keys():
            self.runningRef=ttPars['runningRef']
        if 'refitData' in ttPars.keys():
            self.refitData=ttPars['refitData']
        if 'useProjection' in ttPars.keys():
            self.useProjection=ttPars['useProjection']
        if 'sb_convergence' in ttPars.keys():
            self.sb_convergence=ttPars['sb_convergence']
        if 'ref_convergence' in ttPars.keys():
            self.ref_convergence=ttPars['ref_convergence']
        if 'subtract_sideband' in ttPars.keys():
            self.subtract_sideband=ttPars['subtract_sideband']
        if 'ttCalib' in ttPars.keys():
            self.ttCalib=ttPars['ttCalib']

    def data(self, evt):
        retDict = self.getTraces(evt)
        if not self.refitData:
            return retDict
        data = self.prepareTrace(evt, retDict)
        fitDict = self.fitTraceData(data)
        for key in fitDict:
            retDict[key] = fitDict[key]
        return retDict

    def getTraces(self, evt):
        #check that we have reference, otherwise replace by none
        evtCodes = self.evrdet.eventCodes(evt)
        ttDet=self.det
        ttData={}
        ttData['tt_signal']=np.zeros(abs(self.ttROI_signal[1][1]-self.ttROI_signal[1][0]))
        if self.ttROI_sideband is not None:
            ttData['tt_sideband']=np.zeros(abs(self.ttROI_sideband[1][1]-self.ttROI_sideband[1][0]))
        if self.ttROI_reference is not None:
            ttData['tt_reference']=np.zeros(abs(self.ttROI_reference[1][1]-self.ttROI_reference[1][0]))
        for lOff in self.laserOff:
            if lOff in evtCodes:
                if self._debug:
                    print('ttRaw: laser off event!')
                return ttData
            
        try:
            ttData['tt_signal_pj']=ttDet.projected_signal().astype(dtype='uint32').astype(float)
            ttData['tt_sideband_pj']=ttDet.projected_sideband().astype(dtype='uint32').astype(float)
            ttData['tt_reference_pj']=ttDet.projected_reference().astype(dtype='uint32').astype(float)
        except:
            pass
        ttImg = ttDet.raw(evt)
        if self.ttROI_signal is not None:
            ttData['tt_signal']=ttImg[self.ttROI_signal[0][0]:self.ttROI_signal[0][1],self.ttROI_signal[1][0]:self.ttROI_signal[1][1]].mean(axis=0)          
        if self.ttROI_sideband is not None:
            ttData['tt_sideband']=ttImg[self.ttROI_sideband[0][0]:self.ttROI_sideband[0][1],self.ttROI_sideband[1][0]:self.ttROI_sideband[1][1]].mean(axis=0)
        if self.ttROI_reference is not None:
            beamOff=False
            for bOff in self.beamOff:
                if bOff in evtCodes:
                    beamOff=True
            if beamOff:
                ttRef = ttImg[self.ttROI_reference[0][0]:self.ttROI_reference[0][1],self.ttROI_reference[1][0]:self.ttROI_reference[1][1]].mean(axis=0)
                if self.runningRef is None:
                    self.runningRef=ttRef
                else:
                    self.runningRef=ttRef*self.ref_convergence + self.runningRef*(1.-self.ref_convergence)
                #print('update self.runningRef')
                ttData['tt_reference']=self.runningRef        
        return ttData

    def prepareTrace(self, evt, ttData=None):
        if ttData is None:
            ttData = self.getTraces(evt)
            if len(ttData.keys())==0:
                return None

        if self.useProjection:
            ttRef=ttData['tt_reference_pj']
            ttSignal=ttData['tt_signal_pj']
            if self.subtract_sideband>0:
                ttSignal-=ttData['tt_sideband_pj']
                ttRef-=ttData['tt_sideband_pj']
        else:
            ttRef=ttData['tt_reference'].copy()
            ttSignal=ttData['tt_signal']
            if self.subtract_sideband>0:
                ttSignal-=ttData['tt_sideband']
                ttRef-=ttData['tt_sideband']

        if ttData['tt_reference'].sum()==0:
            nanArray = np.ones(ttData['tt_reference'].shape[0])
            nanArray=nanArray*np.nan
            return nanArray

        return ttSignal/ttRef

    def fitTraceData(self, data):
        if data is None or len(data)<10:
            return
        lf = len(self.weights)
        halfrange = round(lf/10)
        retDict = {}
        retDict['pos']=0.
        retDict['amp']=0.
        retDict['fwhm']=0.
        retDict['pos_ps']=0.
        if np.isnan(data).sum()==data.shape[0]:
            return retDict
        
        f0 = np.convolve(np.array(self.weights).ravel(),data,'same')
        f = f0[lf/2:len(f0)-lf/2-1]
        retDict['f']=f
        if (self.kind=="stepDown"):
            mpr = f.argmin()
        else:
            mpr = f.argmax()
        # now do a parabolic fit around the max
        xd = np.arange(max(0,mpr-halfrange),min(mpr+halfrange,len(f)-1))
        yd = f[max(0,mpr-halfrange):min(mpr+halfrange,len(f)-1)]
        p2 = np.polyfit(xd,yd,2)
        tpos = -p2[1]/2./p2[0]
        tamp = np.polyval(p2,tpos)
        try:
            if self.kind == 'stepDown':
                beloh = (f>((f[-25:].mean()+tamp)/2.)).nonzero()[0]-mpr
            else:
                beloh = (f<tamp/2).nonzero()[0]-mpr            
            #print('beloh ',len(beloh[beloh<0]),len(beloh[beloh>0]))
            tfwhm = abs(beloh[beloh<0][-1]-beloh[beloh>0][0])
        except:
            tfwhm = 0.
        if self.kind == 'stepDown':
            tamp = abs(f[-25:].mean()-tamp)
        retDict['pos']=tpos + lf/2.
        retDict['amp']=tamp
        if np.isnan(tamp): 
            retDict['fwhm']=np.nan
        else:
            retDict['fwhm']=tfwhm 
        ttOrg = retDict['pos']
        ttCorr = self.ttCalib[0]+ ttOrg*self.ttCalib[1]
        if len(self.ttCalib)>2:
            ttCorr+=ttOrg*ttOrg*self.ttCalib[2]
        retDict['pos_ps']=ttCorr
        #for k in retDict.keys():
        #    print('ret ',k,retDict[k])

        return retDict

class xtcavDetector(defaultDetector):
    def __init__(self, name='xtcav', detname='xtcav'):
        self.name = name
        self.detname = detname
        self.nb=1
        self.size=5000
        if Xtcav is None:
            return None
        self.ShotToShotCharacterization = Xtcav.ShotToShotCharacterization()
    def setEnv(self, env):
        self.ShotToShotCharacterization.SetEnv(env)
    def setPars(self, xtcavPars):
        self.nb=xtcavPars[0]
        self.size=xtcavPars[1]
    def data(self,evt):
        #check if detectors are in event
        dl={}
        xtcav_success=False
        arSize=0
        agreement=-2
        timeAr=np.array([np.nan] * self.size)
        power=np.array([np.nan] * self.size)
        ragged_time=np.array([], dtype='float32')
        ragged_power=np.array([], dtype='float32')
        #self.ShotToShotCharacterization.SetCurrentEvent(evt)
        if self.ShotToShotCharacterization.SetCurrentEvent(evt):
            agreement=-1
            timeArOrg,power,ok=self.ShotToShotCharacterization.XRayPower()
            if ok:
              arSize=timeArOrg[0].shape[0]
              agreement,ok=self.ShotToShotCharacterization.ReconstructionAgreement()
              xtcav_success=True
              ragged_time = timeArOrg
              ragged_power = power
              if arSize>=1 and arSize<=self.size:
                  timeAr = np.append(timeArOrg[0],np.array([np.nan] * (self.size-arSize)))
                  power = np.append(power[0],np.array([np.nan] * (self.size-arSize)))
              else:
                print('Xtcav array is too small in run, please check littleData configuration',env.run())
                time = timeArOrg[:self.size]
                power = power[:self.size]

        dl['agreement']=agreement
        dl['arSize']=arSize
        dl['time']=timeAr
        dl['power']=power
        #dl['ragged_time']=ragged_time
        #dl['ragged_power']=ragged_power
        return dl

class gmdDetector(defaultDetector):
    def __init__(self,  name=None):
        if name is None:
            self.name = 'GMD'
        else:
            self.name = name
        defaultDetector.__init__(self, 'GMD', self.name)

    def data(self, evt):
        dl={}
        raw = self.det.get(evt)
        if raw is not None:
           fields = [ field for field in dir(raw) if (field[0]!='_' and field!='TypeId' and field!='Version') ]
           for field in fields:
               dl[field]=getattr(raw, field)()
        return dl

class eorbitsDetector(defaultDetector):
    def __init__(self, name=None):
        if name is None:
            self.name = 'EOrbits'
        else:
            self.name = name
        defaultDetector.__init__(self, 'EOrbits', self.name)
    def data(self, evt):
        dl={}
        detData = self.det.get(evt)
        if detData is not None:
           fields = [ field for field in dir(detData) if (field[0]!='_' and field!='TypeId' and field!='Version') ]
           for field in fields:
               dl[field]=getattr(detData, field)()
        return dl

#
# detector classes for running in shared memory mode
# mpiData fields are not available here.
#

class ebeamDetector(defaultDetector):
    def __init__(self, name=None):
        if name is None:
            self.name = 'ebeam'
        else:
            self.name = name
        defaultDetector.__init__(self, 'EBeam', self.name)
    def data(self, evt):
        dl={}
        ebeamData = self.det.get(evt)
        if ebeamData is not None:
            fields = [ field for field in dir(ebeamData) if (field[0]!='_' and field!='TypeId' and field!='Version') ]
            for field in fields:
                dl[field]=getattr(ebeamData, field)()
        return dl

class gasDetector(defaultDetector):
    def __init__(self, name=None):
        if name is None:
            self.name = 'gas_detector'
        else:
            self.name = name
        defaultDetector.__init__(self, 'FEEGasDetEnergy', self.name)
    def data(self, evt):
        dl={}
        gdetData = self.det.get(evt)
        if gdetData is not None:
           fields = [ field for field in dir(gdetData) if (field[0]!='_' and field!='TypeId' and field!='Version') ]
           for field in fields:
               dl[field]=getattr(gdetData, field)()
        return dl
#
#
#
class genlcls2Detector(defaultDetector):
    def __init__(self,  name=None, run=None, h5name=None):
        if name is None:
            self.name = 'anydet'
        else:
            self.name = name
        if h5name is None: h5name = self.name
        defaultDetector.__init__(self, self.name, h5name, run)

    def data(self, evt):
        dl={}
        raw =getattr( self.det, 'raw')
        if raw is not None:
           fields = [ field for field in dir(raw) if (field[0]!='_' and field!='TypeId' and field!='Version') ]
           for field in fields:
               if getattr(raw, field)(evt) is None: continue
               dl[field]=getattr(raw, field)(evt)
               if isinstance(dl[field], list): dl[field]=np.array(dl[field])
        return dl

class ttlcls2Detector(defaultDetector):
    def __init__(self,  name=None, run=None, saveTraces=False):
        if name is None:
            self.name = 'anydet'
        else:
            self.name = name
        self.saveTraces = saveTraces
        defaultDetector.__init__(self, self.name, 'tt', run)

    def data(self, evt):
        dl={}
        fex=getattr( self.det, 'ttfex')
        veto_fields = ['TypeId', 'Version', 'calib', 'image', 'raw' ]
        if fex is not None:
           fields = [ field for field in dir(fex) if (field[0]!='_' and field not in veto_fields) ]
           for field in fields:
               if getattr(fex, field)(evt) is None: continue
               dl[field]=getattr(fex, field)(evt)
               if isinstance(dl[field], list): dl[field]=np.array(dl[field])

        if self.saveTraces:
            fex=getattr( self.det, 'ttproj')
            veto_fields = ['TypeId', 'Version', 'calib', 'image', 'raw' ]
            if fex is not None:
               fields = [ field for field in dir(fex) if (field[0]!='_' and field not in veto_fields) ]
               for field in fields:
                   if getattr(fex, field)(evt) is None: continue
                   dl[field]=getattr(fex, field)(evt)
                   if isinstance(dl[field], list): dl[field]=np.array(dl[field])        
        return dl

class fimfexDetector(defaultDetector):
    def __init__(self,  name=None, run=None):
        if name is None:
            self.name = 'anydet'
        else:
            self.name = name
        defaultDetector.__init__(self, self.name, self.name, run)

    def data(self, evt):
        dl={}
        fex=getattr( self.det, 'fex')
        veto_fields = []#'TypeId', 'Version', 'calib', 'image', 'raw' ]
        if fex is not None:
           fields = [ field for field in dir(fex) if (field[0]!='_' and field not in veto_fields) ]
           for field in fields:
               if getattr(fex, field)(evt) is None: continue
               dl[field]=getattr(fex, field)(evt)
               if isinstance(dl[field], list): dl[field]=np.array(dl[field])
        return dl

class lcls2_lightStatus(defaultDetector):
    def __init__(self, codes, run):
        defaultDetector.__init__(self, 'timing', 'lightStatus', run)
        self.xrayCodes_drop = [ c for c in codes[0] if c > 0]
        self.laserCodes_drop = [ c for c in codes[1] if c > 0]
        self.xrayCodes_req = [ -c for c in codes[0] if c < 0]
        self.laserCodes_req =  [ -c for c in codes[1] if c < 0]

    def data(self,evt):
        xfel_status, laser_status = (1,1) # default if no EVR code matches
        dl={}
        evtCodes = getattr(getattr( self.det, 'raw'), 'eventcodes')(evt)
        if evtCodes is not None:
            for xOff in self.xrayCodes_drop:
                if evtCodes[xOff]:
                    xfel_status = 0
            for lOff in self.laserCodes_drop:
                if evtCodes[lOff]:
                    laser_status = 0
            if len(self.xrayCodes_req)>0 and xfel_status==1:
                xfel_status = 0
                for xOff in self.xrayCodes_req:
                    if evtCodes[xOff]:
                        xfel_status = 1
            if len(self.laserCodes_req)>0 and laser_status==1:
                laser_status = 0
                for lOff in self.laserCodes_req:
                    if evtCodes[lOff]:
                        laser_status = 1

        else:
            xfel_status, laser_status = (-1,-1) # default if no EVR code matches
        dl['xray']=xfel_status
        dl['laser']=laser_status
        return dl

class lcls2_epicsDetector(defaultDetector):
    def __init__(self, name='epics', PVlist=[],run=None):
        self.name = name
        self.detname='epics'
        self.PVlist = []
        self.pvs = []
        for pv in PVlist:
            try:
                self.pvs.append(run.Detector(pv))
                self.PVlist.append(pv)
            except:
                print('could not find LCLS2 EPICS PV %s in data'%pv)

    def inRun(self):
        if len(self.pvs)>0:
            return True
        return False

    def data(self,evt):
        dl={}
        for pvname,pv in zip(self.PVlist,self.pvs):
            try:
                if pv(evt) is not None:
                    dl[pvname]=pv(evt)
                    if isinstance(dl[pvname], basestring):
                        dl[pvname]=np.nan
            except:
                #print('we have issues with %s in this event'%pvname)
                pass
        return dl

    def params_as_dict(self):
        """returns parameters as dictionary to be stored in the hdf5 file (once/file)"""
        parList =  {key:self.__dict__[key] for key in self.__dict__ if (key[0]!='_' and isinstance(getattr(self,key), (basestring, int, float, np.ndarray, tuple))) }
        PVlist = getattr(self,'PVlist')
        parList.update({'PV_%d'%ipv: pv for ipv,pv in enumerate(PVlist) if pv is not None})

class scanDetector(defaultDetector):
    def __init__(self, name='scan',run=None):
        self.name = name
        self.detname='scan'
        self.scans = []
        self.scanlist = []
        vetolist = ['step_docstring']
        try:
            scanlist = [k[0] for k in run.scaninfo if k[0] not in vetolist]
            for scan in scanlist:
                try:
                    self.scans.append(run.Detector(scan))
                    self.scanlist.append(scan)
                except:
                    print('could not find LCLS2 EPICS PV %s in data'%pv)
        except:
            pass

    def inRun(self):
        if len(self.scans)>0:
            return True
        return False

    def data(self,evt):
        dl={}
        for scanname,scan in zip(self.scanlist,self.scans):
            try:
                if scan(evt) is not None:
                    dl[scanname]=scan(evt)
                    if isinstance(dl[scanname], basestring):
                        dl[scanname]=np.nan
            except:
                #print('we have issues with %s in this event'%scanname)
                pass
        return dl
