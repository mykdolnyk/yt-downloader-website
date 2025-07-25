from ytviewer import settings


def github_repo(request):
    return {'github_repo_url': settings.GITHUB_REPO_URL}