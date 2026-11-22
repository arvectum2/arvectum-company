"""Golden Step v0.87: one phi-guided Inter-derived Cyrillic З/з trial.

v0.86 is the exact font/table baseline. The outline topology of original
Inter (vendored via v0.85) is kept; the two extrema acquire unequal
phi-related tangent flats and the middle bridge gets a tiny local inset.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import hashlib,json,math

P=Path(__file__).resolve().parent
V85=P.parent/'Arvectum-Typeface-v0.85'
V86=P.parent/'Arvectum-Typeface-v0.86'
PHI=(1+math.sqrt(5))/2
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
assert (V85/'OFL-LICENSE.txt').read_bytes()==(V86/'OFL-LICENSE.txt').read_bytes()
(P/'OFL-LICENSE.txt').write_bytes((V86/'OFL-LICENSE.txt').read_bytes())

STYLES={
 'Display':('Medium','ArvectumGoldenStepDisplayBaseDraft085-Medium.otf',
            'ArvectumGoldenStepDisplayArchFlatsDraft086-Medium.otf'),
 'Text':('Regular','ArvectumGoldenStepTextBaseDraft085-Regular.otf',
         'ArvectumGoldenStepTextArchFlatsDraft086-Regular.otf')
}

def fit_from_inter(original_pen,advance,char):
    ops=list(original_pen.value)
    assert len(ops)==20 and ops[0][0]=='moveTo' and ops[19][0]=='closePath'
    topx,topy=ops[5][1][-1]
    bottomx,bottomy=ops[0][1][0]
    assert (bottomx,bottomy)==ops[18][1][-1]
    up=round(advance*(.055 if char=='З' else .050))
    down=round(up*PHI)
    inset=round(advance/(PHI**9))
    uL,uR=up//2,up-up//2
    dL,dR=down//2,down-down//2
    assert ops[5][1][-2][0]>topx+uR
    assert ops[6][1][0][0]<topx-uL
    assert ops[1][1][0][0]>bottomx+dR
    assert ops[18][1][-2][0]<bottomx-dL
    assert ops[11][0]=='lineTo' and ops[12][0]=='lineTo'
    # The two left bridge points move inward; vertical thickness is unchanged.
    def shift_bridge(op):return ('lineTo',((op[1][0][0]+inset,op[1][0][1]),))
    new=[('moveTo',((bottomx+dR,bottomy),))]
    new.extend(ops[1:5])
    u=list(ops[5][1]);u[-1]=(topx+uR,topy)
    new.append(('curveTo',tuple(u)))
    new.append(('lineTo',((topx-uL,topy),)))
    new.extend(ops[6:11])
    new.append(shift_bridge(ops[11]))
    new.append(shift_bridge(ops[12]))
    new.extend(ops[13:18])
    b=list(ops[18][1]);b[-1]=(bottomx-dL,bottomy)
    new.append(('curveTo',tuple(b)))
    new.append(('lineTo',((bottomx+dR,bottomy),)))
    new.append(ops[19])
    assert len(new)==22
    rec=RecordingPen();rec.value=new
    return rec,{'top_flat':up,'bottom_flat':down,'bottom_top_ratio':down/up,
                'phi_error':abs(down/up-PHI),'middle_inset':inset,
                'top_origin':[topx,topy],'bottom_origin':[bottomx,bottomy],
                'join_type':'tangent G1','source_outline':'Inter 4.1 exact'}

def svg(font,char,target):
    cm=font.getBestCmap();gs=font.getGlyphSet();g=gs[cm[ord(char)]]
    s=SVGPathPen(gs);g.draw(s);b=BoundsPen(gs);g.draw(b)
    x0,y0,x1,y1=b.bounds
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{s.getCommands()}"/></svg>\n')

manifest={'version':'0.87','lifecycle':'experiment / owner optical acceptance OPEN',
  'design':'two top/bottom flats with phi length ratio; one phi^-9 horizontal waist inset',
  'source':'Inter v4.1 via v0.85; v0.86 table/outline baseline',
  'phi':PHI,'changed_glyphs':['U+0417','U+0437'],'styles':{}}
for sty,(weight,f85,f86) in STYLES.items():
    source=V85/'experimental'/f85
    prior=V86/'experimental'/f86
    inter=TTFont(source);old=TTFont(prior)
    f=TTFont(prior,recalcTimestamp=False)
    cm=f.getBestCmap()
    top=f['CFF '].cff.topDictIndex[0]
    data={}
    for ch in 'Зз':
        name=cm[ord(ch)]
        rec=RecordingPen();inter.getGlyphSet()[name].draw(rec)
        width,lsb=f['hmtx'][name]
        shaped,params=fit_from_inter(rec,width,ch)
        t=T2CharStringPen(width,None);shaped.replay(t)
        top.CharStrings[name]=t.getCharString(private=top.Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
        data[ch]={'glyph_name':name,'advance':width,'lsb':lsb,**params}
    family=f'Arvectum Golden Step {sty} Phi Draft 087'
    ps=f'ArvectumGoldenStep{sty}PhiDraft087-{weight}'
    for plat,enc,lang in ((3,1,1033),(1,0,0)):
        for nid,value in ((1,family),(2,weight),(3,ps+';0.87;Inter-4.1-source'),
                          (4,family+' '+weight),(5,'Version 0.087; experimental'),
                          (6,ps),(16,family),(17,weight)):
            f['name'].setName(value,nid,plat,enc,lang)
    top.FamilyName=family;top.FullName=family+' '+weight
    f['CFF '].cff.fontNames=[ps]
    f['head'].fontRevision=.087;f.recalcTimestamp=False
    dest=P/'experimental'/f'{ps}.otf';dest.parent.mkdir(parents=True,exist_ok=True);f.save(dest)
    variant=TTFont(dest)
    for source_name,font in (('Inter',inter),('v086',old),('v087',variant)):
        for ch in 'Зз3':
            svg(font,ch,P/'glyphs'/source_name/sty/f'U+{ord(ch):04X}.svg')
    manifest['styles'][sty]={'weight':weight,'prior_otf':f86,'original_otf':f85,
      'source_sha256':sha(source),'prior_sha256':sha(prior),
      'output':str(dest.relative_to(P)),'output_sha256':sha(dest),'parameters':data}
    print(sty,{k:{f:d[f] for f in ('advance','top_flat','bottom_flat','middle_inset','phi_error')} for k,d in data.items()})
(P/'evidence').mkdir(parents=True,exist_ok=True)
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('BUILT',P)
