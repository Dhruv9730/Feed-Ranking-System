import heapq

def rank_posts_with_decay_and_ratio(df, top_n =10):
    now =datetime.now()
    cutoff = now - timedelta(hours =24)

    #Step 1: Filter to last 24 hours
    recent_df = df[df["timestamp"] >=cutoff]

    #Step 2: Agrregate post scores
    post_scores = {}

    for _, row in recent_df.iterrows():
        post =row["post"]

        #Time decay logic
        hours_old = (now -row["timestamp"]).total_seconds() /3600
        freshness_weight = max(1,24 - hours_old)

        #Ratio-based Score
        likes =row['likes']
        comments =row['comments']
        enagement_score =(likes/ (comments+1)) # Avoid division by zero
        # Weighted score with freshness
        raw_score =row["likes"]*2 +row["comments"]*3
        final_score =enagement_score * (freshness_weight/24)
        
        if post in post_scores:
            post_scores[post] += final_score
        else:
            post_scores[post] = final_score

    #Step 3 : Max Heap for top-N
    max_heap =[(-score, post) for post, score in post_scores.items()]
    heapq.heapify(max_heap)

    #Step 4: Extract top-N
    top_posts =[]
    for _ in range(min(top_n, len(max_heap))):
        score , post =heapq.heappop(max_heap)
        top_posts.append((post, -score))

    return top_posts

def personalized_feed(user_id, df,top_n =5):
    now =datetime.now()
    cutoff =  now - timedelta(hours =24)

    #Step 1 : Filter to last 24h and only current user
    user_df =df[(df["timestamp"] >= cutoff) & (df['user'] == user_id)]

    #Step 2: compute post scores form that user's interactions
    post_scores ={}

    for _, row in user_df.iterrows():
        post = row['post']
        hours_old =(now -row['timestamp']).total_seconds() /3600
        freshness_weight = max(1, 24-hours_old)

        likes = row['likes']
        comments = row['comments']
        enagement_score =(likes/ (comments +1))
        final_score = enagement_score * (freshness_weight /24)

        if post in post_scores:
            post_scores[post] += final_score
        else:
            post_scores[post]  = final_score

    #Step 3: Heap to get top-N posts
    max_heap =[(-score, post) for post, score in post_scores.items()]
    heapq.heapify(max_heap)

    #Step 4: Extract top-N
    top_posts =[]
    for _ in range(min(top_n, len(max_heap))):
        score , post =heapq.heappop(max_heap)
        top_posts.append((post, -score))

    return top_posts