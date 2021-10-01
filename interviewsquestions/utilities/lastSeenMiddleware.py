

class lastSeenMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response



    def __call__(self,request):
        response=self.get_response(request)
        if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_active and hasattr(request.user,'profile'):
        
            request.user.profile.updateLastSeen()
        return response
        