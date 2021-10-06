from django.shortcuts import redirect, render,get_object_or_404
from .models import Poll,PollItem, PollResault
from interviewsquestions.utilities.authDecoratros import forActiveUser
from django.contrib import messages


@forActiveUser
def poll(request,pollID):
    poll=get_object_or_404(Poll,id=pollID)
    submitable=not poll.resaults.filter(user=request.user).exists()
    if submitable or request.user.profile.isSuperAdmin:
        if request.method=='POST':
            if not submitable:
                messages.success(request,'Thank You')
                return redirect('content:index')
  
            resault={}
            for item in poll.items.all():
                options=item.getOptions()
                resaultItem=[]
                if item.type==PollItem.types.Check:
                    for option in options:
                        if f'{item.id}-{options.index(option)}' in request.POST:
                            resaultItem.append(option)
                elif item.type==PollItem.types.Radio:
                    resaultItem.append(options[int(request.POST[f'item-{item.id}'])])
                resault[str(item.id)]=resaultItem
            PollResault.objects.create(
                poll=poll,
                user=request.user,
                resault=resault
            )
            messages.success(request,'Thank You')
            return redirect('content:index')
        contxt={
            'poll':poll,
            'submitable':submitable
        }
        return render(request,'polls/poll.html',contxt)

    else:
        messages.success(request,'Thank You')
        return redirect('content:index')
