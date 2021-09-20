from django.db.models.base import Model
from interviewsquestions.utilities.datetime import timeDaltaToInt
from django.db import models
from django.db.models.deletion import CASCADE
from interviewsquestions.utilities.database import languageField
from django.contrib.auth.models import User
import datetime
import json
class Category(models.Model):
    name =models.CharField(max_length=60)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    language=languageField

    
    def toArray(self):
        subCategories=Category.objects.filter(parent=self)
        data=[]
        for sub in subCategories:
            data.append({
                'name':sub.name,
                'id':sub.id,
                'toArray':sub.toArray(),
                'sub':sub.toArray(),
            }
        )
        return data

    
    def subs(self):
        return json.dumps(self.toArray())
    def subCategoies(self):
         return list(Category.objects.filter(parent=self))
    def getLvl(self):
        target=self
        lvl=1
        while True:
            if target.parent:
                lvl+=1
                target=target.parent
            else:
                return lvl
    def getFirstParent(self):
        lvl =self.getLvl()
        if lvl>1:
            if lvl==2:
                return self.parent
            if lvl==3:
                return self.parent.parent
            if lvl==4:
                return self.parent.parent.parent
        else:
            return None
    def getSecondParent(self):
        lvl =self.getLvl()
        if lvl>2:
            if lvl==3:
                return self.parent
            if lvl==4:
                return self.parent.parent
        else:
            return None
    def getThirdParent(self):
        lvl =self.getLvl()
        if lvl>3:
            return self.parent
        else:
            return None
    def getAllSubCategories(self):
        categories=[]
        for cate in self.subCategoies():
            categories.append(cate)
            categories+=cate.getAllSubCategories()
        return categories

class Tag(models.Model):
    name=models.CharField(max_length=60)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='tags')
    description=models.TextField()



class Post(models.Model):
    typeChoices=[
        ('Q','Question'),
        ('A','Answer'),
    ]
    text=models.TextField()
    author=models.ForeignKey(User,on_delete=CASCADE,related_name='posts')
    votes=models.IntegerField(default=0)
    type=models.CharField(max_length=1,choices=typeChoices)
    isPublished=models.BooleanField(default=False)
    ActiveDate=models.DateField(auto_now=True)
    voters=models.ManyToManyField(User,through='Voter',)
    class Meta:
        indexes=[
            models.Index(fields=['author'])
        ]
    class types:
        Question='Q'
        Answer='A'
    def isQuestion(self):
        return self.type==Post.types.Question
    def isAnswer(self):
        return self.type==Post.types.Answer
    def getVotes(self):
        if self.votes < 1000:
            return self.votes
        elif self.votes < 1000000:
            return int(self.votes/1000)+'K'
        else:
            return int(self.votes/1000000)+'M'
    def getQuestion(self):
        if self.type==Post.types.Question:
            return self.question
        else:
            return self.answer.question
    def isEdited(self):
        return self.logs.filter(type=PostLog.types.AcceptEdit).exists()
    def getLastEditAuthor(self):
        return self.logs.filter(type=PostLog.types.AcceptEdit).order_by('time').last().author
class Question(models.Model):
    post=models.OneToOneField(Post,on_delete=models.CASCADE,related_name='question')
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='questions')
    tags=models.ManyToManyField(Tag,related_name='questions')
    views=models.PositiveBigIntegerField(default=0)
    class Meta:
        indexes=[
            models.Index(fields=['category']),
        ]
    def getDuration(self):
        now=datetime.datetime.now().date()
        days =(now - self.post.logs.get(type=PostLog.types.Suggest).time.date()).days
        if days ==0:
            return 'today'
        elif days == 1:
            return 'yesterday'
        elif days<30:
            return str(days) +' days'
        elif days >= 30 and days<356:
            return str(int(days/30))+' months'
        elif days >= 365:
            if days % 365 < 30:
                return str(int(days/365))+' years'
            elif days % 365 >=30 :
                return str(int(days/365))+' years '+ str(int(days%365/30)) + ' months'
    def getLastActDuration(self):
        now=datetime.datetime.now().date()
        days =(now - self.post.ActiveDate).days
        if days ==0:
            return 'today'
        elif days == 1:
            return 'yesterday'
        elif days<30:
            return str(days) +' days'
        elif days >= 30 and days<356:
            return str(int(days/30))+' months'
        elif days >= 365:
            if days % 365 < 30:
                return str(int(days/365))+' years'
            elif days % 365 >=30 :
                return str(int(days/365))+' years '+ str(int(days%365/30)) + ' months'
    def formatedDate(self):
        return self.post.logs.get(type=PostLog.types.Suggest).time.date().strftime('%Y/%m/%d')

    def getSuggestedAnswers(self):
        return self.answers.filter(post__logs__type=PostLog.types.Suggest).exclude(
            post__logs__type=PostLog.types.Accept
        ).exclude(
            post__logs__type=PostLog.types.Reject

        )
    def getAcceptedAnswers(self):
        return self.answers.filter(post__logs__type=PostLog.types.Accept)
        
    def getRejectedAnswers(self):
        return self.answers.filter(
            post__logs__type=PostLog.types.Reject
        ).exclude(
            post__logs__type=PostLog.types.Accept

        )
    @staticmethod
    def orderByLastSuggesAnstDate(questions,asc=True):
        questions=list(questions)
        orderd=[]
        for i in range(len(questions)):
            currentItem=questions[0] if questions else None
            for que in questions:
                date=que.getSuggestedAnswers().last().post.logs.get(type=PostLog.types.Suggest).time
                if asc:
                    if timeDaltaToInt(date -currentItem.getSuggestedAnswers().last().post.logs.get(type=PostLog.types.Suggest).time)<0:
                        currentItem=que
                else:
                    if timeDaltaToInt(date -currentItem.getSuggestedAnswers().last().post.logs.get(type=PostLog.types.Suggest).time)>0:
                        currentItem=que
            questions.remove(currentItem)
            orderd.append(currentItem)
        return orderd
    def orderByLastAccepAnstDate(questions,asc=True):
        questions=list(questions)
        orderd=[]
        for i in range(len(questions)):
            currentItem=questions[0] if questions else None
            for que in questions:
                date=que.getAcceptedAnswers().last().post.logs.get(type=PostLog.types.Accept).time
                if asc:
                    if timeDaltaToInt(date -currentItem.getAcceptedAnswers().last().post.logs.get(type=PostLog.types.Accept).time)<0:
                        currentItem=que
                else:
                    if timeDaltaToInt(date -currentItem.getAcceptedAnswers().last().post.logs.get(type=PostLog.types.Accept).time)>0:
                        currentItem=que
            questions.remove(currentItem)
            orderd.append(currentItem)
        return orderd
    def orderByAcceptDate(questions,asc=True):
        questions=list(questions)
        orderd=[]
        for i in range(len(questions)):
            currentItem=questions[0] if questions else None
            for que in questions:
                date=que.post.logs.get(type=PostLog.types.Accept).time
                if asc:
                    if timeDaltaToInt(date -currentItem.post.logs.get(type=PostLog.types.Accept).time)<0:
                        currentItem=que
                else:
                    if timeDaltaToInt(date -currentItem.post.logs.get(type=PostLog.types.Accept).time)>0:
                        currentItem=que
            questions.remove(currentItem)
            orderd.append(currentItem)
        return orderd

    def getLastAnswerDate(self):
        acceptedAnswers=self.getAcceptedAnswers()
        if acceptedAnswers:
            return acceptedAnswers.last().post.logs.get(type=PostLog.types.Suggest).time.date().strftime('%Y/%m/%d')
    def allLogs(self):
        allLogs=[]
        allLogs+=list(self.post.logs.all())
        for ans in self.answers.all():
            allLogs+=list(ans.post.logs.all())
        return allLogs
class SuggestedQuestion(models.Model):
    post=models.OneToOneField(Post,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    tags=models.ManyToManyField(Tag)
    date=models.DateField(auto_now_add=True,) # TODO make custom oreder
    question=models.OneToOneField(Question,on_delete=models.CASCADE,null=True)

    class Meta:
        ordering=['date']
        indexes=[
                models.Index(fields=['category']),
            ]
    def getDuration(self):
        now=datetime.datetime.now().date()
        days =(now - self.post.logs.get(type=PostLog.types.Suggest).time.date()).days
        if days ==0:
            return 'today'
        elif days == 1:
            return 'yesterday'
        elif days<30:
            return str(days) +' days'
        elif days >= 30 and days<356:
            return str(int(days/30))+' months'
        elif days >= 365:
            if days % 365 < 30:
                return str(int(days/365))+' years'
            elif days % 365 >=30 :
                return str(int(days/365))+' years '+ str(int(days%365/30)) + ' months'
    def formatedDate(self):
        return self.post.logs.get(type=PostLog.types.Suggest).time.date().strftime('%Y/%m/%d')

    def modeWhoAccept(self):
        return self.post.logs.filter(type=PostLog.types.Accept).first().moderator
    def modeWhoReject(self):
        return self.post.logs.filter(type=PostLog.types.Reject).first().moderator

    def isAccepted(self):
        return self.post.logs.filter(type=PostLog.types.Accept).exists()

    def isRejected(self):
        return self.post.logs.filter(type=PostLog.types.Reject).exists()
    @staticmethod
    def orderBySuggestDate(questions,asc=True):
        questions=list(questions)
        orderd=[]
        for i in range(len(questions)):
            currentItem=questions[0] if questions else None
            for que in questions:
                date=que.post.logs.get(type=PostLog.types.Suggest).time
                if asc:
                    if timeDaltaToInt(date -currentItem.post.logs.get(type=PostLog.types.Suggest).time)<0:
                        currentItem=que
                else:
                    if timeDaltaToInt(date -currentItem.post.logs.get(type=PostLog.types.Suggest).time)>0:
                        currentItem=que
            questions.remove(currentItem)
            orderd.append(currentItem)
        return orderd
    def orderByAcceptDate(questions,asc=True):
        questions=list(questions)
        orderd=[]
        for i in range(len(questions)):
            currentItem=questions[0] if questions else None
            for que in questions:
                date=que.post.logs.get(type=PostLog.types.Accept).time
                if asc:
                    if timeDaltaToInt(date -currentItem.post.logs.get(type=PostLog.types.Accept).time)<0:
                        currentItem=que
                else:
                    if timeDaltaToInt(date -currentItem.post.logs.get(type=PostLog.types.Accept).time)>0:
                        currentItem=que
            questions.remove(currentItem)
            orderd.append(currentItem)
        return orderd
    def orderByRejectDate(questions,asc=True):
        questions=list(questions)
        orderd=[]
        for i in range(len(questions)):
            currentItem=questions[0] if questions else None
            for que in questions:
                date=que.post.logs.get(type=PostLog.types.Reject).time
                if asc:
                    if timeDaltaToInt(date -currentItem.post.logs.get(type=PostLog.types.Reject).time)<0:
                        currentItem=que
                else:
                    if timeDaltaToInt(date -currentItem.post.logs.get(type=PostLog.types.Reject).time)>0:
                        currentItem=que
            questions.remove(currentItem)
            orderd.append(currentItem)
        return orderd

class SuggestedEdit(models.Model):
    statusChoisies=[
        ('S','Suggested'),
        ('A','Rejected'),
        ('R','Acceptd'),
    ]
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    status=models.CharField(max_length=1,choices=statusChoisies)
    class staties:
        Suggest='S'
        Accept='A'
        Reject='R'
    def getSuggestedDate(self):
        return self.logs.get(type=PostLog.types.SuggestEdit).time.date().strftime('%Y/%m/%d')
    def userWhoSugget(self):
        return self.logs.get(type=PostLog.types.SuggestEdit).author
    def text(self):
        return self.logs.get(type=PostLog.types.SuggestEdit).text
    @staticmethod
    def orderBySuggestDate(edits,asc=True):
        edits=list(edits)
        orderd=[]
        for i in range(len(edits)):
            currentItem=edits[0] if edits else None
            for edit in edits:
                date=edit.logs.get(type=PostLog.types.SuggestEdit).time
                if asc:
                    if timeDaltaToInt(date -currentItem.logs.get(type=PostLog.types.SuggestEdit).time)<0:
                        currentItem=edit
                else:
                    if timeDaltaToInt(date -currentItem.logs.get(type=PostLog.types.SuggestEdit).time)>0:
                        currentItem=edit
            edits.remove(currentItem)
            orderd.append(currentItem)
        return orderd
    def orderByAcceptDate(edits,asc=True):
        edits=list(edits)
        orderd=[]
        for i in range(len(edits)):
            currentItem=edits[0] if edits else None
            for edit in edits:
                date=edit.logs.get(type=PostLog.types.AcceptEdit).time
                if asc:
                    if timeDaltaToInt(date -currentItem.logs.get(type=PostLog.types.AcceptEdit).time)<0:
                        currentItem=edit
                else:
                    if timeDaltaToInt(date -currentItem.logs.get(type=PostLog.types.AcceptEdit).time)>0:
                        currentItem=edit
            edits.remove(currentItem)
            orderd.append(currentItem)
        return orderd
    def orderByRejectDate(edits,asc=True):
        edits=list(edits)
        orderd=[]
        for i in range(len(edits)):
            currentItem=edits[0] if edits else None
            for edit in edits:
                date=edit.logs.get(type=PostLog.types.RejectEdit).time
                if asc:
                    if timeDaltaToInt(date -currentItem.logs.get(type=PostLog.types.RejectEdit).time)<0:
                        currentItem=edit
                else:
                    if timeDaltaToInt(date -currentItem.logs.get(type=PostLog.types.RejectEdit).time)>0:
                        currentItem=edit
            edits.remove(currentItem)
            orderd.append(currentItem)
        return orderd

class PostLog(models.Model):
    typeChoices=[
        ('S','Suggest'),
        ('A','Accept'),
        ('R','Reject'),
        ('SE','Suggest Edit'),
        ('AE','Accept Edit'),
        ('RE','Reject Edit'),
        ('P','Publish'),
        ('UP','Unpublish'),
    ]
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='logs')
    text=models.TextField(null=True)
    moderator=models.ForeignKey(User,on_delete=CASCADE,related_name='logs', null=True)
    author=models.ForeignKey(User,on_delete=CASCADE)
    time=models.DateTimeField(auto_now_add=True)
    type=models.CharField(max_length=4,choices=typeChoices)
    edit=models.ForeignKey(SuggestedEdit,on_delete=models.CASCADE,null=True,related_name='logs')
    class Meta:
        ordering=['time']
        indexes=[
                    models.Index(fields=['type','post']),
            ]
    class types:
        Suggest='S'
        Accept='A'
        Reject='R'
        SuggestEdit='SE'
        AcceptEdit='AE'
        RejectEdit='RE'
        Publish='P'
        Unpublish='UP'
    
class Voter(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE)
    post=models.ForeignKey(Post,on_delete=CASCADE)
    type=models.BooleanField()


    class types:
        Up=True
        Down=False


class Answer(models.Model):
    post=models.OneToOneField(Post,on_delete=models.CASCADE ,related_name='answer')  
    question=models.ForeignKey(Question,on_delete=CASCADE,related_name='answers')
    def formatedDate(self):
        return self.post.logs.get(type=PostLog.types.Suggest).time.date().strftime('%Y/%m/%d')

    def isAccepted(self):
        return self.post.logs.filter(type=PostLog.types.Accept).exists()
    def isRejected(self):
        return self.post.logs.last().type==PostLog.types.Reject
    def isJustSuggested(self):
        return self.post.logs.last().type==PostLog.types.Suggest


class Comment(models.Model):
    text= models.CharField(max_length=300)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    date=models.DateField(auto_now_add=True)

    def getFormatedDate(self):
        return self.date.strftime('%Y/%m/%d')

