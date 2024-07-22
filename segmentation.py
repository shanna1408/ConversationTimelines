from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
import requests
from collections import Counter


# Break one long dialog into chunks by topic
def segment_dialog(dialogue):
    segments = []
    current_segment = []
    current_sentiment = None
    
    sid = SentimentIntensityAnalyzer()
    sentiments = []
    past_sentiments=[]
    future_sentiments=[]
    for i in range(len(dialogue)):
        sentence = dialogue[i]
        if len(word_tokenize(sentence))<3:
            continue

        sentiment = sid.polarity_scores(sentence)["compound"]
        
        if current_sentiment is None:
            current_sentiment = sentiment
        
        past_sentiments.append(sentiment)
        # print(sentiments)
        if (len(past_sentiments)>4):
            past_sentiments.pop(0)
        if (i<len(dialogue)-4):
            future_sentiments = [sid.polarity_scores(dialogue[i+1])["compound"], sid.polarity_scores(dialogue[i+2])["compound"], sid.polarity_scores(dialogue[i+3])["compound"]]
        sentiments = past_sentiments+future_sentiments

        scores = []
        for s in sentiments:
            if not (s==sentiment):
                scores.append(abs(sentiment - s))
        if (len(scores)==0):
            scores.append(0)

        if (sum(scores) / len(scores)) > 0.7:
            # print("new: "+str(min(scores))+" old: "+str(abs(sentiment - current_sentiment)))
            segment = " ".join(current_segment)
            if ((len(segment.split())>50) or len(segments)<1):   
                segments.append(" ".join(current_segment))
            else:
                segments[-1] += " " + segment
            current_segment = []
            current_sentiment = sentiment
        
        current_segment.append(sentence)
    
    if current_segment:
        segments.append(" ".join(current_segment))
    
    return segments

def short_seg(dialogue, num_words):
    segments = []
    curr_seg = ""
    for i in range(len(dialogue)):
        sentence = dialogue[i]
        len_sent = len(sentence.split())
        curr_seg += " " + sentence
        if (len(curr_seg.split())>num_words):
            segments.append(curr_seg)
            curr_seg = ""
    return segments
    

def main():
    data = "Transcript2/SV_Transcript.txt"

    # Get the dialogue broken into a list by sentence
    text = ""
    for line in open(data, encoding="utf-8"):
        text += str(line)
    tokenized_text = sent_tokenize(text)

    num_1min = 140
    num_10sec = 24
    
    # Segment the dialogue
    tensec_segments = short_seg(tokenized_text, num_10sec)
    onemin_segments = short_seg(tokenized_text, num_1min)
    topic_segments = segment_dialog(tokenized_text)

    segments_text = open("Transcript2/10sec_segments.txt", "w")
    i = 0
    for segment in tensec_segments:
        segments_text.write(f"Segment {i}: {segment}\n\n")
        i += 1
    segments_text.close()

    segments_text = open("Transcript2/1min_segments.txt", "w")
    i = 0
    for segment in onemin_segments:
        segments_text.write(f"Segment {i}: {segment}\n\n")
        i += 1
    segments_text.close()

    segments_text = open("Transcript2/segments.txt", "w")
    i = 0
    for segment in topic_segments:
        segments_text.write(f"Segment {i}: {segment}\n\n")
        i += 1
    segments_text.close()
    
if __name__ == "__main__":
    main()
    