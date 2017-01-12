from django.http import HttpResponse


def ping(request):
    return HttpResponse(status=200)
    
def parse_user(request):
	users = json.loads(request.body)
	return HttpResponse(status=200)