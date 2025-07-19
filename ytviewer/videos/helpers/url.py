from urllib.parse import urlparse, parse_qs


def is_url(string:str) -> bool:
    try:
        result = urlparse(string)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except ValueError:
        return False


def get_video_id(url:str) -> str:
    parsed_url = urlparse(url)
    
    params = parse_qs(parsed_url.query)
    
    video_id = params.get('v')
    
    if video_id:
        return video_id[0]
    else:
        raise ValueError('''The given URL doesn't contain the video ID.''')