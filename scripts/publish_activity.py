"""Publish a strict allowlist of generated assets in one fast-forward commit."""
from pathlib import Path
import base64,json,os,urllib.request,xml.etree.ElementTree as ET
ROOT='/repos/Ap-95671/Ap-95671'
FILES=['assets/activity/calendar-static.svg','assets/activity/snapshot.json','assets/activity/contribution-snake-light.svg','assets/activity/contribution-snake-dark.svg']
def main():
    token=os.environ['GH_TOKEN']
    def api(method,path,data=None):
        assert path.startswith(ROOT+'/')
        req=urllib.request.Request('https://api.github.com'+path,method=method,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','User-Agent':'Ap-95671-activity-assets'},data=json.dumps(data).encode() if data is not None else None)
        with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
    head=api('GET',ROOT+'/git/ref/heads/main')['object']['sha'];base=api('GET',ROOT+'/git/commits/'+head)['tree']['sha']
    tree=[]
    for name in FILES:
        p=Path(name);assert p.is_file() and not p.is_symlink() and p.stat().st_size<500000
        data=p.read_bytes()
        if p.suffix=='.svg':
            root=ET.fromstring(data)
            assert root.tag.endswith('svg')
            for e in root.iter():
                assert e.tag.split('}')[-1] not in ['script','foreignObject','image','iframe']
                assert not any(k.lower().startswith('on') for k in e.attrib)
        else:json.loads(data)
        blob=api('POST',ROOT+'/git/blobs',{'content':base64.b64encode(data).decode(),'encoding':'base64'})['sha']
        tree.append({'path':name,'mode':'100644','type':'blob','sha':blob})
    newtree=api('POST',ROOT+'/git/trees',{'base_tree':base,'tree':tree})['sha']
    if newtree==base:print('Calendar assets unchanged.');return
    identity={'name':'github-actions[bot]','email':'41898282+github-actions[bot]@users.noreply.github.com'}
    commit=api('POST',ROOT+'/git/commits',{'message':'Refresh verified contribution visuals [skip ci]','tree':newtree,'parents':[head],'author':identity,'committer':identity})['sha']
    api('PATCH',ROOT+'/git/refs/heads/main',{'sha':commit,'force':False})
    print('Allowlisted assets published with a fast-forward commit.')
if __name__=='__main__':main()
