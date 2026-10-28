import json, math, numpy as np, sys
from matplotlib.path import Path
W,H=1080,1440
INK,AMB='#13213A','#F2A93B'
lon0,lat0=float(sys.argv[2]) if len(sys.argv)>2 else 48, float(sys.argv[3]) if len(sys.argv)>3 else 22
R=float(sys.argv[4]) if len(sys.argv)>4 else 640
cx,cy=W/2,H*0.53
land=json.load(open('land.json'))
paths=[]
for g in land['features'] if 'features' in land else [land]:
    geom=g['geometry']; polys=geom['coordinates'] if geom['type']=='MultiPolygon' else [geom['coordinates']]
    for poly in polys:
        paths.append(Path(np.array(poly[0])))
def proj(lon,lat):
    l,p=math.radians(lon-lon0),math.radians(lat); p0=math.radians(lat0)
    x=math.cos(p)*math.sin(l); y=math.cos(p0)*math.sin(p)-math.sin(p0)*math.cos(p)*math.cos(l)
    z=math.sin(p0)*math.sin(p)+math.cos(p0)*math.cos(p)*math.cos(l)
    return cx+R*x, cy-R*y, z
# dot grid
step=1.0; pts=[]
lats=np.arange(-80,84,step)
for la in lats:
    n=max(1,int(round(360*math.cos(math.radians(la))/step)))
    for k in range(n):
        lo=-180+k*360/n; pts.append((lo,la))
pts=np.array(pts); inland=np.zeros(len(pts),bool)
for p in paths:
    bb=p.get_extents(); m=(pts[:,0]>=bb.x0)&(pts[:,0]<=bb.x1)&(pts[:,1]>=bb.y0)&(pts[:,1]<=bb.y1)&~inland
    if m.any(): inland[np.where(m)[0][p.contains_points(pts[m])]]=True
out=[]
out.append(f'<defs><radialGradient id="g" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#FBF7F0"/><stop offset="1" stop-color="#EADFCB"/></radialGradient><radialGradient id="glow"><stop offset=".6" stop-color="{AMB}" stop-opacity=".45"/><stop offset="1" stop-color="{AMB}" stop-opacity="0"/></radialGradient></defs>')
out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#g)" stroke="{INK}" stroke-opacity=".08" stroke-width="2"/>')
for lo,la in pts[inland]:
    x,y,z=proj(lo,la)
    if z>0.02: out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.6+1.6*z:.2f}" fill="{INK}" fill-opacity="{0.18+0.5*z:.2f}"/>')
DXB=(55.36,25.25)
C=[(-0.13,51.5),(2.35,48.86),(12.5,41.9),(-9.14,38.7),(23.7,37.98),(-2.24,53.48),(-6.26,53.35),(13.4,52.52),(14.42,50.08),(28.97,41.0),(37.6,55.75),(30.5,50.45),(19.04,47.5),(26.1,44.43),(21.0,52.23),(18.07,59.33),(10.75,59.91),
   (31.24,30.04),(3.38,6.52),(36.82,-1.29),(18.42,-33.92),(28.05,-26.2),(38.75,9.03),(-7.6,33.57),(32.58,0.35),(47.5,-18.9),(-17.45,14.69),
   (72.88,19.08),(77.2,28.6),(80.27,13.08),(76.95,8.5),(67.0,24.86),(74.35,31.55),(90.4,23.8),(85.3,27.7),(79.86,6.93),(73.5,4.17),(100.5,13.75),(101.69,3.14),(103.82,1.35),(106.8,-6.2),(120.98,14.6),(114.17,22.3),(116.4,39.9),(121.47,31.23),(127.0,37.56),(139.7,35.68),(69.24,41.3),(71.43,51.13),
   (44.8,41.7),(49.87,40.4),(35.93,31.95),(35.5,33.9),(46.7,24.7),(39.2,21.5),(47.98,29.37),(58.4,23.6),(50.58,26.22),(51.53,25.29),(44.4,33.3),(51.4,35.7),
   (-73.9,40.7),(-79.4,43.7),(-46.6,-23.5),(151.2,-33.87),(144.96,-37.8),(174.76,-36.85),(115.86,-31.95)]
def gc(a,b,n=140):
    la1,lo1,la2,lo2=map(math.radians,(a[1],a[0],b[1],b[0]))
    v1=np.array([math.cos(la1)*math.cos(lo1),math.cos(la1)*math.sin(lo1),math.sin(la1)])
    v2=np.array([math.cos(la2)*math.cos(lo2),math.cos(la2)*math.sin(lo2),math.sin(la2)])
    om=math.acos(max(-1,min(1,v1@v2)));res=[]
    for t in np.linspace(0,1,n):
        v=(math.sin((1-t)*om)*v1+math.sin(t*om)*v2)/math.sin(om)
        lift=1+0.16*om*math.sin(math.pi*t)   # arcs rise off the surface like flight tracks
        lo,la=math.degrees(math.atan2(v[1],v[0])),math.degrees(math.asin(v[2]))
        x,y,z=proj(lo,la); res.append((cx+(x-cx)*lift,cy+(y-cy)*lift,z,lift))
    return res
dx,dy,_=proj(*DXB)
for c in C:
    x,y,z=proj(*c)
    if z<0.08: continue
    L=math.hypot(dx-x,dy-y); mx,my=(x+dx)/2,(y+dy)/2
    nx,ny=-(dy-y)/L,(dx-x)/L
    if ny>0: nx,ny=-nx,-ny          # bow every arc upwards, like tracks on a flight map
    k=0.22*L
    out.append(f'<path d="M{x:.1f} {y:.1f} Q{mx+nx*k:.1f} {my+ny*k:.1f} {dx:.1f} {dy:.1f}" fill="none" stroke="{AMB}" stroke-width="2.6" stroke-opacity=".9" stroke-linecap="round"/>')
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{INK}"/>')
x,y,z=proj(*DXB)
out.append(f'<circle cx="{x}" cy="{y}" r="70" fill="url(#glow)"/>')
out.append(f'<circle cx="{x}" cy="{y}" r="12" fill="{AMB}" stroke="#FBF7F0" stroke-width="4"/>')
s=84/92.1
out.append(f'<g transform="translate({x:.1f} {y-4:.1f}) scale({s:.3f})"><path d="M-33.25 -68.40 L-38.11 -65.81 L0 0Z" fill="{INK}"/><circle cx="-35.68" cy="-67.1" r="24" fill="{AMB}"/></g>')
bg='background:radial-gradient(60% 50% at 85% 10%,rgba(242,169,59,.34),transparent 70%),radial-gradient(80% 60% at 10% 110%,rgba(214,203,184,.5),transparent 70%),linear-gradient(180deg,#FBF7F0,#F4EFE6)'
open('globe.html','w').write(f'<!doctype html><html><body style="margin:0;width:{W}px;height:{H}px;overflow:hidden;{bg}"><svg width="{W}" height="{H}">{"".join(out)}</svg></body></html>')
