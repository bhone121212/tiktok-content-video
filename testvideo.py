from TikTokApi import TikTokApi
import asyncio
import os
import time


ms_token = "KHeiX7DtKP2LA7-CEPmuVPZ5Y9KzPzeF2NEzIwk87knPb7Heuz1pIDX2eGrRlRQerH3vtGiErY9wpgo80fZqc8foG_pajChnWYA8BeKyhYaoJ9GDuvMuFLreSIonNuE7zGrZbA=="

# async def user_example():
#     async with TikTokApi() as api:
#         await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3,headless=False)
#         user = api.user("willpowermyanmar")
#         user_data = await user.info()
#         print(user_data)

#         async for video in user.videos(count=10):
#             print(video)
#             print(video.as_dict)

        # async for playlist in user.playlists():
        #     print(playlist)

async def get_user_videos(username):
    start_time = time.time()
    row_count = 0

    async with TikTokApi() as api:
        await api.create_sessions(headless=False, ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        user = api.user(username)
        user_data = await user.info()
        post_count = user_data["userInfo"]["stats"].get("videoCount")

        print(post_count)

        async for video in user.videos(count=10):
            # url = f"https://www.tiktok.com/@{video.as_dict['author']['uniqueId']}/video/{video.id}"
            # print(f"URL: {url}") 
            # row_count += 1
            print(video)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time} seconds")
    print(f"Total rows: {row_count}")
    print(f"Rows per second: {row_count / elapsed_time}")

async def get_video_example():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(
            url="https://www.tiktok.com/@davidteathercodes/video/7074717081563942186"
        )

        async for related_video in video.related_videos(count=10):
            print(related_video)
            print(related_video.as_dict)

        video_info = await video.info()  # is HTML request, so avoid using this too much
        print(video_info)
        # video_bytes = await video.bytes()
        # with open("video.mp4", "wb") as f:
        #     f.write(video_bytes)

async def user_example():
    async with TikTokApi() as api:
        await api.create_sessions(headless=False,ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        user = api.user("elevenmedia")
        user_data = await user.info()
        print(user_data)

        async for video in user.videos(count=30):
            print(video)
            # print(video.as_dict)

        async for playlist in user.playlists():
            print(playlist)


if __name__ == "__main__":
    # asyncio.run(get_user_videos(username='elevenmedia'))
    asyncio.run(user_example())

# if __name__ == "__main__":
#     asyncio.run(get_video_example())

# if __name__ == "__main__":
#     asyncio.run(get_user_videos(username="elevenmedia"))

# docker pull mcr.microsoft.com/playwright:focal
# docker build . -t tiktokapi:latest
# docker run -v TikTokApi --rm tiktokapi:latest python3 your_script.py