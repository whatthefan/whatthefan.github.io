import sherpa_onnx, numpy as np, wave, json, sys
M='/tmp/claude-0/sherpa-onnx-whisper-small/'
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M+'small-encoder.int8.onnx',decoder=M+'small-decoder.int8.onnx',tokens=M+'small-tokens.txt',language='es',task='transcribe',num_threads=4)
f=sys.argv[1]; w=wave.open(f); x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
# energía para detectar voz (10 ms)
e=np.sqrt(np.convolve(x**2,np.ones(160)/160,'same'))[::160]
thr=max(0.012,np.percentile(e,30)*2.2)
voz=e>thr
# tramos de voz
tr=[];i=0;n=len(voz)
while i<n:
    if voz[i]:
        j=i
        while j<n and (voz[j] or (j+25<n and voz[j:j+25].any())): j+=1
        if j-i>8: tr.append((i/100,j/100))
        i=j
    else: i+=1
# transcribir cada tramo
out=[]
for a,b in tr:
    s=r.create_stream(); s.accept_waveform(16000,x[int(a*16000):int(b*16000)]); r.decode_stream(s)
    out.append({'a':round(a,2),'b':round(b,2),'txt':s.result.text.strip()})
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
for o in out: print(o)
