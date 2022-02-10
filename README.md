# twitter_linkedin_bot

Post tweets from twitter into linkedin. Automated using github actions (Note the database trick).

> Currently supports only ubuntu os.

### How to setup

- Create `.env` file in main directory as follows with Linkedin and Twitter API access tokens and other information
    ```shell
    LINKEDIN_ACCESS_TOKEN="..."
    LINKEDIN_URN="..."
    TWITTER_API_KEY="..."
    TWITTER_API_KEY_SECRET="..."
    TWITTER_ACCESS_TOKEN="..."
    TWITTER_USER_ID="..."
    TWITTER_USERNAME="..."
    ```
    More info present [here](env_help) on how to acquire keys.
    
- Install google chrome and package requirements using `install.sh`
- Publish your latest tweets and retweets using `run.sh`
- To automate, add the secrets in repo > settings > secrests > actions.
