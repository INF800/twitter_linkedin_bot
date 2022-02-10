# twitter_linkedin_bot
Post tweets from twitter into linkedin

> Currently supports only ubuntu os.

### How to setup

- Create `.env` file in main directory as follows with Linkedin and Twitter API access tokens and other information
    ```shell
    # #### linkedin dev tools
    # generated only after we fill all files in app (including policy url and company url in widget section)
    # goto auth tool -> generate token
    # deprecation warning: token will expire in 2mos by default. https://www.linkedin.com/developers/apps/{app-id}/settings
    LINKEDIN_ACCESS_TOKEN="..."
    # `URN` is same as `id`
    # REQUEST: https://api.linkedin.com/v2/me?oauth2_access_token={ACCESS_TOKEN}
    # RESPONSE: {"localizedLastName":"Rakesh","profilePicture":{"displayImage":"urn:li:digitalmediaAsset:C****ijvbbdfwg"},"firstName":{"localized":{"en_US":"Asapanna"},"preferredLocale":{"country":"US","language":"en"}},"lastName":{"localized":{"en_US":"Rakesh"},"preferredLocale":{"country":"US","language":"en"}},"id":"***********","localizedFirstName":"Asapanna"}
    LINKEDIN_URN="..."


    # #### twitter dev tools
    # keys are available in first page after signup
    TWITTER_API_KEY="..."
    TWITTER_API_KEY_SECRET="..."
    # test bearer token using: `curl -X GET -H "Authorization: Bearer {BEARER_TOKEN}" "https://api.twitter.com/2/tweets/20"`
    TWITTER_ACCESS_TOKEN="..."
    # REQUEST: curl -X GET -H "Authorization: Bearer {BEARER_TOKEN}"  "https://api.twitter.com/2/users/by?usernames=inf800"
    # RESPONSE: {"data":[{"id":"229305005382828","name":"Asapanna Rakesh","username":"inf800"}]}
    # `id` i.e TWITTER_USER_ID is used to fetch latest tweets using:
    # curl -X GET -H "Authorization: Bearer {BEARER_TOKEN}"  "https://api.twitter.com/2/users/229305005382828/tweets?max_results=10"
    # curl -X GET -H "Authorization: Bearer {BEARER_TOKEN}"  "https://api.twitter.com/2/users/229305005382828/tweets?start_time=..."
    # curl -X GET -H "Authorization: Bearer {BEARER_TOKEN}"  "https://api.twitter.com/2/users/229305005382828/tweets?end_time=..."
    # curl -X GET -H "Authorization: Bearer {BEARER_TOKEN}"  "https://api.twitter.com/2/users/229305005382828/tweets?since_id={last_published_tweet_id}"
    TWITTER_USER_ID="229305005382828"
    TWITTER_USERNAME="inf800"
    ```
- Install google chrome and package requirements using `install.sh`
- Publish your latest tweets and retweets using `run.sh`
- To automate, add the secrets in repo > settings > secrests > actions.