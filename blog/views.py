from django.shortcuts import render


def post_list(request):
    example_lips = []

    return render(request,
                  'blog/post_list.html',
                  {'example_lips': example_lips})
