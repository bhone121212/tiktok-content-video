from TikTokApi import TikTokApi
import asyncio
import json
import os
import logging
import random

from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker

from sqlalchemy import update
import app
from datetime import datetime

#ms_token = os.environ.get(
#    "ms_token", None
#)  # set your own ms_token, think it might need to have visited a profile
#database_url = "postgresql://postgres:admin@localhost:5432/dbtiktok"
database_url = "postgresql://fbs:yah7WUy1Oi8G@172.32.253.129:5432/fbs"
engine = create_engine(database_url)

ms_token = "AySjOsUhnRUCms09JiJ47wIqlss6EXPeWjdz2otVANAWFCf52sAiJssicwKW4hFt3gI6XSYVe-bdh73KNszJJMYQBT-QOq_7TFMgWFnJM6inN6ATgMQ5"
ms_token2 = "tg-gfxTNY1vFk8aX074Bx_fBpvBnQ3n0tiXc1CQsYIVVc0vJkVOeRTUrM62hlDcO_87fLtrP7QSw_8UXofYFoQyeiVB-bhFwrvI4kYhygig5KN1wk-zE3Oisnw3xOxCjUBJ3XiVEPbHKW4i3"
ms_token1 = "6ZgMsdFEjgHnPcgKASehIfrCLwYKTVDvQJb-x4g8wo1EW8MY4F27aamjmYrYmsacZowsWEwqFxb-Z92K-jBCqM1rCyK8rr96227LVErJD4fLurIAt8tCUy8dY-_pFAa40aqF17ajISbjZOx7"# get your own ms_token from your cookies on tiktok.com

class UserInfo:
    o_data = []
    vo_data = []
    source = []
    async def user_profile_data(all_users):   
        async with TikTokApi() as api:      
                sources = [''.join(user) for user in all_users] 
                for source in sources:
                    UserInfo.source = source
                    print(source)                
                    #u = 'rfaburmese'
                    await api.create_sessions(ms_tokens=[ms_token,ms_token1,ms_token2], num_sessions=1, sleep_after=3,headless=False)     
                    user = api.user(UserInfo.source)
                    #print(user)
                    user_data = await user.info() 
                    #print(user_data)              
                            
                    user_videos = []          

                    r_data = json.dumps(user_data,indent=4)
                    UserInfo.o_data = json.loads(r_data) 

                    vcounts = UserInfo.o_data["userInfo"]["stats"]["videoCount"]  
                    print(vcounts)

                    ####users videos collect#######
                    async for video in user.videos(count = 5):  
                    #print(video.as_dict)              
                        user_videos.append(video.as_dict)                    
                    #### collect users data convert json format #######
                    v_data = json.dumps(user_videos,indent=4)
                    UserInfo.vo_data = json.loads(v_data)

                    await insert_video()          

async def insert_video():                
    with app.app.app_context():
        app.db.create_all()   
        
        for select_data in UserInfo.vo_data:
                                video_id = select_data["id"]
                                source_id = UserInfo.o_data["userInfo"]["user"]["id"]
                                video_createtime = select_data["createTime"]
                                video_description = str(select_data["desc"])
                                video_url = 'https://www.tiktok.com/@{}/video/{}'.format(UserInfo.source,select_data["id"])
                                video_author =  select_data["music"]["authorName"]
                                video_duration = select_data["music"]["duration"]
                                video_music_title = select_data["music"]["title"]
                                video_collectcount = select_data["stats"]["collectCount"]
                                video_commentcount = select_data["stats"]["commentCount"]
                                video_diggcount = select_data["stats"]["diggCount"]
                                video_playcount = select_data["stats"]["playCount"]
                                video_sharecount = select_data["stats"]["shareCount"]
                                #print(video_id)

                                users_videos = app.TikTokVideosInfo(
                                    video_id=video_id, 
                                    source_id = source_id,
                                    video_createtime = datetime.utcfromtimestamp(video_createtime),
                                    video_description = video_description,
                                    video_url = video_url,                          
                                    video_author = video_author,
                                    video_duration = video_duration,
                                    video_music_title = video_music_title,
                                    video_collectcount = video_collectcount,
                                    video_commentcount = video_commentcount,
                                    video_diggcount = video_diggcount,
                                    video_playcount = video_playcount,
                                    video_sharecount = video_sharecount)
                                
                                #result_video = app.db.session.query(app.TikTokVideosInfo).filter(app.TikTokVideosInfo.video_id == video_id).first()
                                #print(result_video)

                                result_video = app.db.session.query(app.TikTokVideosInfo).filter(app.TikTokVideosInfo.video_id == video_id).first()
                                #print(result_video)

                                if result_video is None:
                                    try:
                                        app.db.session.add(users_videos)
                                        await asyncio.sleep(3)
                                        app.db.session.commit()
                                        print("video data source is added successful, video id : {}".format(video_id))
                                    except Exception as e:
                                        print(f"Error updating data: {e}")
                                        app.db.session.rollback()

                                else:
                                    update_user_videos = update(app.TikTokVideosInfo).where(result_video.video_id  == video_id).values(
                                        #source_id = source_id,
                                        video_createtime = datetime.utcfromtimestamp(video_createtime),
                                        video_description = video_description,
                                        video_url = video_url,                          
                                        video_author = video_author,
                                        video_duration = video_duration,
                                        video_music_title = video_music_title,
                                        video_collectcount = video_collectcount,
                                        video_commentcount = video_commentcount,
                                        video_diggcount = video_diggcount,
                                        video_playcount = video_playcount,
                                        video_sharecount = video_sharecount)
                                    
                                    try:
                                        app.db.session.execute(update_user_videos)
                                        await asyncio.sleep(3)
                                        app.db.session.commit()   
                                        print("video data source is updated successful, video id : {}".format(video_id))
                                    except Exception as e:
                                        print(f"Error updating data: {e}")
                                        app.db.session.rollback()  

if __name__ == "__main__":
        # asyncio.run(UserInfo.user_profile_data(all_users="elevenmedia"))
        metadata = MetaData()
        users = Table('tbl_tk_sources', metadata, autoload_with=engine)
        Session = sessionmaker(bind=engine)
        session = Session()
                        
        all_users = session.query(users).with_entities(app.TikTokSources.source_name).all()
        rand_source = random.sample(all_users,3)
        sources = [''.join(user) for user in rand_source] 
        print(sources)
        
        # sources = ["elevenmedia"] #yangonmediagroup #1108 #elevenmedia

        #asyncio.get_running_loop()

        loop = asyncio.get_event_loop()
        loop.run_until_complete((UserInfo.user_profile_data(sources)))

        loop.close() 