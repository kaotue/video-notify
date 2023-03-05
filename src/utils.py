import urllib.request
from bs4 import BeautifulSoup


def get_video_id(url: str) -> str:
    resources = url.split('/detail/')
    if not resources or len(resources) < 2:
        resources = url.split('/dp/')
        if not resources or len(resources) < 2:
            return None
    if not (resources := resources[1].split('/')):
        return None
    return resources[0]


def get_soup(url: str):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    return soup


def get_title(soup) -> str:
    if not (results := soup.select('*[data-automation-id="title"]')):
        return None
    return results[0].text


def is_streaming_top(soup) -> bool:
    if not (top := soup.select('div[id="dv-action-box"]')):
        return False
    return is_streaming(top[0])


def is_streaming(ep) -> bool:
    if ep.select('a[href*="/gp/video/signup"]'):
        return True
    elif ep.select('a[href*="/gp/video/detail"]'):
        return True
    elif ep.select('a[href*="signup"]'):
        return True
    else:
        return False


def get_latest_ep(soup) -> int:
    if not is_streaming_top(soup):
        return -1
    if not (ep_list := soup.select('li[id^=av-ep-episodes-]')):
        return -1
    print_list = []
    for ep in reversed(ep_list):
        ep_num = int(ep['id'].split('-')[-1]) + 1
        if is_streaming(ep):
            print_list.append(str(ep_num) + '🆗')
            print('ep:' + ','.join(print_list))
            return ep_num
        print_list.append(str(ep_num) + '🈳')
    print('ep:' + ','.join(print_list))
    return -1

