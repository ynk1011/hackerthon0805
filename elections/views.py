# from django.shortcuts import get_object_or_404, render, redirect
# from django.http import HttpResponse

# from .models import Candidate, Poll, Choice
# import datetime     

# from django.http import HttpResponseRedirect
# from django.db.models import Sum 

# from .forms import ElectionForm, PollForm, ChoiceForm

# def electionhome(request):
#     form = ElectionForm()
#     return render(request, 'test.html', {'form': form})

# def newelection(request):
#     form = ElectionForm(request.POST, request.FILES)
#     if form.is_valid():
#         new_election = form.save(commit=False)
#         new_election.save()
#     #return render(request, 'test2.html')
#     return redirect('electionhome2')

# def electionhome2(request):
#     form = ElectionForm()
#     return render(request, 'test2.html', {'form': form})

# def newelection2(request):
#     form = ElectionForm(request.POST, request.FILES)
#     if form.is_valid():
#         new_election = form.save(commit=False)
#         new_election.save()
#     #return render(request, 'test3.html')
#     return redirect('pollhome')

# #########################################


# def pollhome(request):
#     form = PollForm()
#     return render(request, 'test3.html', {'form': form})

# def newpoll(request):
#     form = PollForm(request.POST, request.FILES)
#     if form.is_valid():
#         new_poll = form.save(commit=False)
#         new_poll.save()
#     return redirect('choicehome')


# ######################################


# def choicehome(request):
#     form = ChoiceForm()
#     return render(request, 'test4.html', {'form': form})

# def newchoice(request):
#     form = ChoiceForm(request.POST, request.FILES)
#     if form.is_valid():
#         new_choice = form.save(commit=False)
#         new_choice.save()
#     return redirect('choicehome2')


# def choicehome2(request):
#     form = ChoiceForm()
#     return render(request, 'test5.html', {'form': form})

# def newchoice2(request):
#     form = ChoiceForm(request.POST, request.FILES)
#     if form.is_valid():
#         new_choice = form.save(commit=False)
#         new_choice.save()
#     return redirect('home')


# ######################################

# def index(request, area):
#     #candidates = get_object_or_404(Candidate, area=area)
#     candidates = Candidate.objects.get(area=area)
#     context = {'candidates' : candidates} #context??? ?????? ????????? ?????? ????????? ??????
#     return render(request, 'elections/index.html', context)

    
# def areas(request, area):
#     today = datetime.datetime.now()
#     try :
#          #poll = Poll.objects.get(area = area, start_date__lte = today, end_date__gte=today) # get??? ????????? ????????? ??????????????????. 
#          #poll = Poll.objects.get(area = area, start_date__lte =  datetime.date(2021, 7, 1), end_date__gte= datetime.date(2021, 7, 1)) 
#         poll = Poll.objects.get(area=area) #Poll?????? area?????? ??????. 
    
#         candidates = Candidate.objects.filter(area = area) # Candidate??? area??? ???????????? area??? ?????? ????????? ????????????
#     except:
#         poll = None
#         candidates = None
#     context = {'candidates': candidates, 'area' : area, 'poll' : poll }

#     return render(request, 'elections/area.html', context)



# def polls(request, poll_id):
#     poll = Poll.objects.get(pk = poll_id)
#     selection = request.POST['choice']

#     try: 
#         choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
#         choice.votes += 1
#         choice.save()
#     except:
#         #????????? ???????????? ??????, DB??? ????????? Choice????????? ?????? ????????? Choice??? ?????? ???????????????
#         choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
#         choice.save()

#     return HttpResponseRedirect("/areas/{}/results".format(poll.area))


# #?????? ?????? 
# def results(request, area):
#     candidates = Candidate.objects.filter(area = area)
#     polls = Poll.objects.filter(area = area)
#     poll_results = []
#     for poll in polls:
#         result = {}
#         result['start_date'] = datetime.date(2021, 7, 1)
#         result['end_date'] = datetime.date(2021, 7, 1)

#         # poll.id??? ???????????? ?????? ?????????
#         total_votes = Choice.objects.filter(poll_id = poll.id).aggregate(Sum('votes')) 
#         result['total_votes'] = total_votes['votes__sum']

#         rates = [] #?????????
#         for candidate in candidates:
#             # choice??? ????????? ?????? ?????? - ??????????????? 0??? append
#             try:
#                 choice = Choice.objects.get(poll = poll, candidate = candidate)
#                 rates.append(
#                     round(choice.votes * 100 / result['total_votes'], 1)
#                     )
#             except :
#                 rates.append(0)
#         result['rates'] = rates
#         poll_results.append(result)

#     context = {'candidates':candidates, 'area':area,
#     'poll_results' : poll_results}
#     return render(request, 'elections/result.html', context)

# def jump(request):
#     candidates = Candidate.objects.filter(area = "??????")
#     polls = Poll.objects.filter(area = "??????")
#     poll_results = []
#     for poll in polls:
#         result = {}
#         result['start_date'] = datetime.date(2021, 7, 1)
#         result['end_date'] = datetime.date(2021, 7, 1)

#         # poll.id??? ???????????? ?????? ?????????
#         total_votes = Choice.objects.filter(poll_id = poll.id).aggregate(Sum('votes')) 
#         result['total_votes'] = total_votes['votes__sum']

#         rates = [] #?????????
#         for candidate in candidates:
#             # choice??? ????????? ?????? ?????? - ??????????????? 0??? append
#             try:
#                 choice = Choice.objects.get(poll = poll, candidate = candidate)
#                 rates.append(
#                     round(choice.votes * 100 / result['total_votes'], 1)
#                     )
#             except :
#                 rates.append(0)
#         result['rates'] = rates
#         poll_results.append(result)

#     context = {'candidates':candidates,   'poll_results' : poll_results}
#     return render(request, 'elections/result.html', context)
