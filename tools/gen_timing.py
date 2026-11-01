"""Approximate phrase timing inside MEASURED speech segments (ffmpeg silencedetect -35dB/0.25s).
Segment boundaries are measured. Phrase times inside a segment are ESTIMATES
(proportional to non-space character count), not recognised word timestamps."""
import re, json, sys, os
GOLD = "#FFC93C"
# seg_id: (start, end, [phrases], gold keywords)
SEG = {
 1:(0.00,5.53,["के तपाईंको Social Media Account मा","Followers, Likes र Views","एकदमै कम छन्?"],["Followers","Likes","Views","कम"]),
 3:(6.93,10.03,["आफ्नो Video मा राम्रो Views","नआएर चिन्तित हुनुहुन्छ?"],["Views","चिन्तित"]),
 5:(11.40,13.34,["त्यसो भए","अब चिन्ता नगर्नुहोस्!"],["चिन्ता नगर्नुहोस्"]),
 6:(13.74,17.99,["किनकि NEXORA ले ल्याएको छ एउटा विशेष","FREE PROMOTION CAMPAIGN!"],["NEXORA","FREE PROMOTION CAMPAIGN"]),
 7:(18.34,24.61,["हामी पहिलो ५० जना भाग्यशाली व्यक्तिहरूलाई","Free मा आफ्नो पहिलो Video","Promote गर्ने अवसर दिँदैछौँ!","तपाईंले गर्नुपर्ने यति मात्रै हो:"],["५०","Free","Video","Promote"]),
 8:(25.05,26.91,["यो Video लाई Like गर्नुहोस्।"],["Like"]),
 9:(27.26,28.90,["आफ्ना १० जना साथीहरूलाई Mention गर्नुहोस्।"],["१०","Mention"]),
 10:(29.24,31.79,["अनि आफ्नो Story मा Repost गर्नुहोस्।"],["Repost"]),
 11:(32.07,34.52,["साथै NEXORA को Official Page Follow गर्न नभुल्नुहोला!"],["NEXORA","Follow"]),
 12:(34.88,38.50,["चयन भएका ५० जनालाई","हामी DM मार्फत सम्पर्क गर्नेछौँ।"],["५०","DM"]),
 13:(38.95,42.70,["NEXORA – Upgrade Your Digital Life!"],["NEXORA","Upgrade Your Digital Life"]),
}
TRIG = [(1,"Followers"),(1,"Likes"),(1,"Views"),(1,"एकदमै कम"),(3,"Views"),(3,"चिन्तित"),(5,"अब चिन्ता"),
 (6,"NEXORA"),(6,"FREE PROMOTION"),(7,"५० जना"),(7,"Free मा"),(7,"पहिलो Video"),(7,"Promote"),(7,"तपाईंले"),
 (8,"Like"),(9,"१० जना"),(9,"Mention"),(10,"Story"),(10,"Repost"),(11,"NEXORA"),(11,"Official"),(11,"Follow"),
 (12,"५० जनालाई"),(12,"DM"),(13,"NEXORA"),(13,"Upgrade")]
nz=lambda s:len(s.replace(" ",""))
def span(seg):
    s,e,ph,_=SEG[seg]; full=" ".join(ph); tot=nz(full); d=e-s
    return s,d,full,tot
def t_of(seg,sub):
    s,d,full,tot=span(seg); i=full.index(sub); return s+d*nz(full[:i])/tot
def ts(t):
    ms=round(t*1000); return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"
def build(gold):
    out=[];n=1
    for seg,(s,e,ph,kw) in SEG.items():
        tot=sum(nz(p) for p in ph); t=s
        for i,p in enumerate(ph):
            te=e if i==len(ph)-1 else t+(e-s)*nz(p)/tot
            txt=p
            if gold:
                for k in sorted(kw,key=len,reverse=True):
                    txt=re.sub(re.escape(k),lambda m:f'<font color="{GOLD}"><b>{m.group(0)}</b></font>',txt,count=1) if k in txt and "<font" not in txt.split(k)[0][-30:] else txt
            out.append(f"{n}\n{ts(t)} --> {ts(te)}\n{txt}\n"); n+=1; t=te
    return "\n".join(out)
root=sys.argv[1]
open(f"{root}/subtitles/nexora_ne_plain.srt","w",encoding="utf-8").write(build(False))
open(f"{root}/subtitles/nexora_ne_gold_tags.srt","w",encoding="utf-8").write(build(True))
for seg,w in TRIG: print(f"seg{seg:>2} {w:<16} ~{t_of(seg,w):6.2f}s")
