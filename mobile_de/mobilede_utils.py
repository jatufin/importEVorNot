import requests
import re
def request_car_detail_page(id):
    BASE_URL = 'https://suchen.mobile.de'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control' :'max-age=0',
    }

    resp = requests.get('{}/fahrzeuge/details.html?id={}'.format(BASE_URL, id), headers=headers)
    resp.status_code
    html = resp.text

    r = r'\"bm-verify":\s\"(.*)\",'
    r_i = r'var\si\s=\s(\d*);'
    r_j = r'Number\(\"(\d*)\"\s\+\s\"(\d*)\"\);'

    js = re.findall(r_j, html)[0]
    i = re.findall(r_i, html)[0]

    j = int(i) + int(js[0] + js[1])
    bm_verify = re.findall(r, html)[0]

    cookie_list = [line.strip() for i, line in enumerate(resp.headers['Set-Cookie'].split(',')) if i % 2 == 0]
    cookie_dict = { x[:i]: x[i+1:] for i, x in zip([x.find('=') for x in cookie_list], cookie_list)}
    cookie = ' '.join(['{}={}'.format(k, v) for k, v in cookie_dict.items()])

    resp2 = requests.post(
        '{}/_sec/verify?provider=interstitial'.format(BASE_URL),
        json={
            'bm-verify': bm_verify,
            'pow': j
        },
        headers={
            **headers,
            "Content-Type": "application/json",
            'Cookie': ' '.join(cookie)
        }
    )

    cookie_list = [line.strip() for i, line in enumerate(resp2.headers['Set-Cookie'].split(',')) if i % 2 == 0]
    cookie_dict_2 = { x[:i]: x[i+1:] for i, x in zip([x.find('=') for x in cookie_list], cookie_list)}
    cookie_dict.update(cookie_dict_2)
    cookie = ' '.join(['{}={}'.format(k, v) for k, v in cookie_dict.items()])

    resp3 = requests.get(
        '{}{}'.format(BASE_URL, resp2.json()['location']),
        headers={
            **headers,
            "Content-Type": "application/json",
            'Cookie': ' '.join(cookie),
            'Referer': 'https://www.mobile.de/'
        }
    )

    return resp3.text