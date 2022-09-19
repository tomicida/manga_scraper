import praw
from datetime import datetime
from plyer import notification

def main():
    #init necessary variables
    watchlist = []
    reddit = praw.Reddit("bot")
    new_chapters = []

    #populate watchlist from local file
    f1 = open("watchlist.txt","rt")
    for x in f1:
        watchlist.append(x.strip())
    watchlist.pop()
    f1.close()

    #extract chapters from relevant subreddit views
    extract_chapters(reddit.subreddit("manga").new(limit=100),new_chapters,watchlist)
    extract_chapters(reddit.subreddit("manga").hot(limit=25),new_chapters,watchlist)

    save_to_file(new_chapters)

def save_to_file(chapter_list):
    #record current time
    currdate = datetime.now().strftime("%Y%m%d%H%M%S")

    #save results to local file
    if len(chapter_list) > 0:
        f2 = open(currdate+"_new_chapters.txt","wt")
        for title in chapter_list:
           f2.write(title + "\n")
        f2.close()
    else:
        print("No results found")

def extract_chapters(subreddit_view, collection, watchlist):
    for submission in subreddit_view:
        if "[DISC]" in submission.title:
            for titlename in watchlist:
                if titlename in submission.title and submission.title not in collection:
                    collection.append(submission.title.strip())

if __name__ == "__main__":
    main()
