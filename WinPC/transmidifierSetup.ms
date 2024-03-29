<!DOCTYPE MIDIRoutingSetupDocument>
<MIDIRoutingSetup showingInnards="1" activeRouteName="Program change" name="no name" documentVersion="1.0">
 <MIDIRoutes>
  <MIDIRoute showingInnards="1" midiPortName="VoiceLive 3" midiChannelIndex="127" outputActivationMethod="112" outputActivationSpecificity="0" colorLabelIndex="-1" name="Sustain">
   <MIDIOutputs>
    <MIDIOutput showingInnards="1" isActive="1" mainActivationValue="0" activationRangeValue="0" colorLabelIndex="-1" name="Output1">
     <MIDIPatchTargets>
      <MIDIPatchTarget showingInnards="1" midiOutputPortName="Springbeats vMIDI1" messageDelayType="0" muted="0" midiChannelIndex="127" colorLabelIndex="-1" messageDelay="0" name="Patch1">
       <MIDIPatchInitializers/>
       <MIDIDataTransforms>
        <MIDIDataTransform showingInnards="1" valueMapping=" &#x9;&#xa;&#xd; !&quot;#$%&amp;'()*+,-./0123456789:;&lt;=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~" int1="0" byte1="110" int2="0" bypass="0" byte2="64" byte3="0" editorPositionX="551" editorPositionY="267" name="Change CC#"/>
        <MIDIDataTransform showingInnards="1" valueMapping="~~~                                                            " int1="0" byte1="1" int2="0" bypass="0" byte2="0" byte3="0" editorPositionX="367" editorPositionY="113" name="CC Map"/>
       </MIDIDataTransforms>
      </MIDIPatchTarget>
     </MIDIPatchTargets>
    </MIDIOutput>
   </MIDIOutputs>
  </MIDIRoute>
  <MIDIRoute showingInnards="1" midiPortName="VoiceLive 3" midiChannelIndex="127" outputActivationMethod="1" outputActivationSpecificity="0" colorLabelIndex="-1" name="Program change">
   <MIDIOutputs>
    <MIDIOutput showingInnards="1" isActive="0" mainActivationValue="0" activationRangeValue="0" colorLabelIndex="-1" name="Output1">
     <MIDIPatchTargets>
      <MIDIPatchTarget showingInnards="1" midiOutputPortName="Springbeats vMIDI1" messageDelayType="0" muted="0" midiChannelIndex="127" colorLabelIndex="-1" messageDelay="0" name="Patch1">
       <MIDIPatchInitializers/>
       <MIDIDataTransforms/>
      </MIDIPatchTarget>
     </MIDIPatchTargets>
    </MIDIOutput>
    <MIDIOutput showingInnards="1" isActive="1" mainActivationValue="1" activationRangeValue="1" colorLabelIndex="-1" name="Output2">
     <MIDIPatchTargets>
      <MIDIPatchTarget showingInnards="1" midiOutputPortName="Springbeats vMIDI2" messageDelayType="0" muted="0" midiChannelIndex="127" colorLabelIndex="-1" messageDelay="0" name="Patch1">
       <MIDIPatchInitializers/>
       <MIDIDataTransforms/>
      </MIDIPatchTarget>
     </MIDIPatchTargets>
    </MIDIOutput>
   </MIDIOutputs>
  </MIDIRoute>
 </MIDIRoutes>
</MIDIRoutingSetup>
