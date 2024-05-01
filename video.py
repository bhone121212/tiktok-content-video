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

ms_token = "ZzFUUrA00TSsLWbERKELlxbIPCGej2ihoBA_WJoz6F0gcr493Tp9T8KYMQrFgXiJ4N0k91ILC_iqlcK0ycsrxo4jJV3He8TbOD2NX5pZxirZ_ZNklL4A3OwSv4qV"
ms_token2 = "Tp91uG7q90fIMy5XUz3QwePFlV7VSuVDgcGLYnGghzHfBLSGeeidZsNDxZOL7N1mmovO5kqxoZI3AGiH_Dmd9Mg1-4XCLxlXM6OQPEg7iz7-rcRa6ARgfkNGbA5T"
ms_token1 = "HrJr2bxMVGwLmSxp7fvH-ZOsaJRGg0R9_Sa931ykhuBzQJHBPQDAy15ONGuFwZQDwpmnwOMBSTQlSlEOeDjyMEHQumPELa9x7Y7PC0ddVdK0lfu3mnnfj8K-GUiw"# get your own ms_token from your cookies on tiktok.com

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
                    async for video in user.videos(count = 30):  
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

                                        #content_id collect from table tiktokvideo info
                                        content = app.db.session.query(app.TikTokVideosInfo.id).filter(app.TikTokVideosInfo.video_id == video_id).all()

                                        # Extracting the id values from the result
                                        ids = [row.id for row in content]                       

                                        # Reflect the  table from the database
                                        content_table = Table('all_content', metadata, autoload_with=engine)

                                        # Access the columns of the "content" table
                                        columns = content_table.columns.keys()

                                        # Print the column names
                                        content_column = columns[1]
                                        network_column = columns[2]
                                        # print("content_column {},network_column {}".format(ids,5))

                                        # Define the values to insert
                                        values_to_insert = [
                                            {content_column: content_id, network_column: 5} for content_id in ids
                                        ]

                                        # Create an insert statement
                                        insert_allcontent = content_table.insert().values(values_to_insert)

                                        # Execute the insert statement
                                        app.db.session.execute(insert_allcontent)
                                        print("Added content id values : {} for network id 5".format(ids))

                                    except Exception as e:
                                        print(f"Error updating data: {e}")
                                        app.db.session.rollback()

                                else:
                                    update_user_videos = update(app.TikTokVideosInfo).where(app.TikTokVideosInfo.video_id  == video_id).values(
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
        rand_source = random.sample(all_users,7)
        sources = [''.join(user) for user in rand_source] 
        print(sources)
        
        #sources = ["elevenmedia"] #yangonmediagroup #1108 #elevenmedia

        #asyncio.get_running_loop()

        loop = asyncio.get_event_loop()
        loop.run_until_complete((UserInfo.user_profile_data(sources)))

        loop.close() 