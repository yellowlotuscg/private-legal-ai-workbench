from dataclasses import dataclass
import re
@dataclass(frozen=True)
class Passage:
 matter: str
 source: str
 text: str
def retrieve(query, passages, matter, limit=3):
 terms=set(re.findall(r"[a-z0-9]+",query.lower()))
 allowed=[p for p in passages if p.matter==matter]
 ranked=sorted(allowed,key=lambda p:len(terms & set(re.findall(r"[a-z0-9]+",p.text.lower()))),reverse=True)
 return [p for p in ranked if terms & set(re.findall(r"[a-z0-9]+",p.text.lower()))][:limit]
