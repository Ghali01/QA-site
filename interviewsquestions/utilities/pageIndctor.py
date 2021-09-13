from math import ceil
from django.shortcuts import redirect

def pageGenerat(set,page,redirectTarget):

    page=1 if page==0 else page
    count=set.count()+0
    toN=page*25
    fromN=toN-25
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(set): return redirect(redirectTarget)
    set=list(set)[fromN:toN]
    pages=range(indcStart,indcStart+7 if remPages>=3 else page+remPages )
    return set,pages