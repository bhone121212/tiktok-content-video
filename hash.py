from TikTokApi import TikTokApi
import asyncio
import os
import app
import json
from sqlalchemy import update
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import random

ms_token = os.environ.get("AySjOsUhnRUCms09JiJ47wIqlss6EXPeWjdz2otVANAWFCf52sAiJssicwKW4hFt3gI6XSYVe-bdh73KNszJJMYQBT-QOq_7TFMgWFnJM6inN6ATgMQ5", None)  # set your own ms_token

ms_token2 = os.environ.get(
    "tg-gfxTNY1vFk8aX074Bx_fBpvBnQ3n0tiXc1CQsYIVVc0vJkVOeRTUrM62hlDcO_87fLtrP7QSw_8UXofYFoQyeiVB-bhFwrvI4kYhygig5KN1wk-zE3Oisnw3xOxCjUBJ3XiVEPbHKW4i3", None
) 
ms_token1 = os.environ.get(
    "6ZgMsdFEjgHnPcgKASehIfrCLwYKTVDvQJb-x4g8wo1EW8MY4F27aamjmYrYmsacZowsWEwqFxb-Z92K-jBCqM1rCyK8rr96227LVErJD4fLurIAt8tCUy8dY-_pFAa40aqF17ajISbjZOx7", None
)  # set your own ms_token, needs to have done a search before for this to work

#database_url = "postgresql://postgres:admin@localhost:5432/dbtiktok"
database_url = "postgresql://fbs:yah7WUy1Oi8G@172.32.253.129:5432/fbs"
engine = create_engine(database_url)

async def get_hashtag_videos(hashtag_name):
    async with TikTokApi() as api:        
        await api.create_sessions(ms_tokens=[ms_token,ms_token1,ms_token2], num_sessions=1, sleep_after=3,headless=False)

        with app.app.app_context():
            app.db.create_all()

            # trending = api.hashtag(name=hashtag)
            tag = api.hashtag(name=hashtag_name)
            hashtag_data = []
            async for video in tag.videos(count=50):

                hashtag_data.append(video.as_dict)
                hash_data = json.dumps(hashtag_data,indent=4)
                hash_out_data = json.loads(hash_data)
                # print(video)
                # print(hash_out_data)

            for hashtag in hash_out_data:
                #video_id = video_id 
                hash_name = hashtag_name                             
                hash_video_id = hashtag['id']                
                    #hash_video_url = comments['create_time']
                hash_video_createTime = hashtag['createTime']
                hash_video_duration = hashtag['video']['duration']
                hash_contents_desc = hashtag['desc']
                    
                author_id = hashtag['author']['id']
                author_nickname = hashtag['author']['nickname']
                author_uniqueId = hashtag['author']['uniqueId']
                author_diggCount = hashtag['authorStats']['diggCount']
                author_followerCount = hashtag['authorStats']['followerCount']
                author_followingCount = hashtag['authorStats']['followingCount']
                author_friendCount = hashtag['authorStats']['friendCount']
                author_heartCount = hashtag['authorStats']['heart']
                author_heart = hashtag['authorStats']['heartCount']
                author_videoCount = hashtag['authorStats']['videoCount']

                stats_collectCount = hashtag['stats']['collectCount']
                stats_commentCount = hashtag['stats']['commentCount']
                stats_diggCount = hashtag['stats']['diggCount']
                stats_playCount = hashtag['stats']['playCount']
                stats_shareCount = hashtag['stats']['shareCount']  

                user_url = 'https://www.tiktok.com/@{}'.format(author_uniqueId),

                hash_video_url = 'https://www.tiktok.com/@{}/video/{}'.format(author_nickname,hash_video_id),

                # print(hash_name,hash_video_id,hash_video_createTime,hash_video_duration,
                #       hash_contents_desc,author_id,author_nickname,author_uniqueId,author_diggCount,author_followerCount,
                #       author_followingCount,author_friendCount,author_heartCount,author_heart,author_videoCount,
                #       stats_collectCount,stats_commentCount,stats_diggCount,stats_playCount,stats_shareCount,hash_video_url)
                
                hashtag_video = app.TikTokVideosInfo(                        
                        # hash_name = hashtag_name,
                        video_id = hash_video_id,
                        source_id = author_id,
                        video_createtime = datetime.utcfromtimestamp(hash_video_createTime),
                        video_description = hash_contents_desc,
                        video_url = hash_video_url,
                        video_author = author_nickname,
                        video_duration = hash_video_duration,

                        # hash_video_url = hash_video_url,
                        # hash_video_createTime = datetime.utcfromtimestamp(hash_video_createTime),
                        # hash_video_duration = hash_video_duration,
                        # hash_contents_desc = hash_contents_desc,
                        
                        # author_id = author_id,
                        # author_nickname = author_nickname,
                        # author_uniqueId = author_uniqueId,
                        # author_diggCount = author_diggCount,
                        # author_followerCount = author_followerCount,
                        # author_followingCount = author_followingCount,
                        # author_friendCount = author_friendCount,
                        # author_heartCount = author_heartCount,
                        # author_heart = author_heart,
                        # author_videoCount = author_videoCount,

                        video_collectcount = stats_collectCount,
                        video_commentcount = stats_commentCount,
                        video_diggcount = stats_diggCount,
                        video_playcount = stats_playCount,
                        video_sharecount = stats_shareCount

                        # stats_collectCount = stats_collectCount,
                        # stats_commentCount = stats_commentCount,
                        # stats_diggCount = stats_diggCount,
                        # stats_playCount = stats_playCount,
                        # stats_shareCount = stats_shareCount
                    ) 
                # print(hashtag_video)               
                # app.db.session.add(hashtag_video)
                # print("Added hashtag {}".format(hash_video_id))
                # app.db.session.commit()
                
                check_video = app.db.session.query(app.TikTokVideosInfo).filter(app.TikTokVideosInfo.video_id == hash_video_id).first()

                if check_video is None:
                    try:
                        app.db.session.add(hashtag_video)
                        await asyncio.sleep(3) 
                        app.db.session.commit()
                        print("Added hashtag source is {} and content id {}".format(hashtag_name,hash_video_id))
                    except Exception as e:
                        print(f"Error updating data: {e}")
                        app.db.session.rollback()
                else:
                        update_hashtag_video = update(app.TikTokVideosInfo).where(check_video.video_id  == hash_video_id).values(
                        video_id = hash_video_id,
                        source_id = author_id,
                        video_createtime = datetime.utcfromtimestamp(hash_video_createTime),
                        video_description = hash_contents_desc,
                        video_url = hash_video_url,
                        video_author = author_nickname,
                        video_duration = hash_video_duration,
                        
                        video_collectcount = stats_collectCount,
                        video_commentcount = stats_commentCount,
                        video_diggcount = stats_diggCount,
                        video_playcount = stats_playCount,
                        video_sharecount = stats_shareCount
                    )                                    
                        app.db.session.execute(update_hashtag_video)         
                        await asyncio.sleep(3)                 
                        app.db.session.commit()
                        print("Updated hashtag source is {} and content id {}".format(hashtag_name,hash_video_id))
                
                # else:
                #         app.db.session.add(hashtag_video)
                #         await asyncio.sleep(3) 
                #         app.db.session.commit()
                #         print("Added hashtag {}".format(hash_video_id))

                # hashtag_info = app.TikTokUsersInfo(                        
                        # hash_name = hashtag_name,
                        # hash_video_id = hash_video_id,
                        # hash_video_url = hash_video_url,
                        # hash_video_createTime = datetime.utcfromtimestamp(hash_video_createTime),
                        # hash_video_duration = hash_video_duration,
                        # hash_contents_desc = hash_contents_desc,
                        
                        # source_id = author_id,
                        # user_nickname = author_nickname,
                        # user_uniqueId = author_uniqueId,
                        # user_diggCount = author_diggCount,
                        # user_followerCount = author_followerCount,
                        # user_followingCount = author_followingCount,
                        # user_friendCount = author_friendCount,
                        # user_heart = author_heartCount,
                        # author_heart = author_heart,
                        # user_videoCount = author_videoCount,
                        # user_url = user_url,

                        # stats_collectCount = stats_collectCount,
                        # stats_commentCount = stats_commentCount,
                        # stats_diggCount = stats_diggCount,
                        # stats_playCount = stats_playCount,
                        # stats_shareCount = stats_shareCount
                    # )

                # app.db.session.add(hashtag_info)
                # print("Added hashtag {}".format(author_id))
                # app.db.session.commit()

                # check = app.db.session.query(app.TikTokUsersInfo).filter(app.TikTokUsersInfo.source_id == author_id).first()                
                                
                # if check:
                #         update_hashtag_info = update(app.TikTokUsersInfo).where(check.source_id  == author_id).values(
                        # hash_name = hash_name,
                        # hash_video_id = hash_video_id,
                        # hash_video_url = hash_video_url,
                        # hash_video_createTime = datetime.utcfromtimestamp(hash_video_createTime),
                        # hash_video_duration = hash_video_duration,
                        # hash_contents_desc = hash_contents_desc,
                        
                        # source_id = author_id,
                        # user_nickname = author_nickname,
                        # user_uniqueId = author_uniqueId,
                        # user_diggCount = author_diggCount,
                        # user_followerCount = author_followerCount,
                        # user_followingCount = author_followingCount,
                        # user_friendCount = author_friendCount,
                        # user_heart = author_heartCount,
                        # author_heart = author_heart,
                        # user_videoCount = author_videoCount,
                        # user_url = user_url,
                        
                        # stats_collectCount = stats_collectCount,
                        # stats_commentCount = stats_commentCount,
                        # stats_diggCount = stats_diggCount,
                        # stats_playCount = stats_playCount,
                        # stats_shareCount = stats_shareCount
                #     )                                    
                #         app.db.session.execute(update_hashtag_info) 
                #         await asyncio.sleep(3)   
                #         app.db.session.commit()     
                #         print("Updated hashtag {}".format(author_id))                  
                        
                # else:
                #         app.db.session.add(hashtag_info)
                #         await asyncio.sleep(3)   
                #         app.db.session.commit()
                #         print("Added hashtag {}".format(author_id))
                        

if __name__ == "__main__":
    # asyncio.run(get_hashtag_videos(hashtag_name="စစ်မှုထမ်းဥပဒေ"))

    metadata = MetaData()
    users = Table('tbl_tk_hashtag_sources', metadata, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
                        
    all_hashtag = session.query(users).with_entities(app.TikTokHashKey.hash_name).all()
    rand_hash = random.sample(all_hashtag,3)
    sources = [''.join(user) for user in rand_hash] 
    print(sources)
    # if sources:  # Check if the list is not empty
    #     print(sources[-1])  # Print the last index value
    # else:
    #     print("The list 'sources' is empty.")
    
    # sources = ["လွတ်ငြိမ်း"]

    loop = asyncio.get_event_loop()
    loop.run_until_complete((get_hashtag_videos(sources[-1])))

    loop.close()