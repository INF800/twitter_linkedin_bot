from pprint import pprint
import requests
import os
import requests
from html2image import Html2Image
from os.path import join, dirname
from dotenv import load_dotenv
import cv2
import numpy as np


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_FILE_PATH = 'db.txt'
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME') 
TWITTER_USER_ID = os.getenv('TWITTER_USER_ID')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
WAIT_MS_HTML_RENDERING = 8000
LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')
LINKEDIN_URN = os.getenv('LINKEDIN_URN')


def fetch_last_published():
    with open(DB_FILE_PATH, 'r') as fp:
        data = fp.read()
    last = data.split('\n')[-2]
    return last

def write_published(tweet_id):
    with open(DB_FILE_PATH, 'a') as fp:
        fp.write(f"{tweet_id}\n")


def fetch_all_tweets(user_id, since_id=None):
    headers = {'Authorization': f'Bearer {TWITTER_ACCESS_TOKEN}'}
    if since_id:
        response = requests.get(f"https://api.twitter.com/2/users/{user_id}/tweets?since_id={since_id}", headers=headers)
    else:
        response = requests.get(f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=5", headers=headers)
    if response.status_code!=200:
        print('could not fetch tweets because:', response.content)
        return []
    if response.json()['meta']['result_count']==0:
        print('No new tweets found.')
        return []
    tweets = response.json()['data']
    return tweets[::-1] # last to recent


def generate_html(tweet, username):
    tweet_id = tweet['id']
    r = requests.get(f"https://publish.twitter.com/oembed?url=https%3A%2F%2Ftwitter.com%2F{username}%2Fstatus%2F{tweet_id}&theme=dark")
    html_content = r.json()['html']
    css_before = "<style>html {background-color: #161721;}</style>"
    return css_before + html_content


def generate_image_from_html(html_content, wait_ms, im_path='tmp.png'):
    #### geneate image
    hti = Html2Image(custom_flags=[f'--virtual-time-budget={wait_ms}', '--hide-scrollbars'])
    hti.browser_executable = "/usr/bin/google-chrome" # use install_google_chrome.sh
    hti.screenshot(html_str=html_content, save_as=im_path, size=(550, 1000))
    #### crop tweet region
    im = cv2.imread(im_path, 0)
    sumy = im.sum(axis=1)
    mask = (sumy!=sumy[-1]) 
    idxs = np.arange(len(sumy))[mask]
    hmax = idxs.max()+10
    im = cv2.imread(im_path)[:hmax, :, :]
    cv2.imwrite(im_path, im)
    return im_path


def upload_image(image_path):
    #### generate upload url
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}'}
    api_url = 'https://api.linkedin.com/v2/assets?action=registerUpload'
    post_data = {
        "registerUploadRequest":{
            "owner": f"urn:li:person:{LINKEDIN_URN}",
            "recipes":[
                "urn:li:digitalmediaRecipe:feedshare-image"
            ],
            "serviceRelationships":[
                {
                    "identifier":"urn:li:userGeneratedContent",
                    "relationshipType":"OWNER"
                }
            ],
            "supportedUploadMechanism":[
                "SYNCHRONOUS_UPLOAD"
            ]
        }
    }
    response = requests.post(api_url, headers=headers, json=post_data)
    if response.status_code!=200:
        print('could not generate upload url becase:', response.content)
        return None
    upload_url = response.json()['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    asset = response.json()['value']['asset']
    process = os.popen(f'curl -i --upload-file {image_path} -H "Authorization: Bearer {LINKEDIN_ACCESS_TOKEN}" "{upload_url}"')
    preprocessed = process.read()
    process.close()
    return asset


def post_on_linkedin(image_media, text=""):
    api_url = f'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINKEDIN_ACCESS_TOKEN}'
    }
    post_data = {
        "author":  f"urn:li:person:{LINKEDIN_URN}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text,
                },
                "shareMediaCategory": "IMAGE",
                "media": [{
                    "media": image_media,
                    "status": "READY",
                    "title": {
                        "attributes": [],
                        "text": "Twitter post"
                    }
                }],
            },
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        },
    }
    response = requests.post(api_url, headers=headers, json=post_data)
    if response.status_code!=201:
        print('could not publish post data:', response.content)


def main():

    #### fetch last published if done so
    last_published_id = None
    if os.path.exists(DB_FILE_PATH):
        last_published_id = fetch_last_published()

    #### all tweets to publish since last published
    tweets = fetch_all_tweets(TWITTER_USER_ID, last_published_id)

    #### publish tweets to linkedin & save as done
    for tweet in tweets:
        html_content = generate_html(tweet, username=TWITTER_USERNAME)
        image_path = generate_image_from_html(html_content, wait_ms=WAIT_MS_HTML_RENDERING)
        digital_asset = upload_image(image_path)
        
        if not digital_asset:
            continue
        
        twitter_text = tweet['text']
        link = html_content.split('<a href="https://twitter.com/')[-1].split('</a>')[0].split('">')[0]
        text = f"Twitter Post: https://twitter.com/{link}\n\nPosting #MachineLearning content from Twitter to Linkedin. Double tap on the image to democrtize machine learnining content. This message was automatically generated by @gov-ai."
        post_on_linkedin(digital_asset, text=text)
        write_published(tweet['id'])





if __name__=='__main__':
    main()
