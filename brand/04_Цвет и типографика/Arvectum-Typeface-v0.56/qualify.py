from pathlib import Path
import sys,json,subprocess,html
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'Arvectum-Typeface-v0.49'))
from pipeline import Family,verify,sha,write_json,digest_tree,ellipse,rect,add,move,get,box,svg
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
def ring(outer,inner):
    p=RecordingPen();outer.replay(p);inner.replay(ReverseContourPen(p));return p
def correct_counters(f):
    t=f.t;k=f.k;radius=690;cx=radius+25;cy=745
    for c,inner in [('©','C'),('®','R')]:
        shape=ring(ellipse(cx,cy,radius,radius,k),
                   ellipse(cx,cy,radius-t*.72,radius-t*.72,k))
        letter=get(f.f,inner);b=box(letter);sc=min(670/(b[2]-b[0]),855/(b[3]-b[1]))
        form=add(shape,move(letter,cx-(b[0]+b[2])/2*sc,cy-(b[1]+b[3])/2*sc,sc,sc))
        name=f.f.getBestCmap()[ord(c)];w,lsb=f.h.metrics[name]
        f.put(c,form,width=w,lsb=lsb,note='v0.56 QA repair: reversed counter orientation')
    w=1060;h=1490
    section=ring(ellipse(w*.48,h*.67,w*.48,h*.33,k),ellipse(w*.48,h*.67,w*.48-t,h*.33-t,k))
    glyph=add(section,rect(w*.50,0,t,1150),rect(w*.80,0,t,1490))
    name=f.f.getBestCmap()[ord('¶')];ww,ll=f.h.metrics[name]
    f.put('¶',glyph,width=ww,lsb=ll,note='v0.56 QA repair: reversed counter orientation')
    mark=ring(ellipse(0,145,152,145,k),ellipse(0,145,65,58,k))
    c='\u030a';name=f.f.getBestCmap()[ord(c)]
    pen=T2CharStringPen(0,None);mark.replay(pen);cs=pen.getCharString()
    cs.private=f.cff.Private;cs.globalSubrs=f.f['CFF '].cff.GlobalSubrs
    f.cff.CharStrings.charStringsIndex.items[f.cff.CharStrings.charStrings[name]]=cs
    assert f.h.metrics[name][0]==0
    svg(f.output.parent.parent/'glyphs'/f.style/f'U+{ord(c):04X}.svg',mark)
    f.scope[c]={'type':'fixed_counter','codepoint':'U+030A','width':0,'note':'same mark anchor and advance'}
r={};fontfiles={}
for st in ('Display','Text'):
    src=next((P.parent/'Arvectum-Typeface-v0.55/experimental').glob(f'Arvectum{st}*.otf'))
    out=P/'experimental'/('Arvectum'+st+'GoldenStepDraft056-'+('Medium' if st=='Display' else 'Regular')+'.otf')
    f=Family(st,56,src,out);correct_counters(f);meta=f.finish()
    assert verify(src,out,set("©®¶\u030a"))==208
    fontfiles[st]=out
    cm=TTFont(out).getBestCmap();assert len(cm)==212 and 'GPOS' in TTFont(out) and 'GDEF' in TTFont(out)
    st_report={'OTF':{'file':out.name,'sha256':sha(out)},'web':{},'source_sha256':sha(src)}
    for flavor in ('woff','woff2'):
        web=out.with_suffix('.'+flavor)
        try:
            x=TTFont(out);x.flavor=flavor;x.recalcTimestamp=False;x.save(web)
            back=TTFont(web)
            assert back.getBestCmap()==cm and back['hmtx'].metrics==TTFont(out)['hmtx'].metrics
            assert len(back.getBestCmap())==212 and 'GPOS' in back and 'GDEF' in back
            st_report['web'][flavor]={'status':'PASS','file':web.name,'sha256':sha(web)}
        except Exception as e:
            if web.exists():web.unlink()
            st_report['web'][flavor]={'status':'BLOCKED','reason':str(e)[:200]}
    r[st]=st_report
assert all(r[st]['web']['woff']['status']=='PASS' for st in r)
write_json(P/'web-font-build.json',r)
webs={}
for st in r:
    best='woff2' if r[st]['web']['woff2']['status']=='PASS' else 'woff'
    webs[st]=(r[st]['web'][best]['file'],best)
sample1='Arvectum — Арвектум. Интеллект в действии.'
sample2='№ 17 / 2026: 1\u202f250\u202f000,00 ₽ • 44-ФЗ • 223-ФЗ'
sample3='info@arvectum.com | https://arvectum.com • © ® ™'
css='\n'.join("@font-face {font-family:'Arvectum"+s+"';src:url('experimental/"+webs[s][0]+"') format('"+webs[s][1]+"');font-display:block;}" for s in ('Display','Text'))
page=f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Golden Step web qualification</title>
<style>{css}
body{{margin:0;background:#fff;color:#001432;padding:32px;font-family:Arial,sans-serif}}
h1{{font-size:24px;margin:0 0 20px}}section{{width:850px;display:inline-block;vertical-align:top;margin-right:30px}}
h2{{font-size:20px}}p{{margin:22px 0}}.display{{font-family:'ArvectumDisplay'}}.text{{font-family:'ArvectumText'}}
small{{color:#475569}}#qa{{margin-top:14px}}</style></head><body>
<h1>Arvectum Golden Step — v0.56 / browser proof (draft)</h1>
<section class="display"><h2>Display Medium</h2><p style="font-size:42px">{html.escape(sample1)}</p><p style="font-size:26px">{html.escape(sample2)}</p><p style="font-size:23px">{html.escape(sample3)}</p><p style="font-size:13px">{html.escape(sample1)}</p></section>
<section class="text"><h2>Text Regular</h2><p style="font-size:42px">{html.escape(sample1)}</p><p style="font-size:26px">{html.escape(sample2)}</p><p style="font-size:23px">{html.escape(sample3)}</p><p style="font-size:13px">{html.escape(sample1)}</p></section>
<div id="qa">Checking fonts...</div><script>
document.fonts.ready.then(()=>{{
  const d=document.fonts.check("20px ArvectumDisplay"),t=document.fonts.check("20px ArvectumText");
  const c=document.createElement('canvas').getContext('2d');c.font='32px ArvectumDisplay';const a=c.measureText('Arvectum 0123456789').width;
  c.font='32px Arial';const b=c.measureText('Arvectum 0123456789').width;
  document.getElementById('qa').textContent='FONT_QA display='+d+' text='+t+' widths='+a.toFixed(1)+','+b.toFixed(1)+' result='+(d&&t&&Math.abs(a-b)>1?'PASS':'FAIL');
}});
</script></body></html>'''
(P/'web-proof.html').write_text(page)
print('PASS OTF and WOFF:',json.dumps({s:r[s]['web'] for s in r},indent=1),'count',digest_tree(P))
