"""Render only the public contribution calendar; never print or persist credentials."""
from pathlib import Path
import datetime as dt, json, os, urllib.request

def main():
    token=os.environ['GH_TOKEN']
    query='query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{contributionCount contributionLevel weekday date}}}}}}'
    req=urllib.request.Request('https://api.github.com/graphql',method='POST',headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','User-Agent':'Ap-95671-public-calendar'},data=json.dumps({'query':query,'variables':{'login':'Ap-95671'}}).encode())
    with urllib.request.urlopen(req,timeout=30) as r:d=json.load(r)
    if d.get('errors'):raise RuntimeError('GitHub calendar request failed; existing assets preserved')
    weeks=d['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    assert 1<=len(weeks)<=54
    levels={'NONE':0,'FIRST_QUARTILE':1,'SECOND_QUARTILE':2,'THIRD_QUARTILE':3,'FOURTH_QUARTILE':4}
    palette=['#e7ebef','#bcc8d3','#7f98ad','#45677f','#c58550']
    cells=[];total=0;dates=[]
    for x,week in enumerate(weeks):
        for day in week['contributionDays']:
            level=levels[day['contributionLevel']];y=int(day['weekday']);count=int(day['contributionCount']);assert 0<=y<=6 and count>=0
            dates.append(day['date']);total+=count
            cells.append(f'<rect x="{35+x*16}" y="{63+y*15}" width="12" height="12" rx="3" fill="{palette[level]}"><title>{day["date"]}: {count} contributions</title></rect>')
    today=dt.datetime.now(dt.timezone.utc).date().isoformat()
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="960" height="212" viewBox="0 0 960 212" role="img"><title>GitHub contribution calendar for Ap-95671</title><desc>Actual GitHub calendar snapshot, not a proficiency or productivity score.</desc><rect x="1" y="1" width="958" height="210" rx="16" fill="#f8f9fb" stroke="#d7dee6"/><g font-family="Arial,Helvetica,sans-serif"><text x="35" y="33" font-size="13" letter-spacing="1.5" fill="#263a4e">GITHUB CONTRIBUTION CALENDAR</text><text x="924" y="33" text-anchor="end" font-size="12" fill="#516476">'+today+'</text>'+''.join(cells)+'<text x="35" y="191" font-size="12" fill="#516476">'+min(dates)+' — '+max(dates)+' · '+str(total)+' contributions reported by GitHub</text><text x="924" y="191" text-anchor="end" font-size="12" fill="#516476">Snapshot, not a score</text></g></svg>'
    out=Path('assets/activity');out.mkdir(parents=True,exist_ok=True)
    (out/'calendar-static.svg').write_text(svg)
    (out/'snapshot.json').write_text(json.dumps({'username':'Ap-95671','source':'GitHub contributionCalendar','generatedAt':today,'firstDate':min(dates),'lastDate':max(dates),'reportedContributions':total,'scope':'Calendar GitHub exposes to this repository-scoped token; no private repository names or contents requested.'},indent=2)+'\n')
    print('Public calendar snapshot generated; credentials not persisted.')
if __name__=='__main__':main()
