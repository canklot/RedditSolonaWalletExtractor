import praw

def GetCredentials():
    with open("../botdata.txt", "r",encoding="utf8") as file:
        # Please put yout credentials in upperfolder
        # To get your secret key go to https://www.reddit.com/prefs/apps 
        botdata = {"username":"","password":"","user_agent":"","client_secret":"","client_id":""}
        for var in botdata:
            botdata[var] = file.readline().strip()
        return botdata

def GetCommentsFromReddit(reddit):
    comments = []
    EndTime = 1645136456.0
    url = "https://www.reddit.com/r/solanadev/comments/sux0hu/we_published_spl_solana_token_please_leave_a/"
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)
    # If there is load more button, loads more
    for top_level_comment in submission.comments:
        if top_level_comment.created < EndTime:
            commentbody = top_level_comment.body
            comments.append(commentbody)
        #print(top_level_comment.body)   
    return comments

def DuplicateRemover(mylist):
    mylist = list(dict.fromkeys(mylist))
    return mylist
  
def FindWalletAddress(Data):
    WalletList = []
    NonWalletComments= []
    for comment in Data:
        if (len(comment)==44):
            WalletList.append(comment)
        else :
            NonWalletComments.append(comment)
            
        
    WalletCount = len(WalletList)
    WalletList = DuplicateRemover(WalletList)
    WalletCountIndividual = len(WalletList)
    DuplicateCount = WalletCount-WalletCountIndividual
    
    return WalletList

def WriteToFile(Data):
    with open("RedditResults.txt",'w',encoding = 'utf-8') as f:
        for line in Data:
            f.write(line+"\n")
        
def main():
    print("Working, this should take less than 5 minutes. Please wait...")
    botdata = GetCredentials()
    reddit = praw.Reddit(
        client_id=botdata["client_id"],
        client_secret=botdata["client_secret"],
        user_agent=botdata["user_agent"],
        username=botdata["username"],
        password=botdata["password"])
    reddit.read_only = True
    Comments = GetCommentsFromReddit(reddit)
    WalletList = FindWalletAddress(Comments)
    WriteToFile(WalletList)
    print("Thank you")
    
if __name__ == "__main__":
    main()
